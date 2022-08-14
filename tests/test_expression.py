import pytest

from cron_parser.exceptions.expression_exceptions import *
from cron_parser.parser import Parser


@pytest.mark.expression_type
@pytest.mark.expression_length
@pytest.mark.parametrize(
    "expression",
    (  # correct formats
         "* * * * *",
         "* * * * * *",
         "*/30 * 1-5 * Mon-saT",
         "*/30 * 1,30 * Mon-saT",
         "*/30 * 1,30 * 1"
    )
)
def test_expression_type_must_be_valid(expression):
    result = Parser(expression)
    assert result.validator.is_valid() is True  # el is valid
    assert len(result.validator.reasons()) == 0  # reasons are not present


@pytest.mark.expression_type
@pytest.mark.parametrize("expression", (3, [], (), {}))
def test_expression_type_must_be_not_valid(expression):
    result = Parser(expression)
    assert result.validator.is_valid() is False  # el not valid
    assert len(result.validator.reasons()) > 0  # reasons are present
    # WrongTypeException reason are present
    assert len([el for el in result.validator.reasons() if isinstance(el, WrongTypeException)]) > 0


@pytest.mark.expression_length
@pytest.mark.parametrize("expression", ("* * * * * * *", "* * * *"))
def test_expression_length_must_be_not_valid(expression):
    result = Parser(expression)
    assert result.validator.is_valid() is False  # el not valid
    assert len(result.validator.reasons()) > 0  # reasons are present
    # WrongLengthException reason are present
    assert len([el for el in result.validator.reasons() if isinstance(el, WrongLengthException)]) > 0


@pytest.mark.skip(reason="not implemented yet")
@pytest.mark.expression_content
@pytest.mark.parametrize("expression", ("*!30 * 15 * Mon-saT", "*/30 * 15 * Mon?saT"))
def test_expression_length_must_be_not_valid(expression):
    result = Parser(expression)
    assert result.validator.is_valid() is False  # el not valid
    assert len(result.validator.reasons()) > 0  # reasons are present
    # WrongTypeException reason are present
    assert len([el for el in result.validator.reasons() if isinstance(el, WrongLengthException)]) > 0



