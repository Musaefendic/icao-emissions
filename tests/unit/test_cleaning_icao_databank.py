from os import remove

import pandas as pd
import pytest
from icao_emissions.databank import readers
from icao_emissions.exceptions.clean_databanks import (
    UidNotFoundError,
    VariablesNotInHeaderError,
)
from icao_emissions.utils import clean_icao_databanks, resources
from pytest_mock import MockerFixture


@pytest.mark.parametrize(
    "emission_type",
    ["gaseous", "nvpm"],
)
def test_clean_function_ends_with_two_databanks_saved(
    emission_type: str,
    mocker: MockerFixture,
):
    # Arrange - define a toy dataframe
    emissions_databank = pd.DataFrame(
        {
            "thrust": [100, 85, 30, 7],
            "ienox": [4, 3, 2, 1],
        },
    )
    # Arrange - define a toy dataframe
    certification_databank = pd.DataFrame(
        {
            "engine": ["CFM56-5B", "LEAP-1A"],
            "nox_characteristic": [2, 1],
        },
    )

    # Arrange - Mock the write function 'to_csv' for both databanks
    mock_emissions_databank = mocker.patch.object(
        emissions_databank,
        "to_csv",
    )
    mock_certification_databank = mocker.patch.object(
        certification_databank,
        "to_csv",
    )

    # Act
    clean_icao_databanks._save_databanks(  # noqa - call a private method
        emissions_databank,
        certification_databank,
        emission_type,
    )

    # Assert
    mock_emissions_databank.assert_called_once()
    mock_certification_databank.assert_called_once()


@pytest.mark.parametrize(
    "emission_type",
    ["gaseous"],
)
def test_clean_pipeline_returns_tuple_of_dataframe(
    mocker: MockerFixture, emission_type: str
):
    # Arrange
    databank = readers.get_raw_databank(emission=emission_type)

    # load config files used to clean the dataset
    config = resources.get_cleaning_config(emission_type=emission_type)
    engines = resources.get_engines_config()

    # Act
    cleaning_result = clean_icao_databanks._cleaning_pipeline(
        databank, config, engines
    )

    # Assert
    assert isinstance(cleaning_result, tuple)
    assert len(cleaning_result) == 2
    assert isinstance(cleaning_result[0], pd.DataFrame)
    assert isinstance(cleaning_result[1], pd.DataFrame)


def test_clean_function_raises_error_for_wrong_emission_type():
    # Arrange
    emission_type = "wrong_argument"

    # Act & Assert
    with pytest.raises(ValueError):
        clean_icao_databanks.clean(emission_type)


def test_save_dataframe_without_index(mocker: MockerFixture):
    # Arrange - define a toy dataframe
    databank = pd.DataFrame(
        {"engine": ["CFM56", "LEAP-1A"], "ienox": [10, 5]},
    )

    # Arrange - build the filepath
    filepath = "data.icao_databank.gaseous_emissions.csv"

    # Arrange - Mock the write function 'to_csv'
    mock = mocker.patch.object(databank, "to_csv")

    # Act
    clean_icao_databanks._save(databank, filepath)  # noqa - private method

    # Assert
    mock.assert_called_once_with(filepath, index=False)


def test_rename_header_of_databanks():
    # Arrange - Define a toy dataframe
    databank = pd.DataFrame(
        {
            "UID": ["01P20CM127", "01P20CM128"],
            "Engine Identification": ["LEAP-1A24/24E1/23", "LEAP-1A26/26E1"],
            "NOx Dp/Foo Characteristic (g/kN)": [20, 30],
        }
    )

    # Arrange - Define the renaming table
    rename = {
        "UID": "uid",
        "Engine Identification": "model",
        "NOx Dp/Foo Characteristic (g/kN)": "nox_characteristic",
    }

    # Act - Rename
    cleand_databank = clean_icao_databanks._rename_header(databank, rename)

    # Assert
    assert set(cleand_databank.columns) == set(rename.values())
    assert cleand_databank.shape == databank.shape


def test_rename_header_raises_error_if_columns_not_found():
    # Arrange
    databank = pd.DataFrame(
        {
            "a": [0, 1, 2],
            "y": [3, 4, 5],
            "name_in_header": [6, 7, 8],
        },
    )

    rename = {"not_in_header": "b", "name_in_header": "c"}

    # Act & Assert
    with pytest.raises(VariablesNotInHeaderError):
        clean_icao_databanks._rename_header(databank, rename)


def test_remove_columns_from_databank():
    # Arrange - Define a toy dataframe
    databank = pd.DataFrame(
        {
            "UID": ["01P20CM127", "01P20CM128"],
            "Engine Identification": ["LEAP-1A24/24E1/23", "LEAP-1A26/26E1"],
            "NOx Dp/Foo Characteristic (g/kN)": [20, 30],
            "Data Superseded": [True, False],
            "Test Engine Status": ["NME", "DTEPS"],
        }
    )

    # Arrange - Define the renaming table
    remove_columns = [
        "Data Superseded",
        "Test Engine Status",
    ]

    # Act - Rename
    cleaned_databank = clean_icao_databanks._remove_columns(
        databank,
        remove_columns,
    )

    # Assert - verify the new header
    exepcted_header = set(databank.columns) - set(remove_columns)
    assert set(cleaned_databank.columns) == exepcted_header

    # Assert - verify shape
    expected_rows = databank.shape[0]  # expected unchanged number of rows
    expected_columns = databank.shape[1] - len(remove_columns)
    assert cleaned_databank.shape[0] == expected_rows
    assert cleaned_databank.shape[1] == expected_columns


def test_remove_columns_raises_error_if_columns_not_found():
    # Arrange
    databank = pd.DataFrame(
        {
            "a": [0, 1, 2],
            "y": [3, 4, 5],
            "name_in_header": [6, 7, 8],
        },
    )

    remove_columns = ["not_in_header", "name_in_header"]

    # Act & Assert
    with pytest.raises(KeyError):
        clean_icao_databanks._remove_columns(databank, remove_columns)


def test_remove_duplicate_engines():
    # Arrange - Define a toy dataframe
    databank = pd.DataFrame(
        {
            "uid": ["01P20CM127", "01P20CM128", "6GE092", "8GE110"],
            "engine": ["eng_1", "eng_2", "eng_3", "eng_4"],
            "nox_characteristic": [10, 20, 30, 40],
        }
    )

    # Arrange - Define the engines to be removed, based on uid (user_defined)
    remove_engines_based_on_uid = ["6GE092", "8GE110"]

    # Act - Remove duplicates
    cleaned_databank = clean_icao_databanks._remove_duplicate_engines(
        databank,
        remove_engines_based_on_uid,
    )

    # Assert - verify shape
    expected_rows = databank.shape[0] - len(remove_engines_based_on_uid)
    expected_columns = databank.shape[1]  # unchanged
    assert cleaned_databank.shape[0] == expected_rows
    assert cleaned_databank.shape[1] == expected_columns


def test_remove_duplicate_engines_raises_error_engine_uid_not_found():
    # Arrange - Define a toy dataframe
    databank = pd.DataFrame(
        {
            "uid": ["uid_1", "uid_2", "uid_3", "uid_4"],
            "engine": ["eng_1", "eng_2", "eng_3", "eng_4"],
            "nox_characteristic": [10, 20, 30, 40],
        }
    )

    # Arrange - Define the engines to be removed, based on uid (user_defined)
    remove_engines_based_on_uid = ["uid_1", "uid_not_present"]

    # Act & Assert
    with pytest.raises(UidNotFoundError):
        clean_icao_databanks._remove_duplicate_engines(
            databank, remove_engines_based_on_uid
        )


def test_update_databank_informations():
    # Arrange - Define a toy dataframe
    databank = pd.DataFrame(
        {
            "uid": ["uid_1", "uid_2", "uid_3"],
            "engine": ["engine_1", "wrong_value_2", "wrong_value_3"],
            "model": ["model_1", None, None],
        }
    )

    # Arrange - Define the input to update the toy dataframe
    engines_update = {
        "uid_2": {"engine": "engine_2", "model": "model_2"},
        "uid_3": {"engine": "engine_3", "model": "model_3"},
    }

    # Act
    cleaned_databank = clean_icao_databanks._update_databank_informations(
        databank.copy(),
        engines_update,
    )

    # Assert - dataframe shape is unchanged
    expected_rows = databank.shape[0]
    expected_columns = databank.shape[1]
    assert cleaned_databank.shape[0] == expected_rows
    assert cleaned_databank.shape[1] == expected_columns

    # Transform the dict 'engines_update' into a pd.DataFrame for the assert
    required_updates = pd.DataFrame.from_dict(engines_update, orient="index")
    required_updates = required_updates.reset_index()
    required_updates = required_updates.rename(columns={"index": "uid"})

    # Extract the values updated into a pd.DataFrame
    updates_after_cleaning = cleaned_databank[
        cleaned_databank["uid"].isin(engines_update.keys())
    ]
    updates_after_cleaning = updates_after_cleaning.reset_index()
    updates_after_cleaning = updates_after_cleaning.drop(columns=["index"])

    # Assert
    assert updates_after_cleaning.equals(required_updates)


def test_update_databank_informations_raises_error_if_uid_not_in_databank():
    # Arrange - Define a toy dataframe
    databank = pd.DataFrame(
        {
            "uid": ["uid_1", "uid_2", "uid_3"],
            "engine": ["engine_1", "wrong_value_2", "wrong_value_3"],
            "model": ["model_1", None, None],
        }
    )

    # Arrange - Define the input to update the toy dataframe
    engines_update = {
        "uid_2": {"engine": "engine_2", "model": "model_2"},
        "uid_not_present": {"engine": "engine_3", "model": "model_3"},
    }

    # Act & Assert
    with pytest.raises(UidNotFoundError):
        cleaned_databank = clean_icao_databanks._update_databank_informations(
            databank.copy(),
            engines_update,
        )


def test_compute_intermediate_thrusts():
    # Should add new columns and compute only row by row
    # assert shape unchanged
    # Arrange - Define a toy dataframe
    databank = pd.DataFrame(
        {
            "uid": ["01P20CM127", "01P20CM128"],
            "engine": ["eng_1", "eng_2"],
            "rated_thrust": [80, 100],  # kNewton
        }
    )

    # Act - Remove duplicates
    cleaned_databank = clean_icao_databanks._compute_intermediate_thrusts(
        databank.copy(),
    )

    # Assert - verify header contains new entries
    new_columns = {
        "thrust_take_off",
        "thrust_climb",
        "thrust_approach",
        "thrust_idle",
    }
    expected_columns = set(databank.columns) | new_columns
    assert set(cleaned_databank.columns) == expected_columns

    # Assert - verify shape
    expected_rows = databank.shape[0]  # unchanged
    expected_columns = databank.shape[1] + len(new_columns)
    assert cleaned_databank.shape[0] == expected_rows
    assert cleaned_databank.shape[1] == expected_columns


def test_extract_emissions_data_from_icao_databank():
    # Arrange
    databank = pd.DataFrame(
        {
            "uid": ["uid_1", "uid_2"],
            "engine": ["engine_1", "engine_2"],
            "einox_take_off": [9, 80],
            "einox_climb": [6, 40],
            "einox_approach": [3, 30],
            "einox_idle": [1, 20],
        }
    )

    parameters = {
        "uid": ["uid", "uid", "uid", "uid"],
        "engine": ["engine", "engine", "engine", "engine"],
        "einox": [
            "einox_take_off",
            "einox_climb",
            "einox_approach",
            "einox_idle",
        ],
    }

    expected_databank = pd.DataFrame(
        {
            "uid": [
                "uid_1",
                "uid_1",
                "uid_1",
                "uid_1",
                "uid_2",
                "uid_2",
                "uid_2",
                "uid_2",
            ],
            "engine": [
                "engine_1",
                "engine_1",
                "engine_1",
                "engine_1",
                "engine_2",
                "engine_2",
                "engine_2",
                "engine_2",
            ],
            "einox": [9, 6, 3, 1, 80, 40, 30, 20],
        }
    )

    # Act
    cleaned_databank = (
        clean_icao_databanks._extract_emissions_data_from_icao_databank(
            databank, parameters
        )
    )

    # Assert
    assert cleaned_databank.equals(expected_databank)


def test_extract_certification_data_from_icao_databank():
    # Arrange
    databank = pd.DataFrame(
        {
            "uid": ["uid_1", "uid_2"],
            "engine": ["engine_1", "engine_2"],
            "einox_take_off": [9, 80],
            "einox_climb": [6, 40],
            "einox_approach": [3, 30],
            "einox_idle": [1, 20],
            "nox_characteristic": [50, 60],
            "nox_margin": [0.2, 0.1],
        }
    )

    columns_to_extract = ["uid", "engine", "nox_characteristic", "nox_margin"]

    expected_databank = pd.DataFrame(
        {
            "uid": ["uid_1", "uid_2"],
            "engine": ["engine_1", "engine_2"],
            "nox_characteristic": [50, 60],
            "nox_margin": [0.2, 0.1],
        }
    )

    # Act
    cleaned_databank = (
        clean_icao_databanks._extract_certification_data_from_icao_databank(
            databank, columns_to_extract
        )
    )

    # Assert
    assert cleaned_databank.equals(expected_databank)
