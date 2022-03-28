"""Tests to verify the implementations of functions related to resources."""

import pytest
from icao_emissions.exceptions.data_resources import DataResourceMissingError
from icao_emissions.utils import resources


@pytest.mark.parametrize("emission_type", ["gaseous", "nvpm"])
def test_get_cleaning_config(emission_type, mocker) -> None:
    """Verify the cleaning config file is returned properly."""
    # Arrange - Define a mock config file resource
    cleaning_config = {
        "remove_columns": ["NOx Compliance Demonstration §"],
        "rename_header": {"UID No": "uid", "Manufacturer": "manufacturer"},
        # the actual file contains more attributes
    }

    # Arrange - Mock the yaml loader
    mocker.patch(
        "yaml.safe_load",
        return_value=cleaning_config,
    )

    # Act
    config = resources.get_cleaning_config(emission_type)

    # Assert
    assert isinstance(config, dict)


def test_cleaning_config_missing_raise_error(mocker):
    """Verify an error is thrown if the config file is missing."""
    # Arange - Simulate a missing config file
    mocker.patch(
        "importlib.resources.is_resource",
        return_value=False,
    )

    # Act & Assert
    with pytest.raises(DataResourceMissingError):
        emissions_type = "gaseous"
        config = resources.get_cleaning_config(emissions_type)


def test_get_cleaning_config_with_wrong_keyword_raise_error():
    """Verify an error is thrown if the wrong."""
    # Arange
    emissions_type = "wrong_argument"

    # Assert
    with pytest.raises(ValueError):
        config = resources.get_cleaning_config(emissions_type)


def test_engines_config_missing_resource_raise_error(mocker):
    """Verify an error is thrown if the config file is missing."""
    # Arange - Simulate a missing config file
    mocker.patch(
        "importlib.resources.is_resource",
        return_value=False,
    )

    # Act & Assert
    with pytest.raises(DataResourceMissingError):
        config = resources.get_engines_config()


def test_engines_config_returns_dict(mocker):
    """Verify the engines config file is returned properly."""
    # Arrange - Define a mock config file resource
    engines_config = {
        "remove": ["6GE092", "8GE110"],
        "update": {"01P05GE189": {"engine": "CF34-3B", "model": "CF34-3B}"}},
        # the actual file is more detailed
    }

    # Arrange - Mock the yaml loader
    mocker.patch(
        "yaml.safe_load",
        return_value=engines_config,
    )

    # Act
    config = resources.get_engines_config()

    # Assert
    assert isinstance(config, dict)
