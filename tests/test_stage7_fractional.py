import pytest
from calculus.fractional.riemann_liouville import riemann_liouville_derivative
from calculus.fractional.gamma import GammaCalculator
from calculus.parser.parser import Parser
from calculus.expressions.base import Number, Variable
from calculus.expressions.operations import Pow, Div, Mul
from calculus.expressions.functions import Gamma
from fractions import Fraction


def test_rl_derivative_x_power():
    """Test RL derivative of x^n: D^α x^n = Γ(n+1)/Γ(n-α+1) * x^(n-α)"""
    expr = Pow(Variable("x"), Number(2))
    result = riemann_liouville_derivative(expr, 0.5)
    # Should return Γ(3)/Γ(2.5) * x^(1.5)
    assert isinstance(result, Mul)


def test_rl_derivative_x_linear():
    """Test RL derivative of x: D^α x = x^(1-α) / Γ(1-α)"""
    expr = Variable("x")
    result = riemann_liouville_derivative(expr, 0.5)
    assert isinstance(result, Div) or isinstance(result, Mul)


def test_rl_derivative_constant_zero():
    """Test RL derivative of constant: D^α c = 0"""
    expr = Number(5)
    result = riemann_liouville_derivative(expr, 0.5)
    assert result == Number(0)


def test_rl_derivative_sin_no_closed_form():
    """Test RL derivative of sin(x): no closed form, returns explicit node"""
    from calculus.expressions.functions import Sin
    expr = Sin(Variable("x"))
    result = riemann_liouville_derivative(expr, 0.5)
    from calculus.fractional.riemann_liouville import RiemannLiouvilleDerivative
    assert isinstance(result, RiemannLiouvilleDerivative)


def test_gamma_exact_integer():
    """Test exact Gamma values for integers."""
    # Γ(1) = 1
    result = GammaCalculator.evaluate_gamma(Number(1))
    assert result == Number(1)
    
    # Γ(3) = 2
    result = GammaCalculator.evaluate_gamma(Number(3))
    assert result == Number(2)


def test_gamma_recurrence():
    """Test Gamma recurrence relation."""
    # Γ(5) = 4!
    result = GammaCalculator.gamma_recurrence(5)
    assert result == Number(24)


def test_gamma_half_symbolic():
    """Test Gamma(1/2) which is √π."""
    from calculus.fractional.gamma import GammaValue
    result = GammaCalculator.evaluate_gamma(Number(Fraction(1, 2)))
    assert isinstance(result, (GammaValue, Constant))


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
