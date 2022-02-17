"""Helper function to get data resourcers."""

import pandas as pd
import pkg_resources


def get_raw_icao_databank() -> pd.DataFrame:
    """Returns the ICAO emissions databank in a pandas DataFrame format."""
    excel_file = pkg_resources.resource_filename(
        "data",
        "icao_databank/raw/edb-emissions-databank_v28c_web.xlsx",
    )
    return pd.read_excel(excel_file)
