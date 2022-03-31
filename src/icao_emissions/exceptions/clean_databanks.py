"""Exceptions related to the cleaning of the ICAO databank."""


class VariablesNotInHeaderError(Exception):
    def __init__(self, header: set[str], columns_to_rename: set[str]):
        columns_not_found = columns_to_rename - header

        error_message = """
        Some variables are not contained in the dataframe header.

        Please check the name of the variables to rename.
        The variables that were not found are the following:
        
        {columns_not_found}
        """.format(
            columns_not_found=columns_not_found
        )

        super().__init__(error_message)


class UidNotFoundError(Exception):
    def __init__(self, databank_uid: set[str], uids_to_remove: set[str]):
        uids_not_found = uids_to_remove - databank_uid
        
        error_message = """
        Some uids are not contained in the dataframe. 

        Please check that the following uids are correctly written:

        {uids_not_found}
        """.format(uids_not_found=uids_not_found)

        super().__init__(error_message)
