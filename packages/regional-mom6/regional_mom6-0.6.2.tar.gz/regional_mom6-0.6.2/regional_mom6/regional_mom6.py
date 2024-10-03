import numpy as np
from pathlib import Path
import dask.array as da
import xarray as xr
import xesmf as xe
import subprocess
from scipy.ndimage import binary_fill_holes
import netCDF4
from dask.diagnostics import ProgressBar
import f90nml
import datetime as dt
import warnings
import shutil
import os
import importlib.resources
import datetime
from .utils import quadrilateral_areas


warnings.filterwarnings("ignore")

__all__ = [
    "longitude_slicer",
    "hyperbolictan_thickness_profile",
    "rectangular_hgrid",
    "experiment",
    "segment",
]


## Auxiliary functions


def longitude_slicer(data, longitude_extent, longitude_coords):
    """
    Slice longitudes while handling periodicity and the 'seams', that is the
    longitude values where the data wraps around in a global domain (for example,
    longitudes are defined, usually, within domain [0, 360] or [-180, 180]).

    The algorithm works in five steps:

    - Determine whether we need to add or subtract 360 to get the middle of the
      ``longitude_extent`` to lie within ``data``'s longitude range (hereby ``old_lon``).

    - Shift the dataset so that its midpoint matches the midpoint of
      ``longitude_extent`` (up to a multiple of 360). Now, the modified ``old_lon``
      does not increase monotonically from West to East since the 'seam'
      has moved.

    - Fix ``old_lon`` to make it monotonically increasing again. This uses
      the information we have about the way the dataset was shifted/rolled.

    - Slice the ``data`` index-wise. We know that ``|longitude_extent[1] - longitude_extent[0]| / 360``
      multiplied by the number of discrete longitude points in the global input data gives
      the number of longitude points in our slice, and we've already set the midpoint
      to be the middle of the target domain.

    - Finally re-add the correct multiple of 360 so the whole domain matches
      the target.

    Args:
        data (xarray.Dataset): The global data you want to slice in longitude.
        longitude_extent (Tuple[float, float]): The target longitudes (in degrees)
            we want to slice to. Must be in increasing order.
        longitude_coords (Union[str, list[str]): The name or list of names of the
            longitude coordinates(s) in ``data``.
    Returns:
        xarray.Dataset: The sliced ``data``.
    """

    if isinstance(longitude_coords, str):
        longitude_coords = [longitude_coords]

    for lon in longitude_coords:
        central_longitude = np.mean(longitude_extent)  ## Midpoint of target domain

        ## Find a corresponding value for the intended domain midpoint in our data.
        ## It's assumed that data has equally-spaced longitude values.

        λ = data[lon].data
        dλ = λ[1] - λ[0]

        assert np.allclose(
            np.diff(λ), dλ * np.ones(np.size(λ) - 1)
        ), "provided longitude coordinate must be uniformly spaced"

        for i in range(-1, 2, 1):
            if data[lon][0] <= central_longitude + 360 * i <= data[lon][-1]:

                ## Shifted version of target midpoint; e.g., could be -90 vs 270
                ## integer i keeps track of what how many multiples of 360 we need to shift entire
                ## grid by to match central_longitude
                _central_longitude = central_longitude + 360 * i

                ## Midpoint of the data
                central_data = data[lon][data[lon].shape[0] // 2].values

                ## Number of indices between the data midpoint and the target midpoint.
                ## Sign indicates direction needed to shift.
                shift = int(
                    -(data[lon].shape[0] * (_central_longitude - central_data)) // 360
                )

                ## Shift data so that the midpoint of the target domain is the middle of
                ## the data for easy slicing.
                new_data = data.roll({lon: 1 * shift}, roll_coords=True)

                ## Create a new longitude coordinate.
                ## We'll modify this to remove any seams (i.e., jumps like -270 -> 90)
                new_lon = new_data[lon].values

                ## Take the 'seam' of the data, and either backfill or forward fill based on
                ## whether the data was shifted F or west
                if shift > 0:
                    new_seam_index = shift

                    new_lon[0:new_seam_index] -= 360

                if shift < 0:
                    new_seam_index = data[lon].shape[0] + shift

                    new_lon[new_seam_index:] += 360

                ## new_lon is used to re-centre the midpoint to match that of target domain
                new_lon -= i * 360

                new_data = new_data.assign_coords({lon: new_lon})

                ## Choose the number of lon points to take from the middle, including a buffer.
                ## Use this to index the new global dataset
                num_lonpoints = (
                    int(data[lon].shape[0] * (central_longitude - longitude_extent[0]))
                    // 360
                )

        data = new_data.isel(
            {
                lon: slice(
                    data[lon].shape[0] // 2 - num_lonpoints,
                    data[lon].shape[0] // 2 + num_lonpoints,
                )
            }
        )

    return data


from pathlib import Path


def get_glorys_data(
    longitude_extent,
    latitude_extent,
    timerange,
    segment_name,
    download_path,
    modify_existing=True,
):
    """
    Generates a bash script to download all of the required ocean forcing data.

    Args:
        longitude_extent (tuple of floats): Westward and Eastward extents of the segment
        latitude_extent (tuple of floats): Southward and Northward extents of the segment
        timerange (tule of datetime strings): Start and end of the segment in format %Y-%m-%d %H:%M:%S
        segment_range (str): name of the segment (minus .nc extension, eg east_unprocessed)
        download_path (str): Location of where this script is saved
        modify_existing (bool): Whether to add to an existing script or start a new one
        buffer (float): number of
    """
    buffer = 0.24  # Pads downloads to ensure that interpolation onto desired domain doesn't fail. Default of 0.24 is twice Glorys cell width (12th degree)

    path = Path(download_path)

    if modify_existing:
        file = open(path / "get_glorysdata.sh", "r")
        lines = file.readlines()
        file.close()

    else:
        lines = ["#!/bin/bash\ncopernicusmarine login"]

    file = open(path / "get_glorysdata.sh", "w")

    lines.append(
        f"""
copernicusmarine subset --dataset-id cmems_mod_glo_phy_my_0.083deg_P1D-m --variable so --variable thetao --variable uo --variable vo --variable zos --start-datetime {str(timerange[0]).replace(" ","T")} --end-datetime {str(timerange[1]).replace(" ","T")} --minimum-longitude {longitude_extent[0] - buffer} --maximum-longitude {longitude_extent[1] + buffer} --minimum-latitude {latitude_extent[0] - buffer} --maximum-latitude {latitude_extent[1] + buffer} --minimum-depth 0 --maximum-depth 6000 -o {str(path)} -f {segment_name}.nc --force-download\n
"""
    )
    file.writelines(lines)
    file.close()
    return


def hyperbolictan_thickness_profile(nlayers, ratio, total_depth):
    """Generate a hyperbolic tangent thickness profile with ``nlayers`` vertical
    layers and total depth of ``total_depth`` whose bottom layer is (about) ``ratio``
    times larger than the top layer.

    The thickness profile transitions from the top-layer thickness to
    the bottom-layer thickness via a hyperbolic tangent proportional to
    ``tanh(2π * (k / (nlayers - 1) - 1 / 2))``, where ``k = 0, 1, ..., nlayers - 1``
    is the layer index with ``k = 0`` corresponding to the top-most layer.

    The sum of all layer thicknesses is ``total_depth``.

    Positive parameter ``ratio`` prescribes (approximately) the ratio of the thickness
    of the bottom-most layer to the top-most layer. The final ratio of the bottom-most
    layer to the top-most layer ends up a bit different from the prescribed ``ratio``.
    In particular, the final ratio of the bottom over the top-most layer thickness is
    ``(1 + ratio * exp(2π)) / (ratio + exp(2π))``. This slight departure comes about
    because of the value of the hyperbolic tangent profile at the end-points ``tanh(π)``,
    which is approximately 0.9963 and not 1. Note that because ``exp(2π)`` is much greater
    than 1, the value of the actual ratio is not that different from the prescribed value
    ``ratio``, e.g., for ``ratio`` values between 1/100 and 100 the final ratio of the
    bottom-most layer to the top-most layer only departs from the prescribed ``ratio``
    by ±20%.

    Args:
        nlayers (int): Number of vertical layers.
        ratio (float): The desired value of the ratio of bottom-most to
            the top-most layer thickness. Note that the final value of
            the ratio of bottom-most to the top-most layer thickness
            ends up ``(1 + ratio * exp(2π)) / (ratio + exp(2π))``. Must
            be positive.
        total_depth (float): The total depth of grid, i.e., the sum
            of all thicknesses.

    Returns:
        numpy.array: An array containing the layer thicknesses.

    Examples:

        The spacings for a vertical grid with 20 layers, with maximum depth 1000 meters,
        and for which the top-most layer is about 4 times thinner than the bottom-most
        one.

        >>> from regional_mom6 import hyperbolictan_thickness_profile
        >>> nlayers, total_depth = 20, 1000
        >>> ratio = 4
        >>> dz = hyperbolictan_thickness_profile(nlayers, ratio, total_depth)
        >>> dz
        array([20.11183771, 20.2163053 , 20.41767549, 20.80399084, 21.53839043,
               22.91063751, 25.3939941 , 29.6384327 , 36.23006369, 45.08430684,
               54.91569316, 63.76993631, 70.3615673 , 74.6060059 , 77.08936249,
               78.46160957, 79.19600916, 79.58232451, 79.7836947 , 79.88816229])
        >>> dz.sum()
        1000.0
        >>> dz[-1] / dz[0]
        3.9721960481753706

        If we want the top layer to be thicker then we need to prescribe ``ratio < 1``.

        >>> from regional_mom6 import hyperbolictan_thickness_profile
        >>> nlayers, total_depth = 20, 1000
        >>> ratio = 1/4
        >>> dz = hyperbolictan_thickness_profile(nlayers, ratio, total_depth)
        >>> dz
        array([79.88816229, 79.7836947 , 79.58232451, 79.19600916, 78.46160957,
               77.08936249, 74.6060059 , 70.3615673 , 63.76993631, 54.91569316,
               45.08430684, 36.23006369, 29.6384327 , 25.3939941 , 22.91063751,
               21.53839043, 20.80399084, 20.41767549, 20.2163053 , 20.11183771])
        >>> dz.sum()
        1000.0
        >>> dz[-1] / dz[0]
        0.25174991059652

        Now how about a grid with the same total depth as above but with equally-spaced
        layers.

        >>> from regional_mom6 import hyperbolictan_thickness_profile
        >>> nlayers, total_depth = 20, 1000
        >>> ratio = 1
        >>> dz = hyperbolictan_thickness_profile(nlayers, ratio, total_depth)
        >>> dz
        array([50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50., 50.,
               50., 50., 50., 50., 50., 50., 50.])
    """

    assert isinstance(nlayers, int), "nlayers must be an integer"

    if nlayers == 1:
        return np.array([float(total_depth)])

    assert ratio > 0, "ratio must be > 0"

    # The hyberbolic tangent profile below implies that the sum of
    # all layer thicknesses is:
    #
    # nlayers * (top_layer_thickness + bottom_layer_thickness) / 2
    #
    # By choosing the top_layer_thickness appropriately we ensure that
    # the sum of all layer thicknesses is the prescribed total_depth.
    top_layer_thickness = 2 * total_depth / (nlayers * (1 + ratio))

    bottom_layer_thickness = ratio * top_layer_thickness

    layer_thicknesses = top_layer_thickness + 0.5 * (
        bottom_layer_thickness - top_layer_thickness
    ) * (1 + np.tanh(2 * np.pi * (np.arange(nlayers) / (nlayers - 1) - 1 / 2)))

    sum_of_thicknesses = np.sum(layer_thicknesses)

    atol = np.finfo(type(sum_of_thicknesses)).eps

    assert np.isclose(total_depth, sum_of_thicknesses, atol=atol)  # just checking ;)

    return layer_thicknesses


def rectangular_hgrid(λ, φ):
    """
    Construct a horizontal grid with all the metadata required by MOM6, based on
    arrays of longitudes (``λ``) and latitudes (``φ``) on the supergrid.
    Here, 'supergrid' refers to both cell edges and centres, meaning that there
    are twice as many points along each axis than for any individual field.

    Caution:
        It is assumed the grid's boundaries are lines of constant latitude and
        longitude. Rotated grids need to be handled differently.

        It is also assumed here that the longitude array values are uniformly spaced.

        Ensure both ``λ`` and ``φ`` are monotonically increasing.

    Args:
        λ (numpy.array): All longitude points on the supergrid. Must be uniformly spaced.
        φ (numpy.array): All latitude points on the supergrid.

    Returns:
        xarray.Dataset: An FMS-compatible horizontal grid (``hgrid``) that includes all required attributes.
    """

    assert np.all(np.diff(λ) > 0), "longitudes array λ must be monotonically increasing"
    assert np.all(np.diff(φ) > 0), "latitudes array φ must be monotonically increasing"

    R = 6371e3  # mean radius of the Earth; https://en.wikipedia.org/wiki/Earth_radius

    # compute longitude spacing and ensure that longitudes are uniformly spaced
    dλ = λ[1] - λ[0]

    assert np.allclose(
        np.diff(λ), dλ * np.ones(np.size(λ) - 1)
    ), "provided array of longitudes must be uniformly spaced"

    # dx = R * cos(np.deg2rad(φ)) * np.deg2rad(dλ) / 2
    # Note: division by 2 because we're on the supergrid
    dx = np.broadcast_to(
        R * np.cos(np.deg2rad(φ)) * np.deg2rad(dλ) / 2,
        (λ.shape[0] - 1, φ.shape[0]),
    ).T

    # dy = R * np.deg2rad(dφ) / 2
    # Note: division by 2 because we're on the supergrid
    dy = np.broadcast_to(R * np.deg2rad(np.diff(φ)) / 2, (λ.shape[0], φ.shape[0] - 1)).T

    lon, lat = np.meshgrid(λ, φ)

    area = quadrilateral_areas(lat, lon, R)

    attrs = {
        "tile": {
            "standard_name": "grid_tile_spec",
            "geometry": "spherical",
            "north_pole": "0.0 90.0",
            "discretization": "logically_rectangular",
            "conformal": "true",
        },
        "x": {"standard_name": "geographic_longitude", "units": "degree_east"},
        "y": {"standard_name": "geographic_latitude", "units": "degree_north"},
        "dx": {
            "standard_name": "grid_edge_x_distance",
            "units": "meters",
        },
        "dy": {
            "standard_name": "grid_edge_y_distance",
            "units": "meters",
        },
        "area": {
            "standard_name": "grid_cell_area",
            "units": "m**2",
        },
        "angle_dx": {
            "standard_name": "grid_vertex_x_angle_WRT_geographic_east",
            "units": "degrees_east",
        },
        "arcx": {
            "standard_name": "grid_edge_x_arc_type",
            "north_pole": "0.0 90.0",
        },
    }

    return xr.Dataset(
        {
            "tile": ((), np.array(b"tile1", dtype="|S255"), attrs["tile"]),
            "x": (["nyp", "nxp"], lon, attrs["x"]),
            "y": (["nyp", "nxp"], lat, attrs["y"]),
            "dx": (["nyp", "nx"], dx, attrs["dx"]),
            "dy": (["ny", "nxp"], dy, attrs["dy"]),
            "area": (["ny", "nx"], area, attrs["area"]),
            "angle_dx": (["nyp", "nxp"], lon * 0, attrs["angle_dx"]),
            "arcx": ((), np.array(b"small_circle", dtype="|S255"), attrs["arcx"]),
        }
    )


class experiment:
    """The main class for setting up a regional experiment.

    Everything about the regional experiment.

    Methods in this class generate the various input files needed for a MOM6
    experiment forced with open boundary conditions (OBCs). The code is agnostic
    to the user's choice of boundary forcing, bathymetry, and surface forcing;
    users need to prescribe what variables are all called via mapping dictionaries
    from MOM6 variable/coordinate name to the name in the input dataset.

    The class can be used to generate the grids for a new experiment, or to read in
    an existing one (when ``read_existing_grids=True``; see argument description below).

    Args:
        longitude_extent (Tuple[float]): Extent of the region in longitude (in degrees). For
            example: ``(40.5, 50.0)``.
        latitude_extent (Tuple[float]): Extent of the region in latitude (in degrees). For
            example: ``(-20.0, 30.0)``.
        date_range (Tuple[str]): Start and end dates of the boundary forcing window. For
            example: ``("2003-01-01", "2003-01-31")``.
        resolution (float): Lateral resolution of the domain (in degrees).
        number_vertical_layers (int): Number of vertical layers.
        layer_thickness_ratio (float): Ratio of largest to smallest layer thickness;
            used as input in :func:`~hyperbolictan_thickness_profile`.
        depth (float): Depth of the domain.
        mom_run_dir (str): Path of the MOM6 control directory.
        mom_input_dir (str): Path of the MOM6 input directory, to receive the forcing files.
        toolpath_dir (str): Path of GFDL's FRE tools (https://github.com/NOAA-GFDL/FRE-NCtools)
            binaries.
        grid_type (Optional[str]): Type of horizontal grid to generate.
            Currently, only ``'even_spacing'`` is supported.
        repeat_year_forcing (Optional[bool]): When ``True`` the experiment runs with
            repeat-year forcing. When ``False`` (default) then inter-annual forcing is used.
        read_existing_grids (Optional[Bool]): When ``True``, instead of generating the grids,
            the grids and the ocean mask are being read from within the ``mom_input_dir`` and
            ``mom_run_dir`` directories. Useful for modifying or troubleshooting experiments.
            Default: ``False``.
    """

    def __init__(
        self,
        *,
        longitude_extent,
        latitude_extent,
        date_range,
        resolution,
        number_vertical_layers,
        layer_thickness_ratio,
        depth,
        mom_run_dir,
        mom_input_dir,
        toolpath_dir,
        grid_type="even_spacing",
        repeat_year_forcing=False,
        read_existing_grids=False,
    ):
        ## in case list was given, convert to tuples
        self.longitude_extent = tuple(longitude_extent)
        self.latitude_extent = tuple(latitude_extent)
        self.date_range = tuple(date_range)

        self.mom_run_dir = Path(mom_run_dir)
        self.mom_input_dir = Path(mom_input_dir)
        self.toolpath_dir = Path(toolpath_dir)

        self.mom_run_dir.mkdir(exist_ok=True)
        self.mom_input_dir.mkdir(exist_ok=True)

        self.date_range = [
            dt.datetime.strptime(date_range[0], "%Y-%m-%d %H:%M:%S"),
            dt.datetime.strptime(date_range[1], "%Y-%m-%d %H:%M:%S"),
        ]
        self.resolution = resolution
        self.number_vertical_layers = number_vertical_layers
        self.layer_thickness_ratio = layer_thickness_ratio
        self.depth = depth
        self.grid_type = grid_type
        self.repeat_year_forcing = repeat_year_forcing
        self.ocean_mask = None
        self.layout = None  # This should be a tuple. Leaving in a dummy 'None' makes it easy to remind the user to provide a value later on.
        if read_existing_grids:
            try:
                self.hgrid = xr.open_dataset(self.mom_input_dir / "hgrid.nc")
                self.vgrid = xr.open_dataset(self.mom_input_dir / "vcoord.nc")
            except:
                print(
                    "Error while reading in existing grids!\n\n"
                    + f"Make sure `hgrid.nc` and `vcoord.nc` exists in {self.mom_input_dir} directory."
                )
                raise ValueError
        else:
            self.hgrid = self._make_hgrid()
            self.vgrid = self._make_vgrid()
        # create additional directories and links
        (self.mom_input_dir / "weights").mkdir(exist_ok=True)
        (self.mom_input_dir / "forcing").mkdir(exist_ok=True)

        run_inputdir = self.mom_run_dir / "inputdir"
        if not run_inputdir.exists():
            run_inputdir.symlink_to(self.mom_input_dir.resolve())
        input_rundir = self.mom_input_dir / "rundir"
        if not input_rundir.exists():
            input_rundir.symlink_to(self.mom_run_dir.resolve())

    def __getattr__(self, name):
        available_methods = [
            method for method in dir(self) if not method.startswith("__")
        ]
        error_message = (
            f"{name} method not found. Available methods are: {available_methods}"
        )
        raise AttributeError(error_message)

    def _make_hgrid(self):
        """
        Set up a horizontal grid based on user's specification of the domain.
        The default behaviour generates a grid evenly spaced both in longitude
        and in latitude.

        The latitudinal resolution is scaled with the cosine of the central
        latitude of the domain, i.e., ``Δφ = cos(φ_central) * Δλ``, where ``Δλ``
        is the longitudinal spacing. This way, for a sufficiently small domain,
        the linear distances between grid points are nearly identical:
        ``Δx = R * cos(φ) * Δλ`` and ``Δy = R * Δφ = R * cos(φ_central) * Δλ``
        (here ``R`` is Earth's radius and ``φ``, ``φ_central``, ``Δλ``, and ``Δφ``
        are all expressed in radians).
        That is, if the domain is small enough that so that ``cos(φ_North_Side)``
        is not much different from ``cos(φ_South_Side)``, then ``Δx`` and ``Δy``
        are similar.

        Note:
            The intention is for the horizontal grid (``hgrid``) generation to be flexible.
            For now, there is only one implemented horizontal grid included in the package,
            but you can customise it by simply overwriting the ``hgrid.nc`` file in the
            ``mom_run_dir`` directory after initialising an ``experiment``. To preserve the
            metadata, it might be easiest to read the file in, then modify the fields before
            re-saving.
        """

        assert (
            self.grid_type == "even_spacing"
        ), "only even_spacing grid type is implemented"

        if self.grid_type == "even_spacing":

            # longitudes are evenly spaced based on resolution and bounds
            nx = int(
                (self.longitude_extent[1] - self.longitude_extent[0])
                / (self.resolution / 2)
            )
            if nx % 2 != 1:
                nx += 1

            λ = np.linspace(
                self.longitude_extent[0], self.longitude_extent[1], nx
            )  # longitudes in degrees

            # Latitudes evenly spaced by dx * cos(central_latitude)
            central_latitude = np.mean(self.latitude_extent)  # degrees
            latitudinal_resolution = self.resolution * np.cos(
                np.deg2rad(central_latitude)
            )

            ny = (
                int(
                    (self.latitude_extent[1] - self.latitude_extent[0])
                    / (latitudinal_resolution / 2)
                )
                + 1
            )

            if ny % 2 != 1:
                ny += 1

            φ = np.linspace(
                self.latitude_extent[0], self.latitude_extent[1], ny
            )  # latitudes in degrees

            hgrid = rectangular_hgrid(λ, φ)
            hgrid.to_netcdf(self.mom_input_dir / "hgrid.nc")

            return hgrid

    def _make_vgrid(self):
        """
        Generates a vertical grid based on the ``number_vertical_layers``, the ratio
        of largest to smallest layer thickness (``layer_thickness_ratio``) and the
        total ``depth`` parameters.
        (All these parameters are specified at the class level.)
        """

        thicknesses = hyperbolictan_thickness_profile(
            self.number_vertical_layers, self.layer_thickness_ratio, self.depth
        )

        zi = np.cumsum(thicknesses)
        zi = np.insert(zi, 0, 0.0)  # add zi = 0.0 as first interface

        zl = zi[0:-1] + thicknesses / 2  # the mid-points between interfaces zi

        vcoord = xr.Dataset({"zi": ("zi", zi), "zl": ("zl", zl)})

        vcoord["zi"].attrs = {"units": "meters"}
        vcoord["zl"].attrs = {"units": "meters"}

        vcoord.to_netcdf(self.mom_input_dir / "vcoord.nc")

        return vcoord

    def initial_condition(
        self,
        raw_ic_path,
        varnames,
        arakawa_grid="A",
        vcoord_type="height",
    ):
        """
        Reads the initial condition from files in ``ic_path``, interpolates to the
        model grid, fixes up metadata, and saves back to the input directory.

        Args:
            raw_ic_path (Union[str, Path]): Path to raw initial condition file to read in.
            varnames (Dict[str, str]): Mapping from MOM6 variable/coordinate names to the names
                in the input dataset. For example, ``{'xq': 'lonq', 'yh': 'lath', 'salt': 'so', ...}``.
            arakawa_grid (Optional[str]): Arakawa grid staggering type of the initial condition.
                Either ``'A'`` (default), ``'B'``, or ``'C'``.
            vcoord_type (Optional[str]): The type of vertical coordinate used in the forcing files.
                Either ``'height'`` or ``'thickness'``.
        """

        # Remove time dimension if present in the IC.
        # Assume that the first time dim is the intended on if more than one is present

        ic_raw = xr.open_dataset(raw_ic_path)
        if varnames["time"] in ic_raw.dims:
            ic_raw = ic_raw.isel({varnames["time"]: 0})
        if varnames["time"] in ic_raw.coords:
            ic_raw = ic_raw.drop(varnames["time"])

        # Separate out tracers from two velocity fields of IC
        try:
            ic_raw_tracers = ic_raw[
                [varnames["tracers"][i] for i in varnames["tracers"]]
            ]
        except:
            raise ValueError(
                "Error in reading in initial condition tracers. Terminating!"
            )
        try:
            ic_raw_u = ic_raw[varnames["u"]]
            ic_raw_v = ic_raw[varnames["v"]]
        except:
            raise ValueError(
                "Error in reading in initial condition tracers. Terminating!"
            )

        try:
            ic_raw_eta = ic_raw[varnames["eta"]]
        except:
            raise ValueError(
                "Error in reading in initial condition tracers. Terminating!"
            )

        ## if min(temperature) > 100 then assume that units must be degrees K
        ## (otherwise we can't be on Earth) and convert to degrees C
        if np.nanmin(ic_raw[varnames["tracers"]["temp"]]) > 100:
            ic_raw[varnames["tracers"]["temp"]] -= 273.15
            ic_raw[varnames["tracers"]["temp"]].attrs["units"] = "degrees Celsius"

        # Rename all coordinates to have 'lon' and 'lat' to work with the xesmf regridder
        if arakawa_grid == "A":
            if (
                "xh" in varnames.keys() and "yh" in varnames.keys()
            ):  ## Handle case where user has provided xh and yh rather than x & y
                # Rename xh with x in dictionary
                varnames["x"] = varnames["xh"]
                varnames["y"] = varnames["yh"]

            if "x" in varnames.keys() and "y" in varnames.keys():
                ic_raw_tracers = ic_raw_tracers.rename(
                    {varnames["x"]: "lon", varnames["y"]: "lat"}
                )
                ic_raw_u = ic_raw_u.rename({varnames["x"]: "lon", varnames["y"]: "lat"})
                ic_raw_v = ic_raw_v.rename({varnames["x"]: "lon", varnames["y"]: "lat"})
                ic_raw_eta = ic_raw_eta.rename(
                    {varnames["x"]: "lon", varnames["y"]: "lat"}
                )
            else:
                raise ValueError(
                    "Can't find required coordinates in initial condition.\n\n"
                    + "Given that arakawa_grid is 'A' the 'x' and 'y' coordinates should be provided"
                    + "in the varnames dictionary. For example, {'x': 'lon', 'y': 'lat'}.\n\n"
                    + "Terminating!"
                )

        if arakawa_grid == "B":
            if (
                "xq" in varnames.keys()
                and "yq" in varnames.keys()
                and "xh" in varnames.keys()
                and "yh" in varnames.keys()
            ):
                ic_raw_tracers = ic_raw_tracers.rename(
                    {varnames["xh"]: "lon", varnames["yh"]: "lat"}
                )
                ic_raw_eta = ic_raw_eta.rename(
                    {varnames["xh"]: "lon", varnames["yh"]: "lat"}
                )
                ic_raw_u = ic_raw_u.rename(
                    {varnames["xq"]: "lon", varnames["yq"]: "lat"}
                )
                ic_raw_v = ic_raw_v.rename(
                    {varnames["xq"]: "lon", varnames["yq"]: "lat"}
                )
            else:
                raise ValueError(
                    "Can't find coordinates in initial condition.\n\n"
                    + "Given that arakawa_grid is 'B' the names of the cell centers ('xh' & 'yh')"
                    + "as well as the cell edges ('xq' & 'yq') coordinates should be provided in "
                    + "the varnames dictionary. For example, {'xh': 'lonh', 'yh': 'lath', ...}.\n\n"
                    + "Terminating!"
                )
        if arakawa_grid == "C":
            if (
                "xq" in varnames.keys()
                and "yq" in varnames.keys()
                and "xh" in varnames.keys()
                and "yh" in varnames.keys()
            ):
                ic_raw_tracers = ic_raw_tracers.rename(
                    {varnames["xh"]: "lon", varnames["yh"]: "lat"}
                )
                ic_raw_eta = ic_raw_eta.rename(
                    {varnames["xh"]: "lon", varnames["yh"]: "lat"}
                )
                ic_raw_u = ic_raw_u.rename(
                    {varnames["xq"]: "lon", varnames["yh"]: "lat"}
                )
                ic_raw_v = ic_raw_v.rename(
                    {varnames["xh"]: "lon", varnames["yq"]: "lat"}
                )
            else:
                raise ValueError(
                    "Can't find coordinates in initial condition.\n\n"
                    + "Given that arakawa_grid is 'C' the names of the cell centers ('xh' & 'yh')"
                    + "as well as the cell edges ('xq' & 'yq') coordinates should be provided in "
                    + "in the varnames dictionary. For example, {'xh': 'lonh', 'yh': 'lath', ...}.\n\n"
                    + "Terminating!"
                )

        ## Construct the xq, yh and xh, yq grids
        ugrid = (
            self.hgrid[["x", "y"]]
            .isel(nxp=slice(None, None, 2), nyp=slice(1, None, 2))
            .rename({"x": "lon", "y": "lat"})
            .set_coords(["lat", "lon"])
        )
        vgrid = (
            self.hgrid[["x", "y"]]
            .isel(nxp=slice(1, None, 2), nyp=slice(None, None, 2))
            .rename({"x": "lon", "y": "lat"})
            .set_coords(["lat", "lon"])
        )

        ## Construct the cell centre grid for tracers (xh, yh).
        tgrid = xr.Dataset(
            {
                "lon": (
                    ["lon"],
                    self.hgrid.x.isel(nxp=slice(1, None, 2), nyp=1).values,
                ),
                "lat": (
                    ["lat"],
                    self.hgrid.y.isel(nxp=1, nyp=slice(1, None, 2)).values,
                ),
            }
        )

        # NaNs might be here from the land mask of the model that the IC has come from.
        # If they're not removed then the coastlines from this other grid will be retained!
        # The land mask comes from the bathymetry file, so we don't need NaNs
        # to tell MOM6 where the land is.
        ic_raw_tracers = (
            ic_raw_tracers.interpolate_na("lon", method="linear")
            .ffill("lon")
            .bfill("lon")
            .ffill("lat")
            .bfill("lat")
            .ffill(varnames["zl"])
        )

        ic_raw_u = (
            ic_raw_u.interpolate_na("lon", method="linear")
            .ffill("lon")
            .bfill("lon")
            .ffill("lat")
            .bfill("lat")
            .ffill(varnames["zl"])
        )

        ic_raw_v = (
            ic_raw_v.interpolate_na("lon", method="linear")
            .ffill("lon")
            .bfill("lon")
            .ffill("lat")
            .bfill("lat")
            .ffill(varnames["zl"])
        )

        ic_raw_eta = (
            ic_raw_eta.interpolate_na("lon", method="linear")
            .ffill("lon")
            .bfill("lon")
            .ffill("lat")
            .bfill("lat")
        )

        ## Make our three horizontal regridders
        regridder_u = xe.Regridder(
            ic_raw_u,
            ugrid,
            "bilinear",
        )
        regridder_v = xe.Regridder(
            ic_raw_v,
            vgrid,
            "bilinear",
        )

        regridder_t = xe.Regridder(
            ic_raw_tracers,
            tgrid,
            "bilinear",
        )

        print("INITIAL CONDITIONS")

        ## Regrid all fields horizontally.

        print("Regridding Velocities... ", end="")

        vel_out = xr.merge(
            [
                regridder_u(ic_raw_u)
                .rename({"lon": "xq", "lat": "yh", "nyp": "ny", varnames["zl"]: "zl"})
                .rename("u"),
                regridder_v(ic_raw_v)
                .rename({"lon": "xh", "lat": "yq", "nxp": "nx", varnames["zl"]: "zl"})
                .rename("v"),
            ]
        )

        print("Done.\nRegridding Tracers... ", end="")

        tracers_out = xr.merge(
            [
                regridder_t(ic_raw_tracers[varnames["tracers"][i]]).rename(i)
                for i in varnames["tracers"]
            ]
        ).rename({"lon": "xh", "lat": "yh", varnames["zl"]: "zl"})

        print("Done.\nRegridding Free surface... ", end="")

        eta_out = (
            regridder_t(ic_raw_eta).rename({"lon": "xh", "lat": "yh"}).rename("eta_t")
        )  ## eta_t is the name set in MOM_input by default
        print("Done.")

        ## Return attributes to arrays

        vel_out.u.attrs = ic_raw_u.attrs
        vel_out.v.attrs = ic_raw_v.attrs
        vel_out.xq.attrs = ic_raw_u.lon.attrs
        vel_out.yq.attrs = ic_raw_v.lat.attrs
        vel_out.yh.attrs = ic_raw_u.lat.attrs
        vel_out.yh.attrs = ic_raw_v.lon.attrs
        vel_out.zl.attrs = ic_raw_u[varnames["zl"]].attrs

        tracers_out.xh.attrs = ic_raw_tracers.lon.attrs
        tracers_out.yh.attrs = ic_raw_tracers.lat.attrs
        tracers_out.zl.attrs = ic_raw_tracers[varnames["zl"]].attrs
        for i in varnames["tracers"]:
            tracers_out[i].attrs = ic_raw_tracers[varnames["tracers"][i]].attrs

        eta_out.xh.attrs = ic_raw_tracers.lon.attrs
        eta_out.yh.attrs = ic_raw_tracers.lat.attrs
        eta_out.attrs = ic_raw_eta.attrs

        ## Regrid the fields vertically

        if (
            vcoord_type == "thickness"
        ):  ## In this case construct the vertical profile by summing thickness
            tracers_out["zl"] = tracers_out["zl"].diff("zl")
            dz = tracers_out[self.z].diff(self.z)
            dz.name = "dz"
            dz = xr.concat([dz, dz[-1]], dim=self.z)

        tracers_out = tracers_out.interp({"zl": self.vgrid.zl.values})
        vel_out = vel_out.interp({"zl": self.vgrid.zl.values})

        print("Saving outputs... ", end="")

        vel_out.fillna(0).to_netcdf(
            self.mom_input_dir / "forcing/init_vel.nc",
            mode="w",
            encoding={
                "u": {"_FillValue": netCDF4.default_fillvals["f4"]},
                "v": {"_FillValue": netCDF4.default_fillvals["f4"]},
            },
        )

        tracers_out.to_netcdf(
            self.mom_input_dir / "forcing/init_tracers.nc",
            mode="w",
            encoding={
                "xh": {"_FillValue": None},
                "yh": {"_FillValue": None},
                "zl": {"_FillValue": None},
                "temp": {"_FillValue": -1e20, "missing_value": -1e20},
                "salt": {"_FillValue": -1e20, "missing_value": -1e20},
            },
        )
        eta_out.to_netcdf(
            self.mom_input_dir / "forcing/init_eta.nc",
            mode="w",
            encoding={
                "xh": {"_FillValue": None},
                "yh": {"_FillValue": None},
                "eta_t": {"_FillValue": None},
            },
        )

        self.ic_eta = eta_out
        self.ic_tracers = tracers_out
        self.ic_vels = vel_out

        print("done setting up initial condition.")

        return

    def get_glorys_rectangular(
        self, raw_boundaries_path, boundaries=["south", "north", "west", "east"]
    ):
        """
        This function is a wrapper for `get_glorys_data`, calling this function once for each of the rectangular boundary segments and the initial condition. For more complex boundary shapes, call `get_glorys_data` directly for each of your boundaries that aren't parallel to lines of constant latitude or longitude.

        args:
            raw_boundaries_path (str): Path to the directory containing the raw boundary forcing files.
            boundaries (List[str]): List of cardinal directions for which to create boundary forcing files.
                Default is `["south", "north", "west", "east"]`.
        """

        # Initial Condition
        get_glorys_data(
            self.longitude_extent,
            self.latitude_extent,
            [
                self.date_range[0],
                self.date_range[0] + datetime.timedelta(days=1),
            ],
            "ic_unprocessed",
            raw_boundaries_path,
            modify_existing=False,
        )
        if "east" in boundaries:
            get_glorys_data(
                [self.longitude_extent[1], self.longitude_extent[1]],
                [self.latitude_extent[0], self.latitude_extent[1]],
                self.date_range,
                "east_unprocessed",
                raw_boundaries_path,
            )
        if "west" in boundaries:
            get_glorys_data(
                [self.longitude_extent[0], self.longitude_extent[0]],
                [self.latitude_extent[0], self.latitude_extent[1]],
                self.date_range,
                "west_unprocessed",
                raw_boundaries_path,
            )
        if "north" in boundaries:
            get_glorys_data(
                [self.longitude_extent[0], self.longitude_extent[1]],
                [self.latitude_extent[1], self.latitude_extent[1]],
                self.date_range,
                "north_unprocessed",
                raw_boundaries_path,
            )
        if "south" in boundaries:
            get_glorys_data(
                [self.longitude_extent[0], self.longitude_extent[1]],
                [self.latitude_extent[0], self.latitude_extent[0]],
                self.date_range,
                "south_unprocessed",
                raw_boundaries_path,
            )

        print(
            f"script `get_glorys_data.sh` has been greated at {raw_boundaries_path}.\n Run this script via bash to download the data from a terminal with internet access. \nYou will need to enter your Copernicus Marine username and password.\nIf you don't have an account, make one here:\nhttps://data.marine.copernicus.eu/register"
        )
        return

    def rectangular_boundaries(
        self,
        raw_boundaries_path,
        varnames,
        boundaries=["south", "north", "west", "east"],
        arakawa_grid="A",
    ):
        """
        This function is a wrapper for `simple_boundary`. Given a list of up to four cardinal directions,
        it creates a boundary forcing file for each one. Ensure that the raw boundaries are all saved in the same directory,
        and that they are named using the format `east_unprocessed.nc`

        Args:
            raw_boundaries_path (str): Path to the directory containing the raw boundary forcing files.
            varnames (Dict[str, str]): Mapping from MOM6 variable/coordinate names to the name in the
                input dataset.
            boundaries (List[str]): List of cardinal directions for which to create boundary forcing files.
                Default is `["south", "north", "west", "east"]`.
            arakawa_grid (Optional[str]): Arakawa grid staggering type of the boundary forcing.
                Either ``'A'`` (default), ``'B'``, or ``'C'``.
        """
        for i in boundaries:
            if i not in ["south", "north", "west", "east"]:
                raise ValueError(
                    f"Invalid boundary direction: {i}. Must be one of ['south', 'north', 'west', 'east']"
                )

        if len(boundaries) < 4:
            print(
                "NOTE: the 'setup_run_directories' method assumes that you have four boundaries. You'll need to modify the MOM_input file manually to reflect the number of boundaries you have, and their orientations. You should be able to find the relevant section in the MOM_input file by searching for 'segment_'. Ensure that the segment names match those in your inputdir/forcing folder"
            )

        if len(boundaries) > 4:
            raise ValueError(
                "This method only supports up to four boundaries. To set up more complex boundary shapes you can manually call the 'simple_boundary' method for each boundary."
            )
        # Now iterate through our four boundaries
        for i, orientation in enumerate(boundaries, start=1):
            self.simple_boundary(
                Path(raw_boundaries_path) / (orientation + "_unprocessed.nc"),
                varnames,
                orientation,  # The cardinal direction of the boundary
                i,  # A number to identify the boundary; indexes from 1
                arakawa_grid=arakawa_grid,
            )

    def simple_boundary(
        self, path_to_bc, varnames, orientation, segment_number, arakawa_grid="A"
    ):
        """
        Here 'simple' refers to boundaries that are parallel to lines of constant longitude or latitude.
        Set up a boundary forcing file for a given orientation.

        Args:
            path_to_bc (str): Path to boundary forcing file. Ideally this should be a pre cut-out
                netCDF file containing only the boundary region and 3 extra boundary points on either
                side. Users can also provide a large dataset containing their entire domain but this
                will be slower.
            varnames (Dict[str, str]): Mapping from MOM6 variable/coordinate names to the name in the
                input dataset.
            orientation (str): Orientation of boundary forcing file, i.e., ``'east'``, ``'west'``,
                ``'north'``, or ``'south'``.
            segment_number (int): Number the segments according to how they'll be specified in
                the ``MOM_input``.
            arakawa_grid (Optional[str]): Arakawa grid staggering type of the boundary forcing.
                Either ``'A'`` (default), ``'B'``, or ``'C'``.
        """

        print("Processing {} boundary...".format(orientation), end="")
        if not path_to_bc.exists():
            raise FileNotFoundError(
                f"Boundary file not found at {path_to_bc}. Please ensure that the files are named in the format `east_unprocessed.nc`."
            )
        seg = segment(
            hgrid=self.hgrid,
            infile=path_to_bc,  # location of raw boundary
            outfolder=self.mom_input_dir,
            varnames=varnames,
            segment_name="segment_{:03d}".format(segment_number),
            orientation=orientation,  # orienataion
            startdate=self.date_range[0],
            arakawa_grid=arakawa_grid,
            repeat_year_forcing=self.repeat_year_forcing,
        )

        seg.rectangular_brushcut()
        print("Done.")
        return

    def setup_bathymetry(
        self,
        *,
        bathymetry_path,
        longitude_coordinate_name="lon",
        latitude_coordinate_name="lat",
        vertical_coordinate_name="elevation",
        fill_channels=False,
        minimum_layers=3,
        positive_down=False,
        chunks="auto",
    ):
        """
        Cut out and interpolate the chosen bathymetry and then fill inland lakes.

        It's also possible to optionally fill narrow channels (see ``fill_channels``
        below), although narrow channels are less of an issue for models that are
        discretized on an Arakawa C grid, like MOM6.

        Output is saved in the input directory of the experiment.

        Args:
            bathymetry_path (str): Path to the netCDF file with the bathymetry.
            longitude_coordinate_name (Optional[str]): The name of the longitude coordinate in the bathymetry
                dataset at ``bathymetry_path``. For example, for GEBCO bathymetry: ``'lon'`` (default).
            latitude_coordinate_name (Optional[str]): The name of the latitude coordinate in the bathymetry
                dataset at ``bathymetry_path``. For example, for GEBCO bathymetry: ``'lat'`` (default).
            vertical_coordinate_name (Optional[str]): The name of the vertical coordinate in the bathymetry
                dataset at ``bathymetry_path``. For example, for GEBCO bathymetry: ``'elevation'`` (default).
            fill_channels (Optional[bool]): Whether or not to fill in
                diagonal channels. This removes more narrow inlets,
                but can also connect extra islands to land. Default: ``False``.
            minimum_layers (Optional[int]): The minimum depth allowed as an integer
                number of layers. Anything shallower than the ``minimum_layers``
                (as specified by the vertical coordinate file ``vcoord.nc``) is deemed land.
                Default: 3.
            positive_down (Optional[bool]): If ``True``, it assumes that
                bathymetry vertical coordinate is positive down. Default: ``False``.
            chunks (Optional Dict[str, str]): Horizontal chunking scheme for the bathymetry, e.g.,
                ``{"longitude": 100, "latitude": 100}``. Use ``'longitude'`` and ``'latitude'`` rather
                than the actual coordinate names in the input file.
        """

        ## Convert the provided coordinate names into a dictionary mapping to the
        ## coordinate names that MOM6 expects.
        coordinate_names = {
            "xh": longitude_coordinate_name,
            "yh": latitude_coordinate_name,
            "elevation": vertical_coordinate_name,
        }
        if chunks != "auto":
            chunks = {
                coordinate_names["xh"]: chunks["longitude"],
                coordinate_names["yh"]: chunks["latitude"],
            }

        bathymetry = xr.open_dataset(bathymetry_path, chunks=chunks)[
            coordinate_names["elevation"]
        ]

        bathymetry = bathymetry.sel(
            {
                coordinate_names["yh"]: slice(
                    self.latitude_extent[0] - 0.5, self.latitude_extent[1] + 0.5
                )
            }  # 0.5 degree latitude buffer (hardcoded) for regridding
        ).astype("float")

        ## Check if the original bathymetry provided has a longitude extent that goes around the globe
        ## to take care of the longitude seam when we slice out the regional domain.

        horizontal_resolution = (
            bathymetry[coordinate_names["xh"]][1]
            - bathymetry[coordinate_names["xh"]][0]
        )

        horizontal_extent = (
            bathymetry[coordinate_names["xh"]][-1]
            - bathymetry[coordinate_names["xh"]][0]
            + horizontal_resolution
        )

        longitude_buffer = 0.5  # 0.5 degree longitude buffer (hardcoded) for regridding

        if np.isclose(horizontal_extent, 360):
            ## longitude extent that goes around the globe -- use longitude_slicer
            bathymetry = longitude_slicer(
                bathymetry,
                np.array(self.longitude_extent)
                + np.array([-longitude_buffer, longitude_buffer]),
                coordinate_names["xh"],
            )
        else:
            ## otherwise, slice normally
            bathymetry = bathymetry.sel(
                {
                    coordinate_names["xh"]: slice(
                        self.longitude_extent[0] - longitude_buffer,
                        self.longitude_extent[1] + longitude_buffer,
                    )
                }
            )

        bathymetry.attrs["missing_value"] = -1e20  # missing value expected by FRE tools
        bathymetry_output = xr.Dataset({"elevation": bathymetry})
        bathymetry.close()

        bathymetry_output = bathymetry_output.rename(
            {coordinate_names["xh"]: "lon", coordinate_names["yh"]: "lat"}
        )
        bathymetry_output.lon.attrs["units"] = "degrees_east"
        bathymetry_output.lat.attrs["units"] = "degrees_north"
        bathymetry_output.elevation.attrs["_FillValue"] = -1e20
        bathymetry_output.elevation.attrs["units"] = "meters"
        bathymetry_output.elevation.attrs["standard_name"] = (
            "height_above_reference_ellipsoid"
        )
        bathymetry_output.elevation.attrs["long_name"] = (
            "Elevation relative to sea level"
        )
        bathymetry_output.elevation.attrs["coordinates"] = "lon lat"
        bathymetry_output.to_netcdf(
            self.mom_input_dir / "bathymetry_original.nc", mode="w", engine="netcdf4"
        )

        tgrid = xr.Dataset(
            {
                "lon": (
                    ["lon"],
                    self.hgrid.x.isel(nxp=slice(1, None, 2), nyp=1).values,
                ),
                "lat": (
                    ["lat"],
                    self.hgrid.y.isel(nxp=1, nyp=slice(1, None, 2)).values,
                ),
            }
        )
        tgrid = xr.Dataset(
            data_vars={
                "elevation": (
                    ["lat", "lon"],
                    np.zeros(
                        self.hgrid.x.isel(
                            nxp=slice(1, None, 2), nyp=slice(1, None, 2)
                        ).shape
                    ),
                )
            },
            coords={
                "lon": (
                    ["lon"],
                    self.hgrid.x.isel(nxp=slice(1, None, 2), nyp=1).values,
                ),
                "lat": (
                    ["lat"],
                    self.hgrid.y.isel(nxp=1, nyp=slice(1, None, 2)).values,
                ),
            },
        )

        # rewrite chunks to use lat/lon now for use with xesmf
        if chunks != "auto":
            chunks = {
                "lon": chunks[coordinate_names["xh"]],
                "lat": chunks[coordinate_names["yh"]],
            }

        tgrid = tgrid.chunk(chunks)
        tgrid.lon.attrs["units"] = "degrees_east"
        tgrid.lon.attrs["_FillValue"] = 1e20
        tgrid.lat.attrs["units"] = "degrees_north"
        tgrid.lat.attrs["_FillValue"] = 1e20
        tgrid.elevation.attrs["units"] = "meters"
        tgrid.elevation.attrs["coordinates"] = "lon lat"
        tgrid.to_netcdf(
            self.mom_input_dir / "bathymetry_unfinished.nc", mode="w", engine="netcdf4"
        )
        tgrid.close()

        ## Replace subprocess run with regular regridder
        print(
            "Begin regridding bathymetry...\n\n"
            + "If this process hangs it means that the chosen domain might be too big to handle this way. "
            + "After ensuring access to appropriate computational resources, try calling ESMF "
            + "directly from a terminal in the input directory via\n\n"
            + "mpirun ESMF_Regrid -s bathymetry_original.nc -d bathymetry_unfinished.nc -m bilinear --src_var elevation --dst_var elevation --netcdf4 --src_regional --dst_regional\n\n"
            + "For details see https://xesmf.readthedocs.io/en/latest/large_problems_on_HPC.html\n\n"
            + "Afterwards, we run 'tidy_bathymetry' method to skip the expensive interpolation step, and finishing metadata, encoding and cleanup."
        )

        # If we have a domain large enough for chunks, we'll run regridder with parallel=True
        parallel = True
        if len(tgrid.chunks) != 2:
            parallel = False
        print(f"Regridding in parallel: {parallel}")
        bathymetry_output = bathymetry_output.chunk(chunks)
        # return
        regridder = xe.Regridder(
            bathymetry_output, tgrid, "bilinear", parallel=parallel
        )

        bathymetry = regridder(bathymetry_output)
        bathymetry.to_netcdf(
            self.mom_input_dir / "bathymetry_unfinished.nc", mode="w", engine="netcdf4"
        )
        print(
            "Regridding finished. Now calling `tidy_bathymetry` method for some finishing touches..."
        )

        self.tidy_bathymetry(fill_channels, minimum_layers, positive_down)

    def tidy_bathymetry(
        self, fill_channels=False, minimum_layers=3, positive_down=True
    ):
        """
        An auxiliary function for bathymetry used to fix up the metadata and remove inland
        lakes after regridding the bathymetry. Having `tidy_bathymetry` as a separate
        method from :func:`~setup_bathymetry` allows for the regridding to be done separately,
        since regridding can be really expensive for large domains.

        If the bathymetry is already regridded and what is left to be done is fixing the metadata
        or fill in some channels, then call this function directly to read in the existing
        ``bathymetry_unfinished.nc`` file that should be in the input directory.

        Args:
            fill_channels (Optional[bool]): Whether to fill in
                diagonal channels. This removes more narrow inlets,
                but can also connect extra islands to land. Default: ``False``.
            minimum_layers (Optional[int]): The minimum depth allowed
                as an integer number of layers. The default value of ``3``
                layers means that anything shallower than the 3rd
                layer (as specified by the ``vcoord``) is deemed land.
            positive_down (Optional[bool]): If ``True`` (default), assume that
                bathymetry vertical coordinate is positive down.
        """

        ## reopen bathymetry to modify
        print("Reading in regridded bathymetry to fix up metadata...", end="")
        bathymetry = xr.open_dataset(
            self.mom_input_dir / "bathymetry_unfinished.nc", engine="netcdf4"
        )

        ## Ensure correct encoding
        bathymetry = xr.Dataset(
            {"depth": (["ny", "nx"], bathymetry["elevation"].values)}
        )
        bathymetry.attrs["depth"] = "meters"
        bathymetry.attrs["standard_name"] = "bathymetric depth at T-cell centers"
        bathymetry.attrs["coordinates"] = "zi"

        bathymetry.expand_dims("tiles", 0)

        if not positive_down:
            ## Ensure that coordinate is positive down!
            bathymetry["depth"] *= -1

        ## REMOVE INLAND LAKES

        min_depth = self.vgrid.zi[minimum_layers]

        ocean_mask = bathymetry.copy(deep=True).depth.where(
            bathymetry.depth <= min_depth, 1
        )
        land_mask = np.abs(ocean_mask - 1)

        changed = True  ## keeps track of whether solution has converged or not

        forward = True  ## only useful for iterating through diagonal channel removal. Means iteration goes SW -> NE

        while changed == True:
            ## First fill in all lakes.
            ## scipy.ndimage.binary_fill_holes fills holes made of 0's within a field of 1's
            land_mask[:, :] = binary_fill_holes(land_mask.data)
            ## Get the ocean mask instead of land- easier to remove channels this way
            ocean_mask = np.abs(land_mask - 1)

            ## Now fill in all one-cell-wide channels
            newmask = xr.where(
                ocean_mask * (land_mask.shift(nx=1) + land_mask.shift(nx=-1)) == 2, 1, 0
            )
            newmask += xr.where(
                ocean_mask * (land_mask.shift(ny=1) + land_mask.shift(ny=-1)) == 2, 1, 0
            )

            if fill_channels == True:
                ## fill in all one-cell-wide horizontal channels
                newmask = xr.where(
                    ocean_mask * (land_mask.shift(nx=1) + land_mask.shift(nx=-1)) == 2,
                    1,
                    0,
                )
                newmask += xr.where(
                    ocean_mask * (land_mask.shift(ny=1) + land_mask.shift(ny=-1)) == 2,
                    1,
                    0,
                )
                ## Diagonal channels
                if forward == True:
                    ## horizontal channels
                    newmask += xr.where(
                        (ocean_mask * ocean_mask.shift(nx=1))
                        * (
                            land_mask.shift({"nx": 1, "ny": 1})
                            + land_mask.shift({"ny": -1})
                        )
                        == 2,
                        1,
                        0,
                    )  ## up right & below
                    newmask += xr.where(
                        (ocean_mask * ocean_mask.shift(nx=1))
                        * (
                            land_mask.shift({"nx": 1, "ny": -1})
                            + land_mask.shift({"ny": 1})
                        )
                        == 2,
                        1,
                        0,
                    )  ## down right & above
                    ## Vertical channels
                    newmask += xr.where(
                        (ocean_mask * ocean_mask.shift(ny=1))
                        * (
                            land_mask.shift({"nx": 1, "ny": 1})
                            + land_mask.shift({"nx": -1})
                        )
                        == 2,
                        1,
                        0,
                    )  ## up right & left
                    newmask += xr.where(
                        (ocean_mask * ocean_mask.shift(ny=1))
                        * (
                            land_mask.shift({"nx": -1, "ny": 1})
                            + land_mask.shift({"nx": 1})
                        )
                        == 2,
                        1,
                        0,
                    )  ## up left & right

                    forward = False

                if forward == False:
                    ## Horizontal channels
                    newmask += xr.where(
                        (ocean_mask * ocean_mask.shift(nx=-1))
                        * (
                            land_mask.shift({"nx": -1, "ny": 1})
                            + land_mask.shift({"ny": -1})
                        )
                        == 2,
                        1,
                        0,
                    )  ## up left & below
                    newmask += xr.where(
                        (ocean_mask * ocean_mask.shift(nx=-1))
                        * (
                            land_mask.shift({"nx": -1, "ny": -1})
                            + land_mask.shift({"ny": 1})
                        )
                        == 2,
                        1,
                        0,
                    )  ## down left & above
                    ## Vertical channels
                    newmask += xr.where(
                        (ocean_mask * ocean_mask.shift(ny=-1))
                        * (
                            land_mask.shift({"nx": 1, "ny": -1})
                            + land_mask.shift({"nx": -1})
                        )
                        == 2,
                        1,
                        0,
                    )  ## down right & left
                    newmask += xr.where(
                        (ocean_mask * ocean_mask.shift(ny=-1))
                        * (
                            land_mask.shift({"nx": -1, "ny": -1})
                            + land_mask.shift({"nx": 1})
                        )
                        == 2,
                        1,
                        0,
                    )  ## down left & right

                    forward = True

            newmask = xr.where(newmask > 0, 1, 0)
            changed = np.max(newmask) == 1
            land_mask += newmask

        self.ocean_mask = np.abs(land_mask - 1)

        bathymetry["depth"] *= self.ocean_mask

        bathymetry["depth"] = bathymetry["depth"].where(
            bathymetry["depth"] != 0, np.nan
        )

        bathymetry.expand_dims({"ntiles": 1}).to_netcdf(
            self.mom_input_dir / "bathymetry.nc",
            mode="w",
            encoding={"depth": {"_FillValue": None}},
        )

        print("done.")
        self.bathymetry = bathymetry

    def FRE_tools(self, layout=None):
        """A wrapper for FRE Tools ``check_mask``, ``make_solo_mosaic``, and ``make_quick_mosaic``.
        User provides processor ``layout`` tuple of processing units.
        """

        print(
            "Running GFDL's FRE Tools. The following information is all printed by the FRE tools themselves"
        )
        if not (self.mom_input_dir / "bathymetry.nc").exists():
            print("No bathymetry file! Need to run setup_bathymetry method first")
            return

        for p in self.mom_input_dir.glob("mask_table*"):
            p.unlink()

        print(
            "OUTPUT FROM MAKE SOLO MOSAIC:",
            subprocess.run(
                str(self.toolpath_dir / "make_solo_mosaic/make_solo_mosaic")
                + " --num_tiles 1 --dir . --mosaic_name ocean_mosaic --tile_file hgrid.nc",
                shell=True,
                cwd=self.mom_input_dir,
            ),
            sep="\n\n",
        )

        print(
            "OUTPUT FROM QUICK MOSAIC:",
            subprocess.run(
                str(self.toolpath_dir / "make_quick_mosaic/make_quick_mosaic")
                + " --input_mosaic ocean_mosaic.nc --mosaic_name grid_spec --ocean_topog bathymetry.nc",
                shell=True,
                cwd=self.mom_input_dir,
            ),
            sep="\n\n",
        )

        if layout != None:
            self.cpu_layout(layout)

    def cpu_layout(self, layout):
        """
        Wrapper for the ``check_mask`` function of GFDL's FRE Tools. User provides processor
        ``layout`` tuple of processing units.
        """

        print(
            "OUTPUT FROM CHECK MASK:\n\n",
            subprocess.run(
                str(self.toolpath_dir / "check_mask/check_mask")
                + f" --grid_file ocean_mosaic.nc --ocean_topog bathymetry.nc --layout {layout[0]},{layout[1]} --halo 4",
                shell=True,
                cwd=self.mom_input_dir,
            ),
        )
        self.layout = layout
        return

    def setup_run_directory(
        self,
        surface_forcing=None,
        using_payu=False,
        overwrite=False,
    ):
        """
        Set up the run directory for MOM6. Either copy a pre-made set of files, or modify
        existing files in the 'rundir' directory for the experiment.

        Args:
            surface_forcing (Optional[str]): Specify the choice of surface forcing, one
                of: ``'jra'`` or ``'era5'``. If not prescribed then constant fluxes are used.
            using_payu (Optional[bool]): Whether or not to use payu (https://github.com/payu-org/payu)
                to run the model. If ``True``, a payu configuration file will be created.
                Default: ``False``.
            overwrite (Optional[bool]): Whether or not to overwrite existing files in the
                run directory. If ``False`` (default), will only modify the ``MOM_layout`` file and will
                not re-copy across the rest of the default files.
        """

        ## Get the path to the regional_mom package on this computer
        premade_rundir_path = Path(
            importlib.resources.files("regional_mom6") / "demos/premade_run_directories"
        )
        if not premade_rundir_path.exists():
            print("Could not find premade run directories at ", premade_rundir_path)
            print(
                "Perhaps the package was imported directly rather than installed with conda. Checking if this is the case... "
            )

            premade_rundir_path = Path(
                importlib.resources.files("regional_mom6").parent
                / "demos/premade_run_directories"
            )
            if not premade_rundir_path.exists():
                raise ValueError(
                    f"Cannot find the premade run directory files at {premade_rundir_path} either.\n\n"
                    + "There may be an issue with package installation. Check that the `premade_run_directory` folder is present in one of these two locations"
                )

        # Define the locations of the directories we'll copy files across from. Base contains most of the files, and overwrite replaces files in the base directory.
        base_run_dir = premade_rundir_path / "common_files"
        if not premade_rundir_path.exists():
            raise ValueError(
                f"Cannot find the premade run directory files at {premade_rundir_path}.\n\n"
                + "These files missing might be indicating an error during the package installation!"
            )
        if surface_forcing:
            overwrite_run_dir = premade_rundir_path / f"{surface_forcing}_surface"
            if not overwrite_run_dir.exists():
                available = [x for x in premade_rundir_path.iterdir() if x.is_dir()]
                raise ValueError(
                    f"Surface forcing {surface_forcing} not available. Please choose from {str(available)}"  ##Here print all available run directories
                )
        else:
            ## In case there is additional forcing (e.g., tides) then we need to modify the run dir to include the additional forcing.
            overwrite_run_dir = False

        # 3 different cases to handle:
        #   1. User is creating a new run directory from scratch. Here we copy across all files and modify.
        #   2. User has already created a run directory, and wants to modify it. Here we only modify the MOM_layout file.
        #   3. User has already created a run directory, and wants to overwrite it. Here we copy across all files and modify. This requires overwrite = True

        if not overwrite:
            for file in base_run_dir.glob(
                "*"
            ):  ## copy each file individually if it doesn't already exist OR overwrite = True
                if not os.path.exists(self.mom_run_dir / file.name):
                    ## Check whether this file exists in an override directory or not
                    if (
                        overwrite_run_dir != False
                        and (overwrite_run_dir / file.name).exists()
                    ):
                        shutil.copy(overwrite_run_dir / file.name, self.mom_run_dir)
                    else:
                        shutil.copy(base_run_dir / file.name, self.mom_run_dir)
        else:
            shutil.copytree(base_run_dir, self.mom_run_dir, dirs_exist_ok=True)
            if overwrite_run_dir != False:
                shutil.copy(base_run_dir / file, self.mom_run_dir)

        ## Make symlinks between run and input directories
        inputdir_in_rundir = self.mom_run_dir / "inputdir"
        rundir_in_inputdir = self.mom_input_dir / "rundir"

        inputdir_in_rundir.unlink(missing_ok=True)
        inputdir_in_rundir.symlink_to(self.mom_input_dir)

        rundir_in_inputdir.unlink(missing_ok=True)
        rundir_in_inputdir.symlink_to(self.mom_run_dir)

        ## Get mask table information
        mask_table = None
        for p in self.mom_input_dir.glob("mask_table.*"):
            if mask_table != None:
                print(
                    f"WARNING: Multiple mask tables found. Defaulting to {mask_table}. If this is not what you want, remove it from the run directory and try again."
                )
                break

            _, masked, layout = p.name.split(".")
            mask_table = p.name
            x, y = (int(v) for v in layout.split("x"))
            ncpus = (x * y) - int(masked)
            layout = (
                x,
                y,
            )  # This is a local variable keeping track of the layout as read from the mask table. Not to be confused with self.layout which is unchanged and may differ.

            print(
                f"Mask table {p.name} read. Using this to infer the cpu layout {layout}, total masked out cells {masked}, and total number of CPUs {ncpus}."
            )

        if mask_table == None:
            if self.layout == None:
                raise AttributeError(
                    "No mask table found, and the cpu layout has not been set. At least one of these is requiret to set up the experiment."
                )
            print(
                f"No mask table found, but the cpu layout has been set to {self.layout} This suggests the domain is mostly water, so there are "
                + "no `non compute` cells that are entirely land. If this doesn't seem right, "
                + "ensure you've already run the `FRE_tools` method which sets up the cpu mask table. Keep an eye on any errors that might print while"
                + "the FRE tools (which run C++ in the background) are running."
            )
            # Here we define a local copy of the layout just for use within this function.
            # This prevents the layout from being overwritten in the main class in case
            # in case the user accidentally loads in the wrong mask table.
            layout = self.layout
            ncpus = layout[0] * layout[1]

        print("Number of CPUs required: ", ncpus)

        ## Modify the input namelists to give the correct layouts
        # TODO Re-implement with package that works for this file type? or at least tidy up code
        with open(self.mom_run_dir / "MOM_layout", "r") as file:
            lines = file.readlines()
            for jj in range(len(lines)):
                if "MASKTABLE" in lines[jj]:
                    if mask_table != None:
                        lines[jj] = f'MASKTABLE = "{mask_table}"\n'
                    else:
                        lines[jj] = "# MASKTABLE = no mask table"
                if "LAYOUT =" in lines[jj] and "IO" not in lines[jj]:
                    lines[jj] = f"LAYOUT = {layout[1]},{layout[0]}\n"

                if "NIGLOBAL" in lines[jj]:
                    lines[jj] = f"NIGLOBAL = {self.hgrid.nx.shape[0]//2}\n"

                if "NJGLOBAL" in lines[jj]:
                    lines[jj] = f"NJGLOBAL = {self.hgrid.ny.shape[0]//2}\n"

        with open(self.mom_run_dir / "MOM_layout", "w") as f:
            f.writelines(lines)

        ## If using payu to run the model, create a payu configuration file
        if not using_payu and os.path.exists(f"{self.mom_run_dir}/config.yaml"):
            os.remove(f"{self.mom_run_dir}/config.yaml")

        else:
            with open(f"{self.mom_run_dir}/config.yaml", "r") as file:
                lines = file.readlines()

                inputfile = open(f"{self.mom_run_dir}/config.yaml", "r")
                lines = inputfile.readlines()
                inputfile.close()
                for i in range(len(lines)):
                    if "ncpus" in lines[i]:
                        lines[i] = f"ncpus: {str(ncpus)}\n"
                    if "jobname" in lines[i]:
                        lines[i] = f"jobname: mom6_{self.mom_input_dir.name}\n"

                    if "input:" in lines[i]:
                        lines[i + 1] = f"    - {self.mom_input_dir}\n"

            with open(f"{self.mom_run_dir}/config.yaml", "w") as file:
                file.writelines(lines)

        # Modify input.nml
        nml = f90nml.read(self.mom_run_dir / "input.nml")
        nml["coupler_nml"]["current_date"] = [
            self.date_range[0].year,
            self.date_range[0].month,
            self.date_range[0].day,
            0,
            0,
            0,
        ]
        nml.write(self.mom_run_dir / "input.nml", force=True)

    def setup_era5(self, era5_path):
        """
        Setup the ERA5 forcing files for the experiment. This assumes that
        all of the ERA5 data in the prescribed date range are downloaded.
        We need the following fields: "2t", "10u", "10v", "sp", "2d", "msdwswrf",
        "msdwlwrf", "lsrr", and "crr".

        Args:
            era5_path (str): Path to the ERA5 forcing files. Specifically, the single-level
                reanalysis product. For example, ``'SOMEPATH/era5/single-levels/reanalysis'``
        """

        ## Firstly just open all raw data
        rawdata = {}
        for fname, vname in zip(
            ["2t", "10u", "10v", "sp", "2d", "msdwswrf", "msdwlwrf", "lsrr", "crr"],
            ["t2m", "u10", "v10", "sp", "d2m", "msdwswrf", "msdwlwrf", "lsrr", "crr"],
        ):
            ## Load data from all relevant years
            years = [
                i for i in range(self.date_range[0].year, self.date_range[1].year + 1)
            ]
            # construct a list of all paths for all years to use for open_mfdataset
            paths_per_year = [Path(f"{era5_path}/{fname}/{year}/") for year in years]
            all_files = []
            for path in paths_per_year:
                # Use glob to find all files that match the pattern
                files = list(path.glob(f"{fname}*.nc"))
                # Add the files to the all_files list
                all_files.extend(files)

            ds = xr.open_mfdataset(
                all_files,
                decode_times=False,
                chunks={"longitude": 100, "latitude": 100},
            )

            ## Cut out this variable to our domain size
            rawdata[fname] = longitude_slicer(
                ds,
                self.longitude_extent,
                "longitude",
            ).sel(
                latitude=slice(
                    self.latitude_extent[1], self.latitude_extent[0]
                )  ## This is because ERA5 has latitude in decreasing order (??)
            )

            ## Now fix up the latitude and time dimensions

            rawdata[fname] = (
                rawdata[fname]
                .isel(latitude=slice(None, None, -1))  ## Flip latitude
                .assign_coords(
                    time=np.arange(
                        0, rawdata[fname].time.shape[0], dtype=float
                    )  ## Set the zero date of forcing to start of run
                )
            )

            rawdata[fname].time.attrs = {
                "calendar": "julian",
                "units": f"hours since {self.date_range[0].strftime('%Y-%m-%d %H:%M:%S')}",
            }  ## Fix up calendar to match

            if fname == "2d":
                ## Calculate specific humidity from dewpoint temperature
                dewpoint = 8.07131 - 1730.63 / (233.426 + rawdata["2d"]["d2m"] - 273.15)
                humidity = (0.622 / rawdata["sp"]["sp"]) * (10**dewpoint) * 101325 / 760
                q = xr.Dataset(data_vars={"q": humidity})

                q.q.attrs = {"long_name": "Specific Humidity", "units": "kg/kg"}
                q.to_netcdf(
                    f"{self.mom_input_dir}/forcing/q_ERA5.nc",
                    unlimited_dims="time",
                    encoding={"q": {"dtype": "double"}},
                )
            elif fname == "crr":
                ## Calculate total rain rate from convective and total
                trr = xr.Dataset(
                    data_vars={"trr": rawdata["crr"]["crr"] + rawdata["lsrr"]["lsrr"]}
                )

                trr.trr.attrs = {
                    "long_name": "Total Rain Rate",
                    "units": "kg m**-2 s**-1",
                }
                trr.to_netcdf(
                    f"{self.mom_input_dir}/forcing/trr_ERA5.nc",
                    unlimited_dims="time",
                    encoding={"trr": {"dtype": "double"}},
                )

            elif fname == "lsrr":
                ## This is handled by crr as both are added together to calculate total rain rate.
                pass
            else:
                rawdata[fname].to_netcdf(
                    f"{self.mom_input_dir}/forcing/{fname}_ERA5.nc",
                    unlimited_dims="time",
                    encoding={vname: {"dtype": "double"}},
                )


class segment:
    """
    Class to turn raw boundary segment data into MOM6 boundary
    segments.

    Boundary segments should only contain the necessary data for that
    segment. No horizontal chunking is done here, so big fat segments
    will process slowly.

    Data should be at daily temporal resolution, iterating upwards
    from the provided startdate. Function ignores the time metadata
    and puts it on Julian calendar.

    Note:
        Only supports z-star (z*) vertical coordinate.

    Args:
        hgrid (xarray.Dataset): The horizontal grid used for domain.
        infile (Union[str, Path]): Path to the raw, unprocessed boundary segment.
        outfolder (Union[str, Path]): Path to folder where the model inputs will
            be stored.
        varnames (Dict[str, str]): Mapping between the variable/dimension names and
            standard naming convention of this pipeline, e.g., ``{"xq": "longitude,
            "yh": "latitude", "salt": "salinity", ...}``. Key "tracers" points to nested
            dictionary of tracers to include in boundary.
        segment_name (str): Name of the segment, e.g., ``'segment_001'``.
        orientation (str): Cardinal direction (lowercase) of the boundary segment,
            i.e., ``'east'``, ``'west'``, ``'north'``, or ``'south'``.
        startdate (str): The starting date to use in the segment calendar.
        arakawa_grid (Optional[str]): Arakawa grid staggering type of the boundary forcing.
                Either ``'A'`` (default), ``'B'``, or ``'C'``.
        time_units (str): The units used by the raw forcing files, e.g., ``hours``,
            ``days`` (default).
        tidal_constituents (Optional[int]): An integer determining the number of tidal
            constituents to be included from the list: *M*:sub:`2`, *S*:sub:`2`, *N*:sub:`2`,
            *K*:sub:`2`, *K*:sub:`1`, *O*:sub:`2`, *P*:sub:`1`, *Q*:sub:`1`, *Mm*,
            *Mf*, and *M*:sub:`4`. For example, specifying ``1`` only includes *M*:sub:`2`;
            specifying ``2`` includes *M*:sub:`2` and *S*:sub:`2`, etc. Default: ``None``.
        repeat_year_forcing (Optional[bool]): When ``True`` the experiment runs with repeat-year
            forcing. When ``False`` (default) then inter-annual forcing is used.
    """

    def __init__(
        self,
        *,
        hgrid,
        infile,
        outfolder,
        varnames,
        segment_name,
        orientation,
        startdate,
        arakawa_grid="A",
        time_units="days",
        tidal_constituents=None,
        repeat_year_forcing=False,
    ):
        ## Store coordinate names
        if arakawa_grid == "A":
            self.x = varnames["x"]
            self.y = varnames["y"]

        elif arakawa_grid in ("B", "C"):
            self.xq = varnames["xq"]
            self.xh = varnames["xh"]
            self.yq = varnames["yq"]
            self.yh = varnames["yh"]

        ## Store velocity names
        self.u = varnames["u"]
        self.v = varnames["v"]
        self.z = varnames["zl"]
        self.eta = varnames["eta"]
        self.time = varnames["time"]
        self.startdate = startdate

        ## Store tracer names
        self.tracers = varnames["tracers"]
        self.time_units = time_units

        ## Store other data
        orientation = orientation.lower()
        if orientation not in ("north", "south", "east", "west"):
            raise ValueError(
                "orientation must be one of: 'north', 'south', 'east', or 'west'"
            )
        self.orientation = orientation

        if arakawa_grid not in ("A", "B", "C"):
            raise ValueError("arakawa_grid must be one of: 'A', 'B', or 'C'")
        self.arakawa_grid = arakawa_grid

        self.infile = infile
        self.outfolder = outfolder
        self.hgrid = hgrid
        self.segment_name = segment_name
        self.tidal_constituents = tidal_constituents
        self.repeat_year_forcing = repeat_year_forcing

    def rectangular_brushcut(self):
        """
        Cut out and interpolate tracers. ``rectangular_brushcut`` assumes that the boundary
        is a simple Northern, Southern, Eastern, or Western boundary.
        """
        if self.orientation == "north":
            self.hgrid_seg = self.hgrid.isel(nyp=[-1])
            self.perpendicular = "ny"
            self.parallel = "nx"

        if self.orientation == "south":
            self.hgrid_seg = self.hgrid.isel(nyp=[0])
            self.perpendicular = "ny"
            self.parallel = "nx"

        if self.orientation == "east":
            self.hgrid_seg = self.hgrid.isel(nxp=[-1])
            self.perpendicular = "nx"
            self.parallel = "ny"

        if self.orientation == "west":
            self.hgrid_seg = self.hgrid.isel(nxp=[0])
            self.perpendicular = "nx"
            self.parallel = "ny"

        ## Need to keep track of which axis the 'main' coordinate corresponds to for later on when re-adding the 'secondary' axis
        if self.perpendicular == "ny":
            self.axis_to_expand = 2
        else:
            self.axis_to_expand = 3

        ## Grid for interpolating our fields
        self.interp_grid = xr.Dataset(
            {
                "lat": (
                    [f"{self.parallel}_{self.segment_name}"],
                    self.hgrid_seg.y.squeeze().data,
                ),
                "lon": (
                    [f"{self.parallel}_{self.segment_name}"],
                    self.hgrid_seg.x.squeeze().data,
                ),
            }
        ).set_coords(["lat", "lon"])

        rawseg = xr.open_dataset(self.infile, decode_times=False, engine="netcdf4")

        if self.arakawa_grid == "A":
            rawseg = rawseg.rename({self.x: "lon", self.y: "lat"})
            ## In this case velocities and tracers all on same points
            regridder = xe.Regridder(
                rawseg[self.u],
                self.interp_grid,
                "bilinear",
                locstream_out=True,
                reuse_weights=False,
                filename=self.outfolder
                / f"weights/bilinear_velocity_weights_{self.orientation}.nc",
            )

            segment_out = xr.merge(
                [
                    regridder(
                        rawseg[
                            [self.u, self.v, self.eta]
                            + [self.tracers[i] for i in self.tracers]
                        ]
                    )
                ]
            )

        if self.arakawa_grid == "B":
            ## All tracers on one grid, all velocities on another
            regridder_velocity = xe.Regridder(
                rawseg[self.u].rename({self.xq: "lon", self.yq: "lat"}),
                self.interp_grid,
                "bilinear",
                locstream_out=True,
                reuse_weights=False,
                filename=self.outfolder
                / f"weights/bilinear_velocity_weights_{self.orientation}.nc",
            )

            regridder_tracer = xe.Regridder(
                rawseg[self.tracers["salt"]].rename({self.xh: "lon", self.yh: "lat"}),
                self.interp_grid,
                "bilinear",
                locstream_out=True,
                reuse_weights=False,
                filename=self.outfolder
                / f"weights/bilinear_tracer_weights_{self.orientation}.nc",
            )

            segment_out = xr.merge(
                [
                    regridder_velocity(
                        rawseg[[self.u, self.v]].rename(
                            {self.xq: "lon", self.yq: "lat"}
                        )
                    ),
                    regridder_tracer(
                        rawseg[
                            [self.eta] + [self.tracers[i] for i in self.tracers]
                        ].rename({self.xh: "lon", self.yh: "lat"})
                    ),
                ]
            )

        if self.arakawa_grid == "C":
            ## All tracers on one grid, all velocities on another
            regridder_uvelocity = xe.Regridder(
                rawseg[self.u].rename({self.xq: "lon", self.yh: "lat"}),
                self.interp_grid,
                "bilinear",
                locstream_out=True,
                reuse_weights=False,
                filename=self.outfolder
                / f"weights/bilinear_uvelocity_weights_{self.orientation}.nc",
            )

            regridder_vvelocity = xe.Regridder(
                rawseg[self.v].rename({self.xh: "lon", self.yq: "lat"}),
                self.interp_grid,
                "bilinear",
                locstream_out=True,
                reuse_weights=False,
                filename=self.outfolder
                / f"weights/bilinear_vvelocity_weights_{self.orientation}.nc",
            )

            regridder_tracer = xe.Regridder(
                rawseg[self.tracers["salt"]].rename({self.xh: "lon", self.yh: "lat"}),
                self.interp_grid,
                "bilinear",
                locstream_out=True,
                reuse_weights=False,
                filename=self.outfolder
                / f"weights/bilinear_tracer_weights_{self.orientation}.nc",
            )

            segment_out = xr.merge(
                [
                    regridder_vvelocity(rawseg[[self.v]]),
                    regridder_uvelocity(rawseg[[self.u]]),
                    regridder_tracer(
                        rawseg[[self.eta] + [self.tracers[i] for i in self.tracers]]
                    ),
                ]
            )

        ## segment out now contains our interpolated boundary.
        ## Now, we need to fix up all the metadata and save

        del segment_out["lon"]
        del segment_out["lat"]
        ## Convert temperatures to celsius # use pint
        if (
            np.nanmin(segment_out[self.tracers["temp"]].isel({self.time: 0, self.z: 0}))
            > 100
        ):
            segment_out[self.tracers["temp"]] -= 273.15
            segment_out[self.tracers["temp"]].attrs["units"] = "degrees Celsius"

        # fill in NaNs
        segment_out = (
            segment_out.ffill(self.z)
            .interpolate_na(f"{self.parallel}_{self.segment_name}")
            .ffill(f"{self.parallel}_{self.segment_name}")
            .bfill(f"{self.parallel}_{self.segment_name}")
        )

        time = np.arange(
            0,  #! Indexing everything from start of experiment = simple but maybe counterintutive?
            segment_out[self.time].shape[
                0
            ],  ## Time is indexed from start date of window
            dtype=float,
        )

        segment_out = segment_out.assign_coords({"time": time})
        segment_out.time.attrs = {
            "calendar": "julian",
            "units": f"{self.time_units} since {self.startdate}",
        }
        # Dictionary we built for encoding the netcdf at end
        encoding_dict = {
            "time": {
                "dtype": "double",
            },
            f"nx_{self.segment_name}": {
                "dtype": "int32",
            },
            f"ny_{self.segment_name}": {
                "dtype": "int32",
            },
        }

        ### Generate the dz variable; needs to be in layer thicknesses
        dz = segment_out[self.z].diff(self.z)
        dz.name = "dz"
        dz = xr.concat([dz, dz[-1]], dim=self.z)

        # Here, keep in mind that 'var' keeps track of the mom6 variable names we want, and self.tracers[var]
        # will return the name of the variable from the original data

        allfields = {
            **self.tracers,
            "u": self.u,
            "v": self.v,
        }  ## Combine all fields into one flattened dictionary to iterate over as we fix metadata

        for (
            var
        ) in (
            allfields
        ):  ## Replace with more generic list of tracer variables that might be included?
            v = f"{var}_{self.segment_name}"
            ## Rename each variable in dataset
            segment_out = segment_out.rename({allfields[var]: v})

            ## Rename vertical coordinate for this variable
            segment_out[f"{var}_{self.segment_name}"] = segment_out[
                f"{var}_{self.segment_name}"
            ].rename({self.z: f"nz_{self.segment_name}_{var}"})

            ## Replace the old depth coordinates with incremental integers
            segment_out[f"nz_{self.segment_name}_{var}"] = np.arange(
                segment_out[f"nz_{self.segment_name}_{var}"].size
            )

            ## Re-add the secondary dimension (even though it represents one value..)
            segment_out[v] = segment_out[v].expand_dims(
                f"{self.perpendicular}_{self.segment_name}", axis=self.axis_to_expand
            )

            ## Add the layer thicknesses
            segment_out[f"dz_{v}"] = (
                [
                    "time",
                    f"nz_{v}",
                    f"ny_{self.segment_name}",
                    f"nx_{self.segment_name}",
                ],
                da.broadcast_to(
                    dz.data[None, :, None, None],
                    segment_out[v].shape,
                    chunks=(
                        1,
                        None,
                        None,
                        None,
                    ),  ## Chunk in each time, and every 5 vertical layers
                ),
            )

            encoding_dict[v] = {
                "_FillValue": netCDF4.default_fillvals["f8"],
                "zlib": True,
                # "chunksizes": tuple(s),
            }
            encoding_dict[f"dz_{v}"] = {
                "_FillValue": netCDF4.default_fillvals["f8"],
                "zlib": True,
                # "chunksizes": tuple(s),
            }

            ## appears to be another variable just with integers??
            encoding_dict[f"nz_{self.segment_name}_{var}"] = {"dtype": "int32"}

        ## Treat eta separately since it has no vertical coordinate. Do the same things as for the surface variables above
        segment_out = segment_out.rename({self.eta: f"eta_{self.segment_name}"})
        encoding_dict[f"eta_{self.segment_name}"] = {
            "_FillValue": netCDF4.default_fillvals["f8"],
        }
        segment_out[f"eta_{self.segment_name}"] = segment_out[
            f"eta_{self.segment_name}"
        ].expand_dims(
            f"{self.perpendicular}_{self.segment_name}", axis=self.axis_to_expand - 1
        )

        # Overwrite the actual lat/lon values in the dimensions, replace with incrementing integers
        segment_out[f"{self.parallel}_{self.segment_name}"] = np.arange(
            segment_out[f"{self.parallel}_{self.segment_name}"].size
        )
        segment_out[f"{self.perpendicular}_{self.segment_name}"] = [0]

        # Store actual lat/lon values here as variables rather than coordinates
        segment_out[f"lon_{self.segment_name}"] = (
            [f"ny_{self.segment_name}", f"nx_{self.segment_name}"],
            self.hgrid_seg.x.data,
        )
        segment_out[f"lat_{self.segment_name}"] = (
            [f"ny_{self.segment_name}", f"nx_{self.segment_name}"],
            self.hgrid_seg.y.data,
        )

        # Add units to the lat / lon to keep the `categorize_axis_from_units` checker happy
        segment_out[f"lat_{self.segment_name}"].attrs = {
            "units": "degrees_north",
        }
        segment_out[f"lon_{self.segment_name}"].attrs = {
            "units": "degrees_east",
        }

        # If repeat-year forcing, add modulo coordinate
        if self.repeat_year_forcing:
            segment_out["time"] = segment_out["time"].assign_attrs({"modulo": " "})

        with ProgressBar():
            segment_out.load().to_netcdf(
                self.outfolder / f"forcing/forcing_obc_{self.segment_name}.nc",
                encoding=encoding_dict,
                unlimited_dims="time",
            )

        return segment_out, encoding_dict
