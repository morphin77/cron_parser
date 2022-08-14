class WrongTypeException(Exception):
    msg = "Expression must be string"


class WrongLengthException(Exception):
    msg = "Expression does not match the format"


class ExpressionNotCheckedException(Exception):
    msg = "Expression does not match the format"
