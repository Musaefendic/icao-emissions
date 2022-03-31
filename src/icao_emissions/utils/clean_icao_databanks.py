import os
from importlib.resources import path
from pathlib import Path
from typing import Tuple

import pandas as pd
from icao_emissions.databank import readers
from icao_emissions.exceptions.clean_databanks import (
    UidNotFoundError,
    VariablesNotInHeaderError,
)
from icao_emissions.utils import resources


def clean(emission_type: str):
    # define emissions handled by the cleaning function
    emission_type_supported = ("gaseous", "nvpm")

    # handle the case if the wrong emission has been provided
    if emission_type not in emission_type_supported:
        raise ValueError("the provided argument is not supported")

    # load the databank
    raw_databank = readers.get_raw_databank(emission=emission_type)

    # load config files used to clean the dataset
    config = resources.get_cleaning_config(emission_type="gaseous")
    engines = resources.get_engines_config()

    # clean
    emissions_databank, certification_databank = _cleaning_pipeline(
        databank=raw_databank,
        cleaning_parameters=config,
        cleaning_engines=engines,
    )

    # write the databanks
    _save_databanks(emissions_databank, certification_databank, emission_type)


def _cleaning_pipeline(
    databank: pd.DataFrame,
    cleaning_parameters: resources.CleaningConfig,
    cleaning_engines: resources.EnginesConfig,
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    # clean header
    databank = _rename_header(databank, cleaning_parameters["rename_header"])
    databank = _remove_columns(databank, cleaning_parameters["remove_columns"])

    # remove some duplicates
    databank = _remove_duplicate_engines(databank, cleaning_engines["remove"])

    # update information about each individual engines
    databank = _update_databank_informations(
        databank,
        cleaning_engines["update"],
    )

    # compute additionnal values
    databank = _compute_intermediate_thrusts(databank)

    # split the raw icao databank -> get emissions and some additional fields
    emissions_databank = _extract_emissions_data_from_icao_databank(
        databank,
        cleaning_parameters["emissions_databank"],
    )

    # split the raw icao databank -> get certification data
    certification_databank = _extract_certification_data_from_icao_databank(
        databank,
        cleaning_parameters["certification_databank"],
    )

    return emissions_databank, certification_databank


def _save_databanks(
    emissions_databank: pd.DataFrame,
    certification_databank: pd.DataFrame,
    emission: str,
):
    target_repository = "data.icao_databank"

    with path(target_repository, "__init__.py") as resource:
        # build the directory
        directory = resource.parent.resolve()

        # save emissions_databank
        emissions_databank_filepath = _build_filepath(
            directory=directory,
            emission_type=emission,
            databank_type="emissions",
        )
        _save(
            databank=emissions_databank,
            filepath=emissions_databank_filepath,
        )

        # save certification_databank
        certification_databank_filepath = _build_filepath(
            directory=directory,
            emission_type=emission,
            databank_type="certification",
        )
        _save(
            databank=certification_databank,
            filepath=certification_databank_filepath,
        )


def _build_filepath(
    directory: Path,
    emission_type: str,
    databank_type: str,
) -> Path:
    # build filename & filepath
    filename = "{0}_{1}.csv".format(emission_type, databank_type)
    return os.path.join(directory, filename)


def _save(
    databank: pd.DataFrame,
    filepath: Path,
):
    databank.to_csv(filepath, index=False)


def _rename_header(
    databank: pd.DataFrame,
    mapping: dict[str, str],
) -> pd.DataFrame:
    # Ensure keys to be renamed are contained in the header
    header = set(databank.columns)
    columns_to_rename = set(mapping.keys())

    if not columns_to_rename.issubset(header):
        raise VariablesNotInHeaderError(header, columns_to_rename)

    return databank.rename(columns=mapping)


def _remove_columns(
    databank: pd.DataFrame,
    columns: list[str],
) -> pd.DataFrame:
    # if one item contained in columns not found in header
    # Pandas will raise a keyError
    return databank.drop(columns=columns)


def _remove_duplicate_engines(
    databank: pd.DataFrame,
    duplicates: list[str],
) -> pd.DataFrame:
    # Ensure all uid that have to be removed are contained within the dataframe
    databank_uid = set(databank.uid)
    uid_to_remove = set(duplicates)

    if not uid_to_remove.issubset(databank_uid):
        raise UidNotFoundError(databank_uid, uid_to_remove)

    return databank[~databank.uid.isin(duplicates)]


def _update_databank_informations(
    databank: pd.DataFrame,
    updates: dict[str, dict[str, str]],
) -> pd.DataFrame:
    # Ensure all uids that have to be updated are contained within the databank
    databank_uid = set(databank.uid)
    uid_to_remove = set(updates.keys())

    if not uid_to_remove.issubset(databank_uid):
        raise UidNotFoundError(databank_uid, uid_to_remove)

    header = set(databank.columns)

    for engine_uid, features in updates.items():
        # update
        index = databank[databank["uid"] == engine_uid].index
        databank.loc[index, features.keys()] = list(features.values())
    return databank


def _compute_intermediate_thrusts(databank: pd.DataFrame) -> pd.DataFrame:
    """For each engine, calculates the thrust for each operating point."""
    # init
    thrust_setting = (
        ("thrust_take_off", 1.0),
        ("thrust_climb", 0.85),
        ("thrust_approach", 0.3),
        ("thrust_idle", 0.07),
    )

    # compute intermediate thrusts
    for index, _ in databank.iterrows():
        # get the rated thrust
        rated_thrust = databank.loc[index]["rated_thrust"]

        # compute thrust for each operating point
        for operating_point, thrust_percent in thrust_setting:
            databank.at[index, operating_point] = rated_thrust * thrust_percent

    return databank


def _extract_emissions_data_from_icao_databank(
    databank: pd.DataFrame,
    definition_emissions_databank: dict[str, str],
) -> pd.DataFrame:
    # Init
    emissions = pd.DataFrame()

    # start the extraction and build the new dataframe: emissions
    for _, row in databank.iterrows():
        data = {}

        # build the intermediate dictionary
        for name, values_to_extract in definition_emissions_databank.items():
            data[name] = row[values_to_extract].tolist()

        # transform into a dataframe
        _df = pd.DataFrame(data)

        # stack
        emissions = pd.concat([emissions, _df], ignore_index=True)

    return emissions


def _extract_certification_data_from_icao_databank(
    databank: pd.DataFrame,
    definition_certification_databank: list[str],
) -> pd.DataFrame:
    return databank[definition_certification_databank]


if __name__ == "__main__":
    clean("gaseous")
