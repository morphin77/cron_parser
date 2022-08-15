class WrongTypeException(Exception):
    def __init__(self, msg="Expression must be string"):
        super().__init__(msg)


class WrongLengthException(Exception):
    def __init__(self, msg="Expression does not match the format"):
        super().__init__(msg)


class SymbolNotAllowedException(Exception):
    def __init__(self, msg="Expression contains not allowed symbols"):
        super().__init__(msg)


class StepNotAllowedException(Exception):
    def __init__(self, msg="Expression contains not allowed step"):
        super().__init__(msg)
