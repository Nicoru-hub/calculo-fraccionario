import pytest
from calculus.expressions.base import Number, Variable, Constant, Integer, Rational
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import Sin, Cos, Exp, Ln, Sqrt
from calculus.constants.constants import pi, e, phi
from fractions import Fraction


def test_number_integer():
    n = Number(5)
    assert n.value == Fraction(5, 1)
    assert str(n) == "5"


def test_number_fraction():
    n = Number(Fraction(3, 4))
    assert n.value == Fraction(3, 4)
    assert str(n) == "3/4"


def test_number_float_to_rational():
    n = Number(0.5)
    assert n.value == Fraction(1, 2)
    assert str(n) == "1/2"


def test_variable():
    x = Variable("x")
    assert x.name == "x"
    assert str(x) == "x"


def test_constant_pi():
    assert str(pi) == "π"


def test_constant_e():
    assert str(e) == "e"


def test_constant_phi():
    assert str(phi) == "φ"


def test_add():
    x = Variable("x")
    n = Number(2)
    expr = Add(x, n)
    assert str(expr) == "(x + 2)"


def test_sub():
    x = Variable("x")
    n = Number(3)
    expr = Sub(x, n)
    assert str(expr) == "(x - 3)"


def test_mul():
    x = Variable("x")
    n = Number(2)
    expr = Mul(n, x)
    assert str(expr) == "(2 * x)"


def test_div():
    x = Variable("x")
    n = Number(2)
    expr = Div(x, n)
    assert str(expr) == "(x / 2)"


def test_pow():
    x = Variable("x")
    n = Number(2)
    expr = Pow(x, n)
    assert str(expr) == "(x^2)"


def test_neg():
    x = Variable("x")
    expr = Neg(x)
    assert str(expr) == "(-x)"


def test_sin():
    x = Variable("x")
    expr = Sin(x)
    assert str(expr) == "sin(x)"


def test_cos():
    x = Variable("x")
    expr = Cos(x)
    assert str(expr) == "cos(x)"


def test_exp():
    x = Variable("x")
    expr = Exp(x)
    assert str(expr) == "exp(x)"


def test_ln():
    x = Variable("x")
    expr = Ln(x)
    assert str(expr) == "ln(x)"


def test_sqrt():
    x = Variable("x")
    expr = Sqrt(x)
    assert str(expr) == "sqrt(x)"


def test_complex_expression():
    x = Variable("x")
    expr = Add(Mul(Number(2), Pow(x, Number(3))), Number(1))
    # str representation: (2 * (x^3)) + 1
    assert "x" in str(expr)
    assert "^3" in str(expr)


def test_operator_overloading():
    x = Variable("x")
    n = Number(2)

    expr1 = x + n
    assert isinstance(expr1, Add)

    expr2 = x - n
    assert isinstance(expr2, Sub)

    expr3 = x * n
    assert isinstance(expr3, Mul)

    expr4 = x / n
    assert isinstance(expr4, Div)

    expr5 = x ** n
    assert isinstance(expr5, Pow)

    expr6 = -x
    assert isinstance(expr6, Neg)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
