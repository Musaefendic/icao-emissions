"""Exceptions related to the ICAO databank resources."""

from typing import List


class NoRawDatabankFoundError(Exception):
    """Exception raised when the raw ICAO databank has not been found."""

    def __init__(self):
        error_message = """
        No raw ICAO databank found!

        Please:
            - Download the emissions databank from ICAO website
            - https://www.easa.europa.eu/domains/environment/icao-aircraft-engine-emissions-databank  # noqa
            - Store the downloaded file in the repository: 'data/icao_databank/raw'  # noqa
        """

        super().__init__(error_message)


class MultipleRawDatankFoundError(Exception):
    """Exception raised when multiple raw ICAO databanks have been found."""

    def __init__(self, icao_files: List[str]):
        error_message = """
        Multiple ICAO databank were found in the repository:
                - {files}
        Only one excel file should be stored.
        """.format(
            files="\n\t\t- ".join(icao_files),
        )

        super().__init__(error_message)


class EmissionNotSupportedError(Exception):
    """Exception raised when importing a databank."""

    def __init__(self, emission: str):
        error_message = """
        The argument {0} is not supported

        Please provided one of the two following arguments
            - gaseous
            - nvpm
        """.format(
            emission,
        )

        super().__init__(error_message)
