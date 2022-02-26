import importlib.resources

import yaml
from icao_emissions.exceptions.data_resources import DataResourceMissingError


def _import_yaml_to_dict(repository: str, filename: str) -> dict:  # noqa
    with importlib.resources.open_binary(repository, filename) as infile:
        return yaml.safe_load(infile)


def get_cleaning_config(emission_type: str) -> dict:
    """Return a config file to clean the emission databank.

    Args:
        emission_type (str): 'gaseous' or 'nvpm'

    Returns:
        a config dict

    Raises:
        ValueError: if emission_type is not 'gaseous' nor 'nvpm
    """
    # Init
    repository = "data.icao_databank.configs"
    filename = "config.yaml"

    if emission_type not in set(["gaseous", "nvpm"]):
        raise ValueError("The only arguments allowed are: 'gaseous' or 'nvpm'")

    # construct the repository position
    repository += "." + emission_type

    # Evaluate if the resource exists
    if not importlib.resources.is_resource(repository, filename):
        raise DataResourceMissingError(repository, filename)

    return _import_yaml_to_dict(repository, filename)


def get_engines_config() -> dict:
    # Init
    repository = "data.icao_databank.configs.engines"
    filename = "engines.yaml"

    # Evaluate if the resource exists
    if not importlib.resources.is_resource(repository, filename):
        DataResourceMissingError(repository, filename)

    return _import_yaml_to_dict(repository, filename)
