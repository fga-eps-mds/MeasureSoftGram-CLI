class MeasureSoftGramCLIException(Exception):
    """Base MeasureSoftGram CLI Exception"""

    pass


class InvalidMetricException(MeasureSoftGramCLIException):
    """Raised when an invalid metric value is provided"""

    pass


class InvalidMetricsJsonFile(MeasureSoftGramCLIException):
    """Raised when the metrics file is invalid"""

    pass


class FileNotFound(MeasureSoftGramCLIException):
    """Raised when a file is not found"""

    pass


class UnableToOpenFile(MeasureSoftGramCLIException):
    """Raised when a file could not be opened"""

    pass


class UnableToReadFile(MeasureSoftGramCLIException):
    """Raised when a file could not be readed"""

    pass


class InvalidWeight(MeasureSoftGramCLIException):
    """Raised when a invalid weight is provided to the MeasureSoftGram"""

    pass


class InvalidMeasuresoftgramFormat(MeasureSoftGramCLIException):
    """Raised when a invalid format file is provided to the MeasureSoftGram"""

    pass
