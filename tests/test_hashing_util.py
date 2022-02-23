"""Tests to verify hashing functionalties."""
import hashlib
import importlib.resources
from typing import List

import pytest
from icao_emissions.utils import hashing


def test_files_to_hash_exists(mocker):
    """Ensure that the config file 'hash_config.yaml' exists."""
    # Assert n°1 - Verify the file exists
    files_to_hash = hashing.get_hash_config()
    assert isinstance(files_to_hash, dict)

    # Assert n°2 - a error is raised if the file doesn't exist
    with pytest.raises(ValueError):
        mocker.patch("importlib.resources.is_resource", return_value=False)
        hashing.get_hash_config()


def test_file_with_hash_keys_exits(mocker):
    """Ensure that file with hash keys exists."""
    # Assert n1 -
    hash_keys = hashing.get_hash_keys()
    assert isinstance(hash_keys, dict)

    # Assert n°2 - a error is raised if the file doesn't exist
    with pytest.raises(ValueError):
        mocker.patch("importlib.resources.is_resource", return_value=False)
        hashing.get_hash_keys()


def test_yaml_format_hash_config():
    """Check that the format of 'hash_config.yaml' is correct."""
    # Arange
    hash_config = hashing.get_hash_config()

    # Assert
    for _, files_to_hash in hash_config.items():
        assert isinstance(files_to_hash, List)
        assert files_to_hash  # list of files to hash is not empty


def test_yaml_format_file_with_hash_keys():
    """Check the format of 'hash_keys.yaml' file is as expected."""
    # Arange
    hash_keys = hashing.get_hash_keys()

    # Assert
    for repository, hash_group in hash_keys.items():
        for filename, hash_key in hash_group.items():
            # the hashed file exists
            assert importlib.resources.is_resource(repository, filename)

            # the has key is filled in
            assert isinstance(hash_key, str)
            assert hash_key  # the value is not empty


def test_generate_hash_keys_based_on_hash_config(mocker):
    """Verify the generation of 'hash_keys'."""
    # Init
    hasher = hashlib.sha256()

    # mock content
    mock_filename = "mocked.yaml"
    mock_content = b"this_str_is_a_mock"

    expected_hash = (
        "644287d8a88dcba2244bd0ab85de2a9db59ccd40fc75f8b3cf4600b139ea1dd8"
    )

    # Compute the hash key
    hasher.update(mock_content)
    mocked_hash = hasher.hexdigest()
    # Mock the result from reading -> hash_config.yaml
    mocked_hash_config = {
        "data.icao_databank.configs": [mock_filename],
        "data.icao_databank.raw": [mock_filename],
    }

    # Expected results
    expected_hash_keys = {
        "data.icao_databank.configs": {mock_filename: expected_hash},
        "data.icao_databank.raw": {mock_filename: expected_hash},
    }

    # Time to patch
    mocker.patch(
        "icao_emissions.utils.hashing.get_hash_config",
        return_value=mocked_hash_config,
    )
    mocker.patch(
        "icao_emissions.utils.hashing.compute_key",
        return_value=mocked_hash,
    )

    # Act & Assert
    hash_keys = hashing.generate_hash_keys()
    assert hash_keys == expected_hash_keys


def test_tracked_files_unaltered():
    """Checks tracked files are unaltered."""
    # Arange
    hash_keys_imported = hashing.get_hash_keys()

    # Act
    hash_keys_computed = hashing.generate_hash_keys()

    # Assert
    assert hash_keys_computed == hash_keys_imported
