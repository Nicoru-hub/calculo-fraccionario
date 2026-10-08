import pytest
from calculus.parser.parser import Parser
from calculus.expressions.base import Number, Variable, Constant
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import Sin, Cos, Exp, Ln, Sqrt
from calculus.constants.constants import pi, e, phi
from fractions import Fraction


def test_parse_number():
    expr = Parser.parse("5")
    assert isinstance(expr, Number)
    assert expr.value == Fraction(5)


def test_parse_number_fraction():
    expr = Parser.parse("0.5")
    assert isinstance(expr, Number)
    assert expr.value == Fraction(1, 2)


def test_parse_variable():
    expr = Parser.parse("x")
    assert isinstance(expr, Variable)
    assert expr.name == "x"


def test_parse_constant_pi():
    expr = Parser.parse("pi")
    assert expr == pi


def test_parse_constant_e():
    expr = Parser.parse("e")
    assert expr == e


def test_parse_addition():
    expr = Parser.parse("x + 2")
    assert isinstance(expr, Add)
    assert isinstance(expr.left, Variable)
    assert isinstance(expr.right, Number)


def test_parse_subtraction():
    expr = Parser.parse("x - 3")
    assert isinstance(expr, Sub)
    assert isinstance(expr.left, Variable)
    assert isinstance(expr.right, Number)


def test_parse_multiplication():
    expr = Parser.parse("2 * x")
    assert isinstance(expr, Mul)
    assert isinstance(expr.left, Number)
    assert isinstance(expr.right, Variable)


def test_parse_division():
    expr = Parser.parse("x / 2")
    assert isinstance(expr, Div)
    assert isinstance(expr.left, Variable)
    assert isinstance(expr.right, Number)


def test_parse_power():
    expr = Parser.parse("x^2")
    assert isinstance(expr, Pow)
    assert isinstance(expr.base, Variable)
    assert isinstance(expr.exponent, Number)


def test_parse_power_double_star():
    expr = Parser.parse("x**3")
    assert isinstance(expr, Pow)


def test_parse_negation():
    expr = Parser.parse("-x")
    assert isinstance(expr, Neg)
    assert isinstance(expr.expr, Variable)


def test_parse_sin():
    expr = Parser.parse("sin(x)")
    assert isinstance(expr, Sin)
    assert isinstance(expr.arguments[0], Variable)


def test_parse_cos():
    expr = Parser.parse("cos(x)")
    assert isinstance(expr, Cos)


def test_parse_exp():
    expr = Parser.parse("exp(x)")
    assert isinstance(expr, Exp)


def test_parse_ln():
    expr = Parser.parse("ln(x)")
    assert isinstance(expr, Ln)


def test_parse_sqrt():
    expr = Parser.parse("sqrt(x)")
    assert isinstance(expr, Sqrt)


def test_parse_complex_expression():
    expr = Parser.parse("2 * x^3 + 1")
    assert isinstance(expr, Add)
    assert isinstance(expr.left, Mul)


def test_parse_parentheses():
    expr = Parser.parse("(x + 1) * (x - 1)")
    assert isinstance(expr, Mul)


def test_parse_nested_functions():
    expr = Parser.parse("sin(cos(x))")
    assert isinstance(expr, Sin)
    assert isinstance(expr.arguments[0], Cos)


def test_parse_pi_x_squared():
    expr = Parser.parse("pi*x^2")
    assert isinstance(expr, Mul)
    assert expr.left == pi


def test_parse_e_power():
    expr = Parser.parse("e^x")
    assert isinstance(expr, Pow)
    assert expr.base == e


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
