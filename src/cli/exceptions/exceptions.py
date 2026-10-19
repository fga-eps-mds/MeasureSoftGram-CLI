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
