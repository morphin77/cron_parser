from cron_parser.exceptions.expression_exceptions import *


class ValidateResult:
    valid: bool
    reason: Exception | None

    def __init__(self, valid: bool, reason: Exception = None):
        self.valid = valid
        self.reason = reason


class Validator:
    __value: str
    __valid: bool = None
    __reasons: list[Exception | None] = []

    def __init__(self, value: str):
        self.value = value
        self.__validate()

    def is_valid(self) -> bool:
        return self.__valid

    def reasons(self) -> list[Exception | None]:
        return self.__reasons

    def __validate(self) -> None:
        check_type_res: ValidateResult = self.__validate_type_expression()
        if not check_type_res.valid:
            self.__valid = False
            self.__reasons.append(check_type_res.reason)
            return

        check_len_res: ValidateResult = self.__validate_length_expression()
        if not check_len_res.valid:
            self.__valid = False
            self.__reasons.append(check_type_res.reason)
            return

        # if pass all checks
        self.__valid = True

    def __validate_type_expression(self) -> ValidateResult:
        if isinstance(self.value, str):
            return ValidateResult(valid=True)
        else:
            return ValidateResult(valid=False, reason=WrongTypeException())

    def __validate_length_expression(self) -> ValidateResult:
        length = len(self.value.split(" "))
        if length in (5, 6):
            return ValidateResult(valid=True)
        else:
            return ValidateResult(valid=False, reason=WrongLengthException())
