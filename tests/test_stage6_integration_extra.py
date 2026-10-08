import pytest
from calculus.integration.rules import integrate
from calculus.parser.parser import Parser
from calculus.expressions.base import Number, Variable
from calculus.expressions.functions import Sin, Cos
from calculus.expressions.operations import Pow, Add


def test_integrate_polynomial():
    expr = Parser.parse("x^2")
    result = integrate(expr, "x")
    assert isinstance(result, Add)


def test_integrate_sine():
    expr = Parser.parse("sin(x)")
    result = integrate(expr, "x")
    assert isinstance(result, Add)


def test_integrate_cosine():
    expr = Parser.parse("cos(x)")
    result = integrate(expr, "x")
    assert isinstance(result, Add)


def test_integrate_sum():
    expr = Parser.parse("x + 2")
    result = integrate(expr, "x")
    assert isinstance(result, Add)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
