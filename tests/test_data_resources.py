"""Tests to verify that the module correctly provides the icao databases."""

from pathlib import Path

import pytest
from icao_emissions.databank import readers


def test_verify_only_one_raw_icao_datanbank_stored():
    """Verify that only one raw icao databank is stored.

    Requirement:
        - The repository './data/icao_databank/raw'
        - Must contain *only one* Excel file, format '.xlsx'

    Justification:
        - Avoid making the code dependent of the database name, when new data will be added.
        - Examples of the oaci database name for different versions:
            * edb-emissions-databank v23 (web).xlsx
            * edb-emissions-databank v27 (web).xlsx
            * edb-emissions-databank_v28c_web.xlsx
        - The function to read the database does not look for a specific file name, but imports the only excel file stored in the /raw folder
    """
    # Act
    raw_icao_databank = readers.get_raw_databank_filename()

    # Assert
    assert isinstance(raw_icao_databank, Path)


def test_multiple_raw_icao_databank_stored_throw_error(mocker):
    """An error has to be thrown if multiple databanks are stored in folder 'raw/'.

    Requirement:
        - The repository './data/icao_databank/raw'
        - Must contain *only one* Excel file, format '.xlsx'

    Justification:
        - Avoid making the code dependent of the emissions databank name, when new data will be added.
        - Examples of the ICAO databank name for different versions:
            * edb-emissions-databank v23 (web).xlsx
            * edb-emissions-databank v27 (web).xlsx
            * edb-emissions-databank_v28c_web.xlsx
        - The function to read the emissions databank does not look for a specific file name, but imports the only excel file stored in the /raw folder
    """
    # Arrange
    mocker.patch(
        "icao_emissions.databank.readers._find_raw_icao_databank_file",
        return_value=[
            "icao_databank_n1.xlsx",
            "icao_databank_n2.xlsx",
            "icao_databank_n3.xlsx",
        ],
    )

    # Assert
    with pytest.raises(ValueError):
        readers.get_raw_databank_filename()


def test_missing_raw_icao_databank_throw_error(mocker):
    """An error has to be thrown if any ICAO emissions databank was found.

    Justification:
        - Avoid making the code dependent of the emissions databank name, when new data will be added.
        - Examples of the ICAO databank name for different versions:
            * edb-emissions-databank v23 (web).xlsx
            * edb-emissions-databank v27 (web).xlsx
            * edb-emissions-databank_v28c_web.xlsx
        - The function to read the emissions databank does not look for a specific file name, but imports the only excel file stored in the /raw folder
    """
    # Arange
    mocker.patch(
        "icao_emissions.databank.readers._find_raw_icao_databank_file",
        return_value=[],  # empty list
    )

    # Assert
    with pytest.raises(ValueError):
        readers.get_raw_databank_filename()
