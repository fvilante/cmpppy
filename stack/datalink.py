


# ----------

class ErrorTypes(Enum):
    NO_ERROR = 0
    INVALID_CHECKSUM = 1

class Error(NamedTuple):
    hasError: bool
    type: ErrorTypes

class Report(NamedTuple):



def decodeFrame(frame) -> Result:
    pass

