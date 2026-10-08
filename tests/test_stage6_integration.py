import pytest
from calculus.integration.rules import integrate
from calculus.parser.parser import Parser
from calculus.expressions.base import Number, Variable, Constant
from calculus.expressions.operations import Pow, Div, Mul, Add, Neg
from calculus.expressions.functions import Ln, Cos, Sin, Exp
from fractions import Fraction


def test_integrate_constant():
    expr = Number(5)
    result = integrate(expr, "x")
    assert isinstance(result, Add)


def test_integrate_variable():
    expr = Variable("x")
    result = integrate(expr, "x")
    assert isinstance(result, Add)


def test_integrate_power_x_squared():
    # ∫ x^2 dx = x^3/3 + C
    expr = Pow(Variable("x"), Number(2))
    result = integrate(expr, "x")
    assert isinstance(result, Add)


def test_integrate_power_x_cubed():
    # ∫ x^3 dx = x^4/4 + C
    expr = Pow(Variable("x"), Number(3))
    result = integrate(expr, "x")
    assert isinstance(result, Add)


def test_integrate_power_inverse():
    # ∫ x^(-1) dx = ln(x) + C
    expr = Pow(Variable("x"), Number(-1))
    result = integrate(expr, "x")
    assert isinstance(result, Add)
    assert isinstance(result.left, Ln)


def test_integrate_sin():
    # ∫ sin(x) dx = -cos(x) + C
    expr = Sin(Variable("x"))
    result = integrate(expr, "x")
    assert isinstance(result, Add)


def test_integrate_cos():
    # ∫ cos(x) dx = sin(x) + C
    expr = Cos(Variable("x"))
    result = integrate(expr, "x")
    assert isinstance(result, Add)


def test_integrate_exp():
    # ∫ e^x dx = e^x + C
    expr = Exp(Variable("x"))
    result = integrate(expr, "x")
    assert isinstance(result, Add)
    assert isinstance(result.left, Exp)


def test_integrate_parsed_expression():
    # Test with parsed expression: x^2
    expr = Parser.parse("x^2")
    result = integrate(expr, "x")
    assert isinstance(result, Add)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
