import pytest
from calculus.parser.parser import Parser
from calculus.differentiation.rules import differentiate
from calculus.expressions.base import Number, Variable
from calculus.expressions.operations import Pow, Add, Mul


def test_differentiate_constant():
    expr = Number(42)
    result = differentiate(expr, "x")
    assert result == Number(0)


def test_differentiate_variable():
    expr = Variable("x")
    result = differentiate(expr, "x")
    assert result == Number(1)


def test_differentiate_power():
    expr = Parser.parse("x^2")
    result = differentiate(expr, "x")
    assert isinstance(result, Mul)


def test_differentiate_sum():
    expr = Parser.parse("x + 2")
    result = differentiate(expr, "x")
    assert result == Number(1)


def test_differentiate_product():
    expr = Parser.parse("x * x")
    result = differentiate(expr, "x")
    assert isinstance(result, Add)


def test_differentiate_sin():
    from calculus.expressions.functions import Sin
    expr = Sin(Variable("x"))
    result = differentiate(expr, "x")
    assert isinstance(result, Mul)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
