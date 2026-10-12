import pytest
from calculus.parser.parser import Parser
from calculus.differentiation.order import (
    evaluate_order,
    DerivativeOrder,
    IntegralExpression,
)
from calculus.differentiation.rules import differentiate


def test_order_zero():
    """Order 0 returns the expression unchanged."""
    expr = Parser.parse("x^2")
    assert evaluate_order(expr, 0, "x") == expr


def test_order_one():
    """Order 1 is equivalent to differentiate()."""
    expr = Parser.parse("x^3")
    assert evaluate_order(expr, 1, "x") == differentiate(expr, "x")


def test_order_two():
    """Order 2 equals differentiating twice."""
    expr = Parser.parse("x^3")
    expected = differentiate(differentiate(expr, "x"), "x")
    assert evaluate_order(expr, 2, "x") == expected


def test_order_negative_one():
    """Order -1 returns an integral placeholder."""
    expr = Parser.parse("x^2")
    result = evaluate_order(expr, -1, "x")
    assert isinstance(result, IntegralExpression)


def test_order_fractional():
    """Fractional order returns an explicit fractional derivative node."""
    expr = Parser.parse("x^2")
    result = evaluate_order(expr, 0.5, "x")
    assert "FractionalDerivative" in str(result)


def test_order_symbolic():
    """Symbolic order returns a DerivativeOrder node."""
    expr = Parser.parse("x^2")
    result = evaluate_order(expr, "n", "x")
    assert isinstance(result, DerivativeOrder)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
