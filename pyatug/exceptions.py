# Exceptions
class AutoUnitGeneratorBaseException(Exception):
    pass

class WrongTypeError(AutoUnitGeneratorBaseException):
    pass

class EmptyValueError(AutoUnitGeneratorBaseException):
    pass

class AUGSyntaxError(AutoUnitGeneratorBaseException):
    pass