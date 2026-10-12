import pytest
from calculus.parser.parser import Parser
from calculus.expressions.base import Number, Variable
from calculus.expressions.operations import Pow, Mul, Add


def test_parse_number():
    expr = Parser.parse("42")
    assert isinstance(expr, Number)
    assert expr.value == 42


def test_parse_variable():
    expr = Parser.parse("x")
    assert isinstance(expr, Variable)
    assert expr.name == "x"


def test_parse_addition():
    expr = Parser.parse("x + 2")
    assert isinstance(expr, Add)


def test_parse_power():
    expr = Parser.parse("x^2")
    assert isinstance(expr, Pow)


def test_parse_complex_expression():
    expr = Parser.parse("2*x^3 + 3*x + 1")
    assert isinstance(expr, Add)


def test_parse_sin():
    from calculus.expressions.functions import Sin
    expr = Parser.parse("sin(x)")
    assert isinstance(expr, Sin)


def test_parse_pi_constant():
    expr = Parser.parse("pi")
    from calculus.expressions.base import Constant
    assert isinstance(expr, Constant)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
