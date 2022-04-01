"""Helper function to get data resourcers."""

import importlib.resources
from pathlib import Path
from typing import List

import pandas as pd
from icao_emissions.exceptions.readers_databank import (
    EmissionNotSupportedError,
    MultipleRawDatankFoundError,
    NoRawDatabankFoundError,
)


def _find_raw_icao_databank_file(
    repository: str,
    icao_file_extension: str,
) -> List[str]:
    files = list(importlib.resources.contents(repository))
    return [filename for filename in files if icao_file_extension in filename]


def _get_raw_databank_filename() -> Path:
    """Returns the filename for the *raw* ICAO emissions databank."""
    repository = "data.icao_databank.raw"
    icao_file_extension = ".xlsx"

    icao_files = _find_raw_icao_databank_file(
        repository,
        icao_file_extension,
    )

    # avoid some edge cases
    if not icao_files:
        raise NoRawDatabankFoundError
    elif len(icao_files) > 1:
        raise MultipleRawDatankFoundError(icao_files)

    with importlib.resources.path(repository, icao_files[0]) as filename:
        return filename


def get_emissions_databank(emission_type: str) -> pd.DataFrame:
    """Returns a cleand gaseous emissions databank."""
    # init
    repository = "data.icao_databank"

    # build the filename
    databank = "{0}_emissions.csv".format(emission_type)

    # import
    with importlib.resources.path(repository, databank) as filename:
        return pd.read_csv(filename)


def get_certification_databank(emission_type: str) -> pd.DataFrame:
    """Returns a cleand gaseous emissions databank."""
    # init
    repository = "data.icao_databank"

    # build the filename
    databank = "{0}_certification.csv".format(emission_type)

    # import
    with importlib.resources.path(repository, databank) as filename:
        return pd.read_csv(filename)


def get_raw_databank(emission: str):
    """Returns a *raw* emissions databank -> gaseous or nvpm databank."""
    # Raise a ValueError if the argument provided is not supported
    if emission not in {"gaseous", "nvpm"}:
        raise EmissionNotSupportedError(emission)

    # load the databank
    filename = _get_raw_databank_filename()

    # get the databank
    if emission == "gaseous":
        sheet_name = "Gaseous Emissions and Smoke"
    elif emission == "nvpm":
        sheet_name = "nvPM Emissions"

    return pd.read_excel(
        filename,
        sheet_name=sheet_name,
    )
