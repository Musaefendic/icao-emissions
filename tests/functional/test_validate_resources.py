"""Tests tests to validate the existence of resources and that they are correctly defined."""
import importlib.resources
from pathlib import Path
from typing import Any

import pytest
from icao_emissions.databank import readers
from icao_emissions.exceptions.readers_databank import (
    MultipleRawDatankFoundError,
    NoRawDatabankFoundError,
)
from icao_emissions.utils import resources
from schema import Schema


# Add tests:
#    - when data resources are empty


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
    raw_icao_databank = readers._get_raw_databank_filename()

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
    with pytest.raises(MultipleRawDatankFoundError):
        readers._get_raw_databank_filename()


def test_missing_raw_icao_databank_throw_error(mocker) -> None:
    """An error has to be thrown if any ICAO emissions databank was found.

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
        return_value=[],  # empty list
    )

    # Assert
    with pytest.raises(NoRawDatabankFoundError):
        readers._get_raw_databank_filename()


@pytest.mark.parametrize(
    "repository, filename",
    [
        ("data.icao_databank.configs.gaseous", "config.yaml"),
        ("data.icao_databank.configs.nvpm", "config.yaml"),
        ("data.icao_databank.configs.engines", "engines.yaml"),
    ],
)
def test_cleaning_config_files_exist(repository, filename):
    """Validate that the resources required for running the module are present."""
    # Assert
    assert importlib.resources.is_resource(repository, filename)


@pytest.mark.parametrize("emission_type", ["gaseous", "nvpm"])
def test_cleaning_config_is_correctly_defined(emission_type):
    """Validate the definition of the cleaning config file."""
    # Arrange - Excepected definition of the cleaning config file
    schema = Schema(
        {
            "remove_columns": list[str],
            "rename_header": dict[str, str],
            "emissions_databank": list[str],
            "certification_databank": list[str],
        },
    )

    # Act
    cleaning_config = resources.get_cleaning_config(emission_type)

    # Assert
    assert schema.is_valid(cleaning_config)


def test_engines_config_file_exists():
    """Validate the definition of the engines config file."""
    # Arrange
    schema = Schema({"remove": list[str], "update": dict[str, dict[str, str]]})

    # Act
    engines_config = resources.get_engines_config()

    # Assert
    assert schema.validate(engines_config)
