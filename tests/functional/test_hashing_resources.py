import hashlib
import importlib.resources

from icao_emissions.utils import hashing


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
