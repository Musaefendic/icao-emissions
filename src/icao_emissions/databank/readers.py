"""Helper function to get data resourcers."""

import os
from typing import List

import pandas as pd
import pkg_resources
import yaml


def _find_raw_icao_databank_file(
    directory,
    folder,
    icao_file_extension,
) -> List[str]:
    files = pkg_resources.resource_listdir(directory, folder)
    return [filename for filename in files if icao_file_extension in filename]


def _raise_exception_no_raw_databank_found() -> None:
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


def get_raw_databank_filename() -> str:
    """Returns the filename for the *raw* ICAO emissions databank."""
    directory = "data"
    folder = "icao_databank/raw"
    icao_file_extension = ".xlsx"

    icao_files = _find_raw_icao_databank_file(
        directory,
        folder,
        icao_file_extension,
    )

    if not icao_files:
        _raise_exception_no_raw_databank_found()
    elif len(icao_files) > 1:
        _raise_exception_only_one_raw_databank_stored(icao_files)

    raw_icao_datanbank = os.path.join(folder, icao_files[0])

    return pkg_resources.resource_filename(
        directory,
        raw_icao_datanbank,
    )


def get_raw_gaseous_databank() -> pd.DataFrame:
    """Returns the *raw* gasesous emissions databank."""
    filename = get_raw_databank_filename()
    return pd.read_excel(filename, sheet_name="Gaseous Emissions and Smoke")


def get_raw_nvpm_databank() -> pd.DataFrame:
    """Returns the *raw* nvPM emissions databank."""
    filename = get_raw_databank_filename()
    return pd.read_excel(filename, sheet_name="nvPM Emissions")
