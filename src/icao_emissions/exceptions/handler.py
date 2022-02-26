from icao_emissions.exceptions.icao_databank import NoRawDatabankFoundError

exceptions_available = {
    ("icao_emissions.databank.reader", ""): NoRawDatabankFoundError,
}


def catch_exceptions(func) -> None:
    def exception_triage(*args, **kwargs):
        print("")
        print("Function name: ", func.__name__)
        print("Module: ", func.__module__)
        print("")
        custom_exception = exceptions_available[func.__name__]
        error_message = """
        STOP
        """
        raise custom_exception(error_message)

    return exception_triage


@catch_exceptions
def add(a, b):
    return a + b


if __name__ == "__main__":
    add(1, 2)
