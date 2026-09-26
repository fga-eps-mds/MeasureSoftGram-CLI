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


class InitFileAlreadyExists(MeasureSoftGramCLIException):
    """Raised when the init file already exists"""

    pass


class InvalidWeight(MeasureSoftGramCLIException):
    """Raised when a invalid weight is provided to the MeasureSoftGram"""

    pass


class InvalidMeasuresoftgramFormat(MeasureSoftGramCLIException):
    """Raised when a invalid format file is provided to the MeasureSoftGram"""

    pass


class RepositoryUrlNotFound(MeasureSoftGramCLIException):
    """
    Excessão lançada quando não é possível encontrar uma URL que contenha a
    substring do nome do arquivo
    """

    pass


class ConfigFileNotFound(MeasureSoftGramCLIException):
    """Raised when the .measuresoftgram file is not found"""

    pass


class ConfigFileQueryFailed(MeasureSoftGramCLIException):
    """Raised when the query is in the config file"""

    pass


class ConfigFileFormatInvalid(MeasureSoftGramCLIException):
    """Raised when the config file is invalid"""

    pass
