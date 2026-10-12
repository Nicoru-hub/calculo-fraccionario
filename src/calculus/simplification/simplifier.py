from __future__ import annotations

from calculus.expressions.base import Expression, Number, Variable, Constant
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import (
    Sin, Cos, Tan, Exp, Ln, Log, Sqrt, Abs
)
from fractions import Fraction


class Simplifier:
    """Simplifies mathematical expressions."""
    
    def simplify(self, expr: Expression) -> Expression:
        """Main simplification entry point."""
        return self._simplify_recursive(expr)
    
    def _simplify_recursive(self, expr: Expression) -> Expression:
        """Recursively simplify an expression."""
        # Numbers and variables are already simple
        if isinstance(expr, (Number, Variable, Constant)):
            return expr
        
        # Simplify operations
        if isinstance(expr, Add):
            return self._simplify_add(expr)
        elif isinstance(expr, Sub):
            return self._simplify_sub(expr)
        elif isinstance(expr, Mul):
            return self._simplify_mul(expr)
        elif isinstance(expr, Div):
            return self._simplify_div(expr)
        elif isinstance(expr, Pow):
            return self._simplify_pow(expr)
        elif isinstance(expr, Neg):
            return self._simplify_neg(expr)
        
        # Functions: simplify arguments
        if hasattr(expr, 'arguments'):
            new_args = tuple(self._simplify_recursive(arg) for arg in expr.arguments)
            # Return new function with simplified arguments
            return type(expr)(*new_args)
        
        return expr
    
    def _simplify_add(self, expr: Add) -> Expression:
        """Simplify addition."""
        left = self._simplify_recursive(expr.left)
        right = self._simplify_recursive(expr.right)
        
        # 0 + x = x
        if isinstance(left, Number) and left.value == 0:
            return right
        if isinstance(right, Number) and right.value == 0:
            return left
        
        # a + b (both numbers) = a + b
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value + right.value)
        
        return Add(left, right)
    
    def _simplify_sub(self, expr: Sub) -> Expression:
        """Simplify subtraction."""
        left = self._simplify_recursive(expr.left)
        right = self._simplify_recursive(expr.right)
        
        # x - 0 = x
        if isinstance(right, Number) and right.value == 0:
            return left
        
        # a - b (both numbers) = a - b
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value - right.value)
        
        return Sub(left, right)
    
    def _simplify_mul(self, expr: Mul) -> Expression:
        """Simplify multiplication."""
        left = self._simplify_recursive(expr.left)
        right = self._simplify_recursive(expr.right)
        
        # 0 * x = 0
        if isinstance(left, Number) and left.value == 0:
            return Number(0)
        if isinstance(right, Number) and right.value == 0:
            return Number(0)
        
        # 1 * x = x
        if isinstance(left, Number) and left.value == 1:
            return right
        if isinstance(right, Number) and right.value == 1:
            return left
        
        # a * b (both numbers) = a * b
        if isinstance(left, Number) and isinstance(right, Number):
            return Number(left.value * right.value)
        
        return Mul(left, right)
    
    def _simplify_div(self, expr: Div) -> Expression:
        """Simplify division."""
        left = self._simplify_recursive(expr.left)
        right = self._simplify_recursive(expr.right)
        
        # x / 1 = x
        if isinstance(right, Number) and right.value == 1:
            return left
        
        # 0 / x = 0 (if x != 0)
        if isinstance(left, Number) and left.value == 0:
            return Number(0)
        
        # a / b (both numbers) = a / b
        if isinstance(left, Number) and isinstance(right, Number):
            if right.value != 0:
                return Number(left.value / right.value)
        
        return Div(left, right)
    
    def _simplify_pow(self, expr: Pow) -> Expression:
        """Simplify exponentiation."""
        base = self._simplify_recursive(expr.base)
        exponent = self._simplify_recursive(expr.exponent)
        
        # x^0 = 1
        if isinstance(exponent, Number) and exponent.value == 0:
            return Number(1)
        
        # x^1 = x
        if isinstance(exponent, Number) and exponent.value == 1:
            return base
        
        # a^b (both numbers) = a^b
        if isinstance(base, Number) and isinstance(exponent, Number):
            result = base.value ** float(exponent.value)
            return Number(result)
        
        return Pow(base, exponent)
    
    def _simplify_neg(self, expr: Neg) -> Expression:
        """Simplify negation."""
        inner = self._simplify_recursive(expr.expr)
        
        # -(-x) = x
        if isinstance(inner, Neg):
            return inner.expr
        
        # -(number) = -number
        if isinstance(inner, Number):
            return Number(-inner.value)
        
        return Neg(inner)


def simplify_expression(expr: Expression) -> Expression:
    """Simplify an expression."""
    simplifier = Simplifier()
    return simplifier.simplify(expr)
