"""Exceptions related to data resources."""


class DataResourceMissingError(Exception):
    def __init__(self, repository: str, filename: str) -> None:
        error_message = """
        The configuration file is missing.

        This configuraiton file is needed to clean the emissions databank.
        The file has been either removed or renamed.

        Please, verify that the file is present:
            - repository: {repository}
            - file: {filename}

        In case the file is missing, refer to an older commit.
        """.format(
            repository=repository,
            filename=filename,
        )

        super().__init__(error_message)
