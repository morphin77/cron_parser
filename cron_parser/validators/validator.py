from cron_parser.exceptions.expression_exceptions import *


class ValidateResult:
    valid: bool
    reason: Exception | None

    def __init__(self, valid: bool, reason: Exception = None):
        self.valid = valid
        self.reason = reason


# validate values with `/`
def validate_step_sign(value: str, range_of_step: int) -> list[ValidateResult]:
    result = []
    if '/' not in value:
        return result
    parts = value.split('/')
    allowed_values = [str(el) for el in range(1, range_of_step) if range_of_step % el == 0]
    if parts[0] != '*':
        result.append(
            ValidateResult(
                valid=False,
                reason=SymbolNotAllowedException(msg=f"Using {parts[0]} not allowed before '/' delimiter")
            )
        )
    if parts[1] not in allowed_values:
        result.append(
            ValidateResult(
                valid=False,
                reason=SymbolNotAllowedException(msg=f"Using {parts[1]} not allowed after '/' in this place")
            )
        )
    if len(result) == 0:
        return [ValidateResult(valid=True)]
    else:
        return result


# validate values with `-`
def validate_range_sign(value: str, range_of_step: int) -> list[ValidateResult]:
    result = []
    if '-' not in value:
        return result
    parts = value.split('-')
    allowed_values = [str(el) for el in range(0, range_of_step)]
    if not parts[0] or parts[0] not in allowed_values:
        result.append(
            ValidateResult(
                valid=False,
                reason=SymbolNotAllowedException(msg=f"Using {parts[0]} not allowed before '-' delimiter")
            )
        )
        return result
    if not parts[1] or parts[1] not in allowed_values:
        result.append(
            ValidateResult(
                valid=False,
                reason=SymbolNotAllowedException(msg=f"Using {parts[1]} not allowed after '-' in this place")
            )
        )
        return result
    if parts[0] and parts[1] and int(parts[0]) >= int(parts[1]):
        result.append(
            ValidateResult(
                valid=False,
                reason=SymbolNotAllowedException(msg=f"Range {value} cannot be calculated")
            )
        )
        return result
    if len(result) == 0:
        return [ValidateResult(valid=True)]
    else:
        return result


# validate values with `,`
def validate_array_sign(value: str, range_of_step: int) -> list[ValidateResult]:
    result = []
    if ',' not in value:
        return result
    parts = value.split(',')
    allowed_values = [str(el) for el in range(0, range_of_step)]
    if not parts[0] or parts[0] not in allowed_values:
        result.append(
            ValidateResult(
                valid=False,
                reason=SymbolNotAllowedException(msg=f"Using {parts[0]} not allowed before ',' delimiter")
            )
        )
        return result
    if not parts[-1] or parts[-1] not in allowed_values:
        result.append(
            ValidateResult(
                valid=False,
                reason=SymbolNotAllowedException(msg=f"Using {parts[1]} not allowed after ',' in this place")
            )
        )
        return result
    for el in parts:
        if el not in allowed_values:
            result.append(
                ValidateResult(
                    valid=False,
                    reason=SymbolNotAllowedException(msg=f"Element {el} can not be used in value {value}")
                )
            )
        return result
    if len(result) == 0:
        return [ValidateResult(valid=True)]
    else:
        return result


class Validator:
    __value: str
    __valid: bool = None
    __reasons: list[Exception | None]

    def __init__(self, value: str):
        self.value = value
        self.__validate()

    def is_valid(self) -> bool:
        return self.__valid

    def reasons(self) -> list[Exception | None]:
        return self.__reasons

    def __validate(self) -> None:
        self.__reasons = []
        check_type_res: ValidateResult = self.__validate_type_expression()
        if not check_type_res.valid:
            self.__valid = False
            self.__reasons.append(check_type_res.reason)
            return

        check_len_res: ValidateResult = self.__validate_length_expression()
        if not check_len_res.valid:
            self.__valid = False
            self.__reasons.append(check_len_res.reason)
            return

        check_minutes: list[ValidateResult] = [el for el in self.__validate_minutes() if not el.valid]
        if len(check_minutes) > 0:
            self.__valid = False
            self.__reasons += [el.reason for el in check_minutes]
            return

        # if pass all checks
        if len(self.__reasons) == 0:
            self.__valid = True

    def __validate_type_expression(self) -> ValidateResult:
        if isinstance(self.value, str):
            return ValidateResult(valid=True)
        else:
            return ValidateResult(valid=False, reason=WrongTypeException())

    def __validate_length_expression(self) -> ValidateResult:
        length = len(self.value.split())
        if length in (5, 6):
            return ValidateResult(valid=True)
        else:
            return ValidateResult(valid=False, reason=WrongLengthException())

    def __validate_minutes(self) -> list[ValidateResult]:
        result: list[ValidateResult] = []
        result += self.__validate_minutes_available_symbols()
        result += validate_step_sign(self.value.split(" ")[0], 60)
        result += validate_range_sign(self.value.split(" ")[0], 60)
        result += validate_array_sign(self.value.split(" ")[0], 60)
        return result

    def __validate_minutes_available_symbols(self) -> list[ValidateResult]:
        result = []
        minutes = self.value.split()[0]
        allowed_characters = ['*', '/', '-', ','] + [str(el) for el in range(0, 59)]
        for symbol in minutes:
            if symbol not in allowed_characters:
                result.append(
                    ValidateResult(
                        valid=False,
                        reason=SymbolNotAllowedException(msg=f"Symbol {symbol} not allowed in minutes section")
                    )
                )
        if len(result) == 0:
            return [ValidateResult(valid=True)]
        else:
            return result
