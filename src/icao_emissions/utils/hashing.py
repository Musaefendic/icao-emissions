"""Helper function related to hash key generation and verification."""

import hashlib
import importlib.resources
from typing import Dict, List, NoReturn

import yaml
from icao_emissions.exceptions.data_resources import DataResourceMissingError
from icao_emissions.exceptions.hashing import (
    HashKeysFileMissingError,
    PatternNotFoundError,
)


def get_hash_config() -> Dict[str, List[str]]:
    """Returns a dictionary with resources to be hashed."""
    # Init
    repository = "data.verification"
    filename = "hash_config.yaml"

    # Evaluate if the resource exists
    if not importlib.resources.is_resource(repository, filename):
        raise DataResourceMissingError(repository, filename)

    # Import the file
    with importlib.resources.open_binary(repository, filename) as infile:
        preliminary_config = yaml.safe_load(infile)

    # Update the config file
    return _populate_config_with_files_to_hash(preliminary_config)


def _populate_config_with_files_to_hash(
    preliminary_config: Dict[str, List[str]],
) -> Dict[str, List[str]]:
    """Extract files that need to be hashed."""
    # init
    hash_config: Dict[str, List[str]] = {}

    # search files to hash based on user input
    for repository, request_files in preliminary_config.items():
        # add a new key
        hash_config[repository] = []
        # list all files within the specified repository
        files = list(importlib.resources.contents(repository))

        for pattern in request_files:
            files_to_hash = [
                filename for filename in files if pattern in filename
            ]
            # Raise error if no files match the pattern
            if not files_to_hash:
                raise PatternNotFoundError(repository, files, pattern)
            # Save results
            hash_config[repository].extend(files_to_hash)

    return hash_config


def get_hash_keys() -> Dict[str, Dict[str, str]]:
    """Returns a dictionary with files and their hash keys."""
    # Init
    repository = "data.verification"
    resource = "hash_keys.yaml"

    # Evaluate if the resource exists
    if not importlib.resources.is_resource(repository, resource):
        raise HashKeysFileMissingError

    # Import the file
    with importlib.resources.open_binary(repository, resource) as infile:
        return yaml.safe_load(infile)


def generate_hash_keys() -> Dict[str, Dict[str, str]]:
    """Hash keys generation from 'hash_config.yaml'."""
    # Init
    hash_keys: Dict[str, Dict[str, str]] = {}

    # load config
    hash_config = get_hash_config()

    # compute hash key
    for repository, files in hash_config.items():
        # add a new entry
        hash_keys[repository] = {}
        # loop over to generate keys
        for filename in files:
            hash_keys[repository][filename] = compute_key(repository, filename)

    return hash_keys


def compute_key(repository, filename) -> str:
    """Read file as stream and compute hash key, based on hashlib.sha256."""
    hasher = hashlib.sha256()

    with importlib.resources.open_binary(repository, filename) as infile:
        while True:
            chunk = infile.read(hasher.block_size)
            if not chunk:
                break
            hasher.update(chunk)

    return hasher.hexdigest()
