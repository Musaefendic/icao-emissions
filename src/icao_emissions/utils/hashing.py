"""Helper function related to hash key generation and verification."""

import hashlib
import importlib.resources
from typing import Dict, List, NoReturn

import yaml


def _raise_exception_if_resource_not_found(resource: str) -> NoReturn:
    """Raise an exception if a file related to the hash util is missing."""
    message = """
        The following file is missing:
        - {resource}
    """.format(
        resource=resource,
    )

    raise ValueError(message)


def _raise_warning_pattern_not_found_during_file_search(
    repository: str,
    files: List[str],
    pattern: str,
) -> NoReturn:
    """Raise a warning if no files matches the searched pattern."""
    message = """
        When building the hash config file
            - Function called: hashing.get_hash_config()

        Within the file 'data/verification/hash_config.yaml'
            - This pattern has been defined: {pattern}

        No files found that match the search pattern
            - Pattern: {pattern}

            - Repository: {repository}
            - Files: {files}

        To resolve this warning, please:
            - Edit the file: 'data/verification/hash_config.yaml'
    """.format(
        repository=repository,
        files=files,
        pattern=pattern,
    )
    raise Warning(message)


def _raise_exception_if_hash_keys_not_found() -> None:
    message = """
        The file 'hash_keys.yaml' is missing.

        The file can be obtained as follows:
            - Go to the directory: data/verification
            - From the terminal, enter the following command:
            >> python -m generate_hash_keys
    """
    raise ValueError(message)


def get_hash_config() -> Dict[str, List[str]]:
    """Returns a dictionary with resources to be hashed."""
    # Init
    repository = "data.verification"
    resource = "hash_config.yaml"

    # Evaluate if the resource exists
    if not importlib.resources.is_resource(repository, resource):
        _raise_exception_if_resource_not_found(resource)

    # Import the file
    with importlib.resources.open_binary(repository, resource) as infile:
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
            # don't save result if empty
            if not files_to_hash:
                _raise_warning_pattern_not_found_during_file_search(
                    repository,
                    files,
                    pattern,
                )
            hash_config[repository].extend(files_to_hash)

    return hash_config


def get_hash_keys() -> Dict[str, Dict[str, str]]:
    """Returns a dictionary with files and their hash keys."""
    # Init
    repository = "data.verification"
    resource = "hash_keys.yaml"

    # Evaluate if the resource exists
    if not importlib.resources.is_resource(repository, resource):
        _raise_exception_if_hash_keys_not_found()

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
