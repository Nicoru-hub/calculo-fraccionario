import pytest
from calculus.differentiation.rules import differentiate
from calculus.parser.parser import Parser
from calculus.expressions.base import Number, Variable
from calculus.expressions.operations import Mul, Add, Pow
from calculus.expressions.functions import Sin, Cos, Exp, Ln
from calculus.constants.constants import pi, e
from fractions import Fraction


def test_derivative_constant():
    expr = Number(5)
    result = differentiate(expr, "x")
    assert result == Number(0)


def test_derivative_variable():
    expr = Variable("x")
    result = differentiate(expr, "x")
    assert result == Number(1)


def test_derivative_constant_pi():
    expr = pi
    result = differentiate(expr, "x")
    assert result == Number(0)


def test_derivative_sum():
    expr = Add(Variable("x"), Number(2))
    result = differentiate(expr, "x")
    assert result == Number(1)


def test_derivative_power_x_squared():
    # d/dx(x^2) = 2x
    expr = Pow(Variable("x"), Number(2))
    result = differentiate(expr, "x")
    # Result should simplify to 2*x
    assert isinstance(result, Mul)


def test_derivative_power_x_cubed():
    # d/dx(x^3) = 3x^2
    expr = Pow(Variable("x"), Number(3))
    result = differentiate(expr, "x")
    assert isinstance(result, Mul)


def test_derivative_sin():
    # d/dx(sin(x)) = cos(x)
    expr = Sin(Variable("x"))
    result = differentiate(expr, "x")
    assert isinstance(result, Cos)


def test_derivative_cos():
    # d/dx(cos(x)) = -sin(x)
    expr = Cos(Variable("x"))
    result = differentiate(expr, "x")
    # Result should be -sin(x)
    from calculus.expressions.operations import Neg
    assert isinstance(result, Neg)


def test_derivative_exp():
    # d/dx(e^x) = e^x
    expr = Exp(Variable("x"))
    result = differentiate(expr, "x")
    assert isinstance(result, Exp)


def test_derivative_ln():
    # d/dx(ln(x)) = 1/x
    expr = Ln(Variable("x"))
    result = differentiate(expr, "x")
    from calculus.expressions.operations import Div
    assert isinstance(result, Div)


def test_derivative_product():
    # d/dx(x * sin(x)) = sin(x) + x*cos(x)
    expr = Mul(Variable("x"), Sin(Variable("x")))
    result = differentiate(expr, "x")
    assert isinstance(result, Add)


def test_derivative_parsed_expression():
    # Test with parsed expression: x^2
    expr = Parser.parse("x^2")
    result = differentiate(expr, "x")
    # d/dx(x^2) = 2x
    assert isinstance(result, Mul)


def test_derivative_parsed_sin():
    # Test with parsed expression: sin(x)
    expr = Parser.parse("sin(x)")
    result = differentiate(expr, "x")
    assert isinstance(result, Cos)


def test_derivative_pi_x_squared():
    # d/dx(pi*x^2) = 2*pi*x
    expr = Parser.parse("pi*x^2")
    result = differentiate(expr, "x")
    # Should be 2*pi*x
    assert isinstance(result, Mul)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
