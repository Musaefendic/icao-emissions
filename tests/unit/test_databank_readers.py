"""Tests to verify the implementations of functions related to read icao databanks."""

import pandas as pd
import pytest
from icao_emissions.databank import readers
from icao_emissions.exceptions.readers_databank import (
    EmissionNotSupportedError,
    MultipleRawDatankFoundError,
    NoRawDatabankFoundError,
)


def test_search_raw_databank_raises_error_if_no_file_found(mocker):
    # Arrange
    mocker.patch(
        "importlib.resources.contents",
        return_value=[],
    )

    # Act & Assert
    with pytest.raises(NoRawDatabankFoundError):
        filename = readers._get_raw_databank_filename()  # noqa


def test_search_raw_databank_raises_error_if_multiple_files_found(mocker):
    # Arrange
    mocker.patch(
        "importlib.resources.contents",
        return_value=["file_n1.xlsx", "file_n2.xlsx"],
    )

    # Act & Assert
    with pytest.raises(MultipleRawDatankFoundError):
        filename = readers._get_raw_databank_filename()  # noqa


@pytest.mark.parametrize("emission", ["gaseous", "nvpm"])
def test_get_raw_databank_returns_dataframe(emission):
    # Act
    raw_databank = readers.get_raw_databank(emission)

    # Assert
    assert isinstance(raw_databank, pd.DataFrame)


def test_get_raw_databank_raises_error_given_wrong_argument():
    # Arrange
    emission = "wrong_input"

    # Act & Assert
    with pytest.raises(EmissionNotSupportedError):
        raw_databank = readers.get_raw_databank(emission)
