"""Script to clean the ICAO emissions databank.

Although the data contained within the emission databank is structured
and cleaned, some operations are made to facilitate its use, such as:
- Remove duplicate rows
- Update model names to correctly reflect the evolution of
engine definitions. Example: TRENT1000 Pack-B1, TRENT1000 Pack-C1, ...
"""
import os
from importlib.resources import path
from typing import NoReturn

import pandas as pd
from icao_emissions.databank import readers
from icao_emissions.utils import resources


def compute_thrust(databank: pd.DataFrame, index: str) -> NoReturn:
    """For each engine, calculates the thrust for each operating point."""
    # init
    thrust_setting = (
        ("thrust_take_off", 1.0),
        ("thrust_climb", 0.85),
        ("thrust_approach", 0.3),
        ("thrust_idle", 0.07),
    )

    # get the rated thrust
    rated_thrust = databank.loc[index]["rated_thrust"]

    # compute thrust for each operating point
    for operating_point, thrust_percent in thrust_setting:
        databank.at[index, operating_point] = rated_thrust * thrust_percent


def cleaning_chain(
    databank: pd.DataFrame,
    config: dict,
    engines: dict,
) -> pd.DataFrame:
    """Clean the the data contained within the ICAO databank."""
    # header cleaning
    databank = databank.rename(columns=config["rename_header"])
    databank = databank.drop(columns=config["remove_columns"])

    # remove some engines (corresponds to duplicate information)
    databank = databank[~databank.uid.isin(engines["remove"])]

    # set dataframe index
    databank = databank.set_index("uid")

    # for each engine, some informations are updated
    for engine_uid, updates in engines["update"].items():
        databank.loc[engine_uid, updates.keys()] = updates.values()

    # compute additional information
    for index, _ in databank.iterrows():
        compute_thrust(databank, index)

    return databank


def _rename_header(databank: pd.DataFrame, config):
    ...


def _foo():
    databank = rename_header(databank, config)

    databank = remove_columns(databank, config)

    databank = remove_duplicate_engines(databank, config)

    databank = databank.set_index("uid")

    databank = update_databank_informations(databank, config)

    # additionnal values
    databank = compute_intermediate_thrust(databank)

    # split databank
    emissions_databank, certification_databank = split_databank(
        databank, config
    )

    return emissions_databank, certification_databank


def clean_gasesous_databank() -> pd.DataFrame:
    """Return a cleaned gaseous emissions databank."""
    # get config files needed for cleaning the databank
    config = resources.get_cleaning_config(emission_type="gaseous")
    engines = resources.get_engines_config()

    # get the raw databank and clean it
    raw_gaseous_databank = readers.get_raw_gaseous_databank()
    return cleaning_chain(
        raw_gaseous_databank,
        config,
        engines,
    )


def generate_clean_databank(emissions_type: str):
    # generate a clean datafra
    if emissions_type == "gaseous":
        clean_df = clean_gasesous_databank()
        save_filename = "gaseous_databank.csv"

    elif emissions_type == "nvpm":
        save_filename = "nvpm_databank.csv"
        raise ValueError("not implemented")

    else:
        raise ValueError("the provided argument is not supported")

    # save
    with path("data.icao_databank", "__init__.py") as resource:
        directory = resource.parent.resolve()
        filepath = os.path.join(directory, save_filename)
        clean_df.to_csv(filepath)


def main() -> None:
    generate_clean_databank(emissions_type="gaseous")


if __name__ == "__main__":
    main()
