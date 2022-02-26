"""Tests to verify hashing functionalties."""
from typing import List

import pytest
from icao_emissions.exceptions.data_resources import DataResourceMissingError
from icao_emissions.exceptions.hashing import HashKeysFileMissingError
from icao_emissions.utils import hashing


def test_files_to_hash_exists(mocker):
    """Ensure that the config file 'hash_config.yaml' exists."""
    # Assert n°1 - Verify the file exists
    files_to_hash = hashing.get_hash_config()
    assert isinstance(files_to_hash, dict)

    # Assert n°2 - a error is raised if the file doesn't exist
    with pytest.raises(DataResourceMissingError):
        mocker.patch("importlib.resources.is_resource", return_value=False)
        hashing.get_hash_config()


def test_file_with_hash_keys_exits(mocker):
    """Ensure that file with hash keys exists."""
    # Assert n1 -
    hash_keys = hashing.get_hash_keys()
    assert isinstance(hash_keys, dict)

    # Assert n°2 - a error is raised if the file doesn't exist
    with pytest.raises(HashKeysFileMissingError):
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


def test_tracked_files_unaltered():
    """Checks tracked files are unaltered."""
    # Arange
    hash_keys_imported = hashing.get_hash_keys()

    # Act
    hash_keys_computed = hashing.generate_hash_keys()

    # Assert
    assert hash_keys_computed == hash_keys_imported
