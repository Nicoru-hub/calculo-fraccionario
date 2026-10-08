from __future__ import annotations

from dataclasses import dataclass

from calculus.expressions.base import Expression
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import Gamma
from calculus.differentiation.rules import differentiate
from calculus.simplification.simplifier import simplify_expression


@dataclass(frozen=True)
class DerivativeOrder(Expression):
    """Represents D^α(f(x))."""
    expr: Expression
    order: Expression | str

    def __str__(self):
        return f"D^{self.order}({self.expr})"


@dataclass(frozen=True)
class IntegralOrder(Expression):
    """Represents repeated integrals D^{-n}(f(x))."""
    expr: Expression
    order: int

    def __str__(self):
        return f"D^{-{self.order}({self.expr})}"


@dataclass(frozen=True)
class FractionalDerivative(Expression):
    """Represents a fractional derivative operation when no closed form is available."""
    expr: Expression
    order: Expression

    def __str__(self):
        return f"FractionalDerivative({self.expr}, {self.order})"


class OrderEvaluator:
    """Handle order-based differentiation and integration."""

    def evaluate(self, expr: Expression, order: Expression | str, variable: str = "x") -> Expression:
        # Case: order = 0
        if isinstance(order, int) and order == 0:
            return simplify_expression(expr)

        if hasattr(order, "value") and getattr(order, "value", None) == 0:
            return simplify_expression(expr)

        # Case: positive integer order
        if isinstance(order, int) and order > 0:
            current = expr
            for _ in range(order):
                current = differentiate(current, variable)
            return simplify_expression(current)

        # Case: negative integer order
        if isinstance(order, int) and order < 0:
            current = expr
            for _ in range(-order):
                # Simple symbolic integral placeholder: ∫ f dx
                current = IntegralExpression(current, variable)
            return simplify_expression(current)

        # Fractional order: keep as explicit FractionalDerivative
        if isinstance(order, (int, float)) or hasattr(order, "value"):
            return FractionalDerivative(expr, order)

        # Symbolic order: return an explicit symbolic derivative expression
        return DerivativeOrder(expr, order)


@dataclass(frozen=True)
class IntegralExpression(Expression):
    """Placeholder for integration result, with explicit constant of integration."""
    expr: Expression
    variable: str

    def __str__(self):
        return f"∫({self.expr}) d{self.variable} + C"


def evaluate_order(expr: Expression, order: Expression | str | int | float, variable: str = "x") -> Expression:
    """Entry point for an order-based operator."""
    evaluator = OrderEvaluator()
    return evaluator.evaluate(expr, order, variable)
