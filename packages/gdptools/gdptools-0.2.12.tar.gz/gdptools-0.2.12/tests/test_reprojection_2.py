import pytest
import geopandas as gpd
from shapely.geometry import Polygon
from pyproj import CRS
from gdptools.utils import _check_reprojection


# Mock functions and logger
def _check_grid_file_availability(source_crs, new_crs):
    pass


def _check_invalid_geometries(gdf):
    pass


def _check_empty_geometries(gdf):
    pass


def _check_inf_values(gdf):
    pass


class MockLogger:
    def error(self, message):
        pass


logger = MockLogger()

SOURCE_ORIGIN = str


@pytest.mark.parametrize(
    "gdf, new_crs, source_crs, source_type",
    [
        # Happy path test cases with polygons
        (gpd.GeoDataFrame(geometry=[Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])]), 4326, 3857, "source"),
        (gpd.GeoDataFrame(geometry=[Polygon([(0, 0), (2, 0), (2, 2), (0, 2)])]), "EPSG:4326", "EPSG:3857", "target"),
        (
            gpd.GeoDataFrame(geometry=[Polygon([(0, 0), (3, 0), (3, 3), (0, 3)])]),
            CRS.from_epsg(4326),
            CRS.from_epsg(3857),
            "source",
        ),
    ],
    ids=["happy_path_epsg", "happy_path_string", "happy_path_crs_object"],
)
def test_check_reprojection_happy_path(gdf, new_crs, source_crs, source_type):
    # Act
    _check_reprojection(gdf, new_crs, source_crs, source_type)

    # Assert
    # No exception should be raised


@pytest.mark.parametrize(
    "gdf, new_crs, source_crs, source_type, expected_exception, expected_message",
    [
        # Edge case: empty GeoDataFrame
        (
            gpd.GeoDataFrame(geometry=[]),
            4326,
            3857,
            "source",
            RuntimeError,
            "Error during reprojection of the source polygons.",
        ),
        # Error case: invalid CRS
        (
            gpd.GeoDataFrame(geometry=[Polygon([(0, 0), (1, 0), (1, 1), (0, 1)])]),
            "invalid_crs",
            3857,
            "source",
            RuntimeError,
            "Error during reprojection of the source polygons.",
        ),
        # Error case: invalid geometry (self-intersecting polygon)
        (
            gpd.GeoDataFrame(geometry=[Polygon([(0, 0), (1, 1), (1, 0), (0, 1)])]),
            4326,
            3857,
            "source",
            RuntimeError,
            "Error during reprojection of the source polygons.",
        ),
    ],
    ids=["empty_geodataframe", "invalid_crs", "invalid_geometry"],
)
def test_check_reprojection_error_cases(gdf, new_crs, source_crs, source_type, expected_exception, expected_message):
    # Act & Assert
    with pytest.raises(expected_exception) as excinfo:
        _check_reprojection(gdf, new_crs, source_crs, source_type)

    # Assert
    assert expected_message in str(excinfo.value)
