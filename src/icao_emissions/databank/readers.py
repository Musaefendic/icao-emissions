"""Helper function to get data resourcers."""

import importlib.resources
from pathlib import Path
from typing import List

import pandas as pd
from icao_emissions.exceptions.icao_databank import (
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


def get_gaseous_databank() -> pd.DataFrame:
    """Returns a cleand gaseous emissions databank."""
    repository = "data.icao_databank"
    databank = "gaseous_databank.csv"
    with importlib.resources.path(repository, databank) as filename:
        return pd.read_csv(filename)


def get_raw_gaseous_databank() -> pd.DataFrame:
    """Returns the *raw* gasesous emissions databank."""
    filename = _get_raw_databank_filename()
    return pd.read_excel(
        filename,
        sheet_name="Gaseous Emissions and Smoke",
    )


def get_raw_nvpm_databank() -> pd.DataFrame:
    """Returns the *raw* nvPM emissions databank."""
    filename = _get_raw_databank_filename()
    return pd.read_excel(filename, sheet_name="nvPM Emissions")
