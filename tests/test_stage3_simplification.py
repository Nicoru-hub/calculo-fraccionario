import pytest
from calculus.simplification.simplifier import simplify_expression
from calculus.expressions.base import Number, Variable
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.constants.constants import pi, e
from fractions import Fraction


def test_add_identity_left_zero():
    expr = Add(Number(0), Variable("x"))
    result = simplify_expression(expr)
    assert result == Variable("x")


def test_add_identity_right_zero():
    expr = Add(Variable("x"), Number(0))
    result = simplify_expression(expr)
    assert result == Variable("x")


def test_mul_identity_left_one():
    expr = Mul(Number(1), Variable("x"))
    result = simplify_expression(expr)
    assert result == Variable("x")


def test_mul_identity_right_one():
    expr = Mul(Variable("x"), Number(1))
    result = simplify_expression(expr)
    assert result == Variable("x")


def test_mul_zero_left():
    expr = Mul(Number(0), Variable("x"))
    result = simplify_expression(expr)
    assert result == Number(0)


def test_mul_zero_right():
    expr = Mul(Variable("x"), Number(0))
    result = simplify_expression(expr)
    assert result == Number(0)


def test_div_zero_numerator():
    expr = Div(Number(0), Variable("x"))
    result = simplify_expression(expr)
    assert result == Number(0)


def test_sub_identity():
    expr = Sub(Variable("x"), Variable("x"))
    result = simplify_expression(expr)
    assert result == Number(0)


def test_power_exponent_one():
    expr = Pow(Variable("x"), Number(1))
    result = simplify_expression(expr)
    assert result == Variable("x")


def test_power_exponent_zero():
    expr = Pow(Variable("x"), Number(0))
    result = simplify_expression(expr)
    assert result == Number(1)


def test_power_base_zero():
    expr = Pow(Number(0), Variable("x"))
    result = simplify_expression(expr)
    assert result == Number(0)


def test_power_base_one():
    expr = Pow(Number(1), Variable("x"))
    result = simplify_expression(expr)
    assert result == Number(1)


def test_combine_constants():
    expr = Add(Number(2), Number(3))
    result = simplify_expression(expr)
    assert isinstance(result, Number)
    assert result.value == Fraction(5)


def test_combine_constants_mul():
    expr = Mul(Number(2), Number(3))
    result = simplify_expression(expr)
    assert isinstance(result, Number)
    assert result.value == Fraction(6)


def test_complex_simplification():
    # (x * 0) + 5
    expr = Add(Mul(Variable("x"), Number(0)), Number(5))
    result = simplify_expression(expr)
    assert result == Number(5)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
