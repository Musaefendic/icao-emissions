"""Script to clean the ICAO emissions databank.

Although the data contained within the emission databank is structured
and cleaned, some operations are made to facilitate its use, such as:
- Remove duplicate rows
- Update model names to correctly reflect the evolution of
engine definitions. Example: TRENT1000 Pack-B1, TRENT1000 Pack-C1, ...
"""
import pandas as pd
from icao_emissions.databank import edb_raw


def main() -> pd.DataFrame:
    print(edb_raw.head())
    return edb_raw


if __name__ == "__main__":
    main()
