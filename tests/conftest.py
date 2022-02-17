"""pytest fixtures."""

import pkg_resources
import pytest


@pytest.fixture()
def raw_icao_databank_filename():
    """Returns the filename of the ICAO emissions databank."""
    return pkg_resources.resource_filename(
        "data",
        "icao_databank/raw/edb-emissions-databank_v28c_web.xlsx",
    )
