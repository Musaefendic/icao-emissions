from typing import List


class PatternNotFoundError(Exception):
    """Exception raised when no file matches the search pattern."""

    def __init__(
        self,
        repository: str,
        files: List[str],
        pattern: str,
    ) -> None:
        error_message = """
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

        super().__init__(error_message)


class HashKeysFileMissingError(Exception):
    """Exception raised if the file 'hash_keys.yaml' is missing."""

    def __init__(self):
        error_message = """
        The file 'hash_keys.yaml' is missing.

        The file can be obtained as follows:
            - Go to the directory: data/verification
            - From the terminal, enter the following command:
            >> python -m generate_hash_keys
        """

        super().__init__(error_message)
