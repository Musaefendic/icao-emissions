"""Tests related to the cleaning of the ICAO emissions databank."""

import pkg_resources
from icao_emissions.utils import hashing


def test_raw_icao_databank_is_correct(raw_icao_databank_filename):
    """Verify the raw icao emissions databank is unaltered."""
    # Arange
    hash_read_in_bytes = pkg_resources.resource_string(
        "data",
        "icao_databank/raw/edb-emissions-databank_v28c_web.sha",
    )
    expected_hash = hash_read_in_bytes.decode("utf-8")

    # Act
    databank_hash = hashing.compute_key(raw_icao_databank_filename)

    # Assert
    assert databank_hash == expected_hash
