import importlib.resources
from typing import Any, List, TypedDict

import yaml
from icao_emissions.exceptions.data_resources import DataResourceMissingError


class CleaningConfig(TypedDict):  # noqa: H601 - class has low cohesion
    """Define the type for the cleaning config file.

    Files:
        - data/icao_databank/configs/gaseous/config.yaml
        - data/icao_databank/configs/nvpm/config.yaml
    """

    remove_columns: List[str]
    add_columns: dict[str, Any]
    rename_header: dict[str, str]
    emissions_databank: dict[str, str]
    certification_databank: List[str]


class EnginesConfig(TypedDict):  # noqa: H601 - class has low cohesion
    """Define the type for the engines config file.

    File:
        - data/icao_databank/configs/engines/engines.yaml
    """

    remove: List[str]
    update: dict[str, dict[str, str]]


def get_cleaning_config(emission_type: str) -> CleaningConfig:
    """Return a config file to clean the emission databank.

    Args:
        emission_type (str): 'gaseous' or 'nvpm'

    Returns:
        A config dict that defines how to clean the raw ICAO databank

    Raises:
        ValueError: if emission_type is not 'gaseous' nor 'nvpm
        DataResourceMissingError: if the resource file does not exist
    """
    # Init
    repository = "data.icao_databank.configs"
    filename = "config.yaml"

    if emission_type not in {"gaseous", "nvpm"}:
        raise ValueError("The only arguments allowed are: 'gaseous' or 'nvpm'")

    # construct the repository position
    repository = "{0}.{1}".format(repository, emission_type)

    # Evaluate if the resource exists
    if not importlib.resources.is_resource(repository, filename):
        raise DataResourceMissingError(repository, filename)

    # Load yaml file in a dictionary
    with importlib.resources.open_binary(repository, filename) as infile:
        cleaning_parameters: CleaningConfig = yaml.safe_load(infile)

    return cleaning_parameters


def get_engines_config() -> EnginesConfig:
    """Return a config file with the information to be updated for some engines.

    Returns:
        A config dict with the information to be updated for the defined engines

    Raises:
        DataResourceMissingError: if the resource file does not exist
    """
    # Init
    repository = "data.icao_databank.configs.engines"
    filename = "engines.yaml"

    # Evaluate if the resource exists
    if not importlib.resources.is_resource(repository, filename):
        raise DataResourceMissingError(repository, filename)

    # Load yaml file in a dictionary
    with importlib.resources.open_binary(repository, filename) as infile:
        engines_config: EnginesConfig = yaml.safe_load(infile)

    return engines_config
