"""Helper function to get data resourcers."""

import importlib.resources
from pathlib import Path
from typing import List, NoReturn

import pandas as pd


def _find_raw_icao_databank_file(
    repository: str,
    icao_file_extension: str,
) -> List[str]:
    files = list(importlib.resources.contents(repository))
    return [filename for filename in files if icao_file_extension in filename]


def _raise_exception_no_raw_databank_found() -> NoReturn:
    raise ValueError(
        """
        No raw ICAO databank found!
        
        Please:
            - Download emissions databank from ICAO website
            - https://www.easa.europa.eu/domains/environment/icao-aircraft-engine-emissions-databank
            - Store the downloaded file in the repository: 'data/icao_databank/raw'
        """
    )


def _raise_exception_only_one_raw_databank_stored(
    icao_files: List[str],
) -> None:
    raise ValueError(
        """
        Multiple ICAO databank were found in the repository:
                - {}
        Only one excel file should be stored.
        """.format(
            "\n\t\t- ".join(icao_files),
        ),
    )


def get_raw_databank_filename() -> Path:
    """Returns the filename for the *raw* ICAO emissions databank."""
    repository = "data.icao_databank.raw"
    icao_file_extension = ".xlsx"

    icao_files = _find_raw_icao_databank_file(
        repository,
        icao_file_extension,
    )

    # avoid some edge cases
    if not icao_files:
        _raise_exception_no_raw_databank_found()
    elif len(icao_files) > 1:
        _raise_exception_only_one_raw_databank_stored(icao_files)

    with importlib.resources.path(repository, icao_files[0]) as filename:
        return filename


def get_raw_gaseous_databank() -> pd.DataFrame:
    """Returns the *raw* gasesous emissions databank."""
    filename = get_raw_databank_filename()
    return pd.read_excel(filename, sheet_name="Gaseous Emissions and Smoke")


def get_raw_nvpm_databank() -> pd.DataFrame:
    """Returns the *raw* nvPM emissions databank."""
    filename = get_raw_databank_filename()
    return pd.read_excel(filename, sheet_name="nvPM Emissions")
