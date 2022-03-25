class MeasureSoftGramCliException(Exception):
    """Base MeasureSoftGram Cli exception"""
    pass


class FileNotFound(MeasureSoftGramCliException):
    """Raised when a invalid file path is provided to the MeasureSoftGram"""
    pass
