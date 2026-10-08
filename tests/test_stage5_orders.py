import pytest
from calculus.differentiation.order import evaluate_order
from calculus.parser.parser import Parser
from calculus.expressions.base import Number, Variable
from calculus.expressions.operations import Pow


def test_order_zero():
    expr = Parser.parse("x^2")
    result = evaluate_order(expr, 0)
    assert result == expr


def test_order_positive_integer():
    expr = Parser.parse("x^3")
    result = evaluate_order(expr, 1)
    assert result != expr


def test_order_negative_integer_placeholder():
    expr = Parser.parse("x^2")
    result = evaluate_order(expr, -1)
    assert "∫" in str(result)


def test_order_fractional_placeholder():
    expr = Parser.parse("sin(x)")
    result = evaluate_order(expr, 0.5)
    assert "FractionalDerivative" in str(result)


def test_order_symbolic():
    expr = Parser.parse("x^m")
    result = evaluate_order(expr, "n")
    assert "D" in str(result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
