from __future__ import annotations

from typing import Union
from calculus.expressions.base import Expression, Number, Variable, Constant
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.differentiation.rules import differentiate
from fractions import Fraction


def evaluate_order(
    expr: Expression,
    order: Union[int, float, str, Fraction],
    variable: str = "x"
) -> Expression:
    """Evaluate derivative of arbitrary order.
    
    - Positive integers: repeated differentiation
    - Zero: return expression unchanged
    - Negative integers: repeated integration (antiderivative)
    - Fractional: prepare for fractional calculus (not fully implemented)
    - Symbolic: return expression with symbolic order notation
    """
    
    # Zero order: return as is
    if isinstance(order, (int, float, Fraction)):
        if order == 0:
            return expr
    
    # Positive integer order: apply chain rule n times
    if isinstance(order, int) and order > 0:
        result = expr
        for _ in range(order):
            result = differentiate(result, variable)
        return result
    
    # Negative integer order: antiderivative (integration)
    if isinstance(order, int) and order < 0:
        from calculus.integration.rules import integrate
        result = expr
        for _ in range(abs(order)):
            result = integrate(result, variable)
        return result
    
    # Fractional order: prepare for Riemann-Liouville
    if isinstance(order, float) and not order.is_integer():
        from calculus.fractional.riemann_liouville import riemann_liouville_derivative
        return riemann_liouville_derivative(expr, order, variable)
    
    # Symbolic order: return with symbolic notation
    if isinstance(order, str):
        return SymbolicDerivative(expr, order, variable)
    
    # Fraction order
    if isinstance(order, Fraction):
        if order.denominator == 1:
            # Integer case
            return evaluate_order(expr, int(order.numerator), variable)
        else:
            # Fractional case
            from calculus.fractional.riemann_liouville import riemann_liouville_derivative
            return riemann_liouville_derivative(expr, float(order), variable)
    
    raise ValueError(f"Invalid order: {order}")


class SymbolicDerivative(Expression):
    """Represents a derivative of symbolic order.
    
    Example: D^n f(x) where n is a symbol
    """
    
    def __init__(self, expr: Expression, order: str, variable: str = "x"):
        self.expr = expr
        self.order = order  # e.g., 'n', 'alpha'
        self.variable = variable
    
    def __str__(self):
        return f"D^{self.order}[{self.expr}]"


def get_derivative_order(expr: Expression) -> int | float | str | None:
    """Extract the order from a SymbolicDerivative if applicable."""
    if isinstance(expr, SymbolicDerivative):
        return expr.order
    return None
