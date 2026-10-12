import pytest
from calculus.simplification.simplifier import simplify_expression
from calculus.parser.parser import Parser
from calculus.expressions.base import Number, Variable
from calculus.expressions.operations import Add, Mul, Pow


def test_simplify_addition_with_zero():
    expr = Parser.parse("x + 0")
    result = simplify_expression(expr)
    assert result == Variable("x")


def test_simplify_multiplication_by_one():
    expr = Parser.parse("x * 1")
    result = simplify_expression(expr)
    assert result == Variable("x")


def test_simplify_multiplication_by_zero():
    expr = Parser.parse("x * 0")
    result = simplify_expression(expr)
    assert result == Number(0)


def test_simplify_power_zero():
    expr = Parser.parse("x^0")
    result = simplify_expression(expr)
    assert result == Number(1)


def test_simplify_power_one():
    expr = Parser.parse("x^1")
    result = simplify_expression(expr)
    assert result == Variable("x")


def test_simplify_numbers():
    expr = Parser.parse("2 + 3")
    result = simplify_expression(expr)
    assert result == Number(5)


def test_simplify_multiplication_numbers():
    expr = Parser.parse("3 * 4")
    result = simplify_expression(expr)
    assert result == Number(12)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
