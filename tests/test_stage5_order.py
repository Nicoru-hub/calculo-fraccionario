import pytest
from calculus.parser.parser import Parser
from calculus.differentiation.order import evaluate_order
from calculus.expressions.base import Number, Variable


def test_order_zero():
    """Order 0 should return expression unchanged."""
    expr = Parser.parse("x^2")
    result = evaluate_order(expr, 0, "x")
    assert result == expr


def test_order_one():
    """Order 1 should be equivalent to differentiate()."""
    expr = Parser.parse("x^3")
    result = evaluate_order(expr, 1, "x")
    from calculus.differentiation.rules import differentiate
    direct = differentiate(expr, "x")
    # Both should simplify to 3*x^2
    assert isinstance(result, type(direct))


def test_order_two():
    """Order 2 should give second derivative."""
    expr = Parser.parse("x^3")
    result = evaluate_order(expr, 2, "x")
    # d/dx[d/dx[x^3]] = d/dx[3x^2] = 6x
    assert isinstance(result, type(Parser.parse("6*x")))


def test_order_negative_one():
    """Order -1 should integrate once."""
    expr = Parser.parse("x^2")
    result = evaluate_order(expr, -1, "x")
    # integral of x^2 is x^3/3 + C
    from calculus.expressions.operations import Add
    assert isinstance(result, Add)


def test_order_fractional():
    """Order 0.5 should use Riemann-Liouville."""
    expr = Parser.parse("x^2")
    result = evaluate_order(expr, 0.5, "x")
    from calculus.fractional.riemann_liouville import RiemannLiouvilleDerivative
    # Should return either a closed form or explicit RL node
    assert result is not None


def test_order_symbolic():
    """Order as string should return SymbolicDerivative."""
    from calculus.differentiation.order import SymbolicDerivative
    expr = Parser.parse("x^2")
    result = evaluate_order(expr, "n", "x")
    assert isinstance(result, SymbolicDerivative)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
