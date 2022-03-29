class MeasureSoftGramCLIException(Exception):
    ''' Base MeasureSoftGram CLI Exception '''
    pass

class InvalidMetricException(MeasureSoftGramCLIException):
    ''' Raised when an invalid metric value is provided '''
    pass

class InvalidSonarFileAttributeException(MeasureSoftGramCLIException):
    ''' Raised when an sonar file attribute is incorrect '''
    pass

class InvalidBaseComponentException(MeasureSoftGramCLIException):
    ''' Raised when the field baseComponent from sonar metrics file is incorrect '''
    pass

class InvalidFileTypeException(MeasureSoftGramCLIException):
    '''' Raised when the file type is not JSON '''
    pass
