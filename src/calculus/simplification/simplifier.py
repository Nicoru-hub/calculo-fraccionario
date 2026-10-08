from __future__ import annotations

from calculus.expressions.base import Expression, Number, Variable, Constant
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import Function
from calculus.constants.constants import pi, e, phi
from fractions import Fraction
from typing import Dict, Callable


class SimplificationRule:
    """Base class for simplification rules."""
    
    def apply(self, expr: Expression) -> Expression | None:
        """Apply rule, return simplified expr or None if no match."""
        raise NotImplementedError


class AddIdentityRule(SimplificationRule):
    """x + 0 = x, 0 + x = x"""
    
    def apply(self, expr: Expression) -> Expression | None:
        if not isinstance(expr, Add):
            return None
        
        zero = Number(0)
        if expr.left == zero:
            return expr.right
        if expr.right == zero:
            return expr.left
        return None


class MulIdentityRule(SimplificationRule):
    """x * 1 = x, 1 * x = x"""
    
    def apply(self, expr: Expression) -> Expression | None:
        if not isinstance(expr, Mul):
            return None
        
        one = Number(1)
        if expr.left == one:
            return expr.right
        if expr.right == one:
            return expr.left
        return None


class MulZeroRule(SimplificationRule):
    """x * 0 = 0, 0 * x = 0"""
    
    def apply(self, expr: Expression) -> Expression | None:
        if not isinstance(expr, Mul):
            return None
        
        zero = Number(0)
        if expr.left == zero or expr.right == zero:
            return zero
        return None


class DivZeroRule(SimplificationRule):
    """0 / x = 0 (x ≠ 0)"""
    
    def apply(self, expr: Expression) -> Expression | None:
        if not isinstance(expr, Div):
            return None
        
        zero = Number(0)
        if expr.left == zero:
            return zero
        return None


class SubIdentityRule(SimplificationRule):
    """x - x = 0"""
    
    def apply(self, expr: Expression) -> Expression | None:
        if not isinstance(expr, Sub):
            return None
        
        if expr.left == expr.right:
            return Number(0)
        return None


class PowerRulesRule(SimplificationRule):
    """x^1 = x, x^0 = 1, 0^x = 0 (x > 0), 1^x = 1"""
    
    def apply(self, expr: Expression) -> Expression | None:
        if not isinstance(expr, Pow):
            return None
        
        zero = Number(0)
        one = Number(1)
        
        if expr.exponent == one:
            return expr.base
        if expr.exponent == zero:
            return one
        if expr.base == zero:
            return zero
        if expr.base == one:
            return one
        return None


class CombineConstantsRule(SimplificationRule):
    """Combine numeric constants in addition/multiplication."""
    
    def apply(self, expr: Expression) -> Expression | None:
        if isinstance(expr, Add):
            if isinstance(expr.left, Number) and isinstance(expr.right, Number):
                result_frac = expr.left.value + expr.right.value
                return Number(result_frac)
        
        elif isinstance(expr, Mul):
            if isinstance(expr.left, Number) and isinstance(expr.right, Number):
                result_frac = expr.left.value * expr.right.value
                return Number(result_frac)
        
        return None


class CombineConstantsMultiplyRule(SimplificationRule):
    """π + π = 2π, π * π = π², etc. (same constant)"""
    
    def apply(self, expr: Expression) -> Expression | None:
        if isinstance(expr, Add):
            if expr.left == expr.right and isinstance(expr.left, Constant):
                return Mul(Number(2), expr.left)
        
        elif isinstance(expr, Mul):
            if isinstance(expr.left, Mul) and isinstance(expr.right, Constant):
                if isinstance(expr.left.right, Constant) and expr.left.right == expr.right:
                    # c*π * π = c*π²
                    if isinstance(expr.left.left, Number):
                        return Mul(expr.left.left, Pow(expr.right, Number(2)))
        
        return None


class Simplifier:
    """Main simplification engine."""
    
    def __init__(self):
        self.rules = [
            AddIdentityRule(),
            MulIdentityRule(),
            MulZeroRule(),
            DivZeroRule(),
            SubIdentityRule(),
            PowerRulesRule(),
            CombineConstantsRule(),
            CombineConstantsMultiplyRule(),
        ]
    
    def simplify(self, expr: Expression, max_iterations: int = 100) -> Expression:
        """Simplify expression until no more rules apply."""
        iteration = 0
        while iteration < max_iterations:
            simplified = self._simplify_once(expr)
            if simplified == expr:
                break
            expr = simplified
            iteration += 1
        return expr
    
    def _simplify_once(self, expr: Expression) -> Expression:
        """Apply one pass of simplification rules."""
        # First, recursively simplify children
        if isinstance(expr, Add):
            left = self._simplify_once(expr.left)
            right = self._simplify_once(expr.right)
            expr = Add(left, right)
        elif isinstance(expr, Sub):
            left = self._simplify_once(expr.left)
            right = self._simplify_once(expr.right)
            expr = Sub(left, right)
        elif isinstance(expr, Mul):
            left = self._simplify_once(expr.left)
            right = self._simplify_once(expr.right)
            expr = Mul(left, right)
        elif isinstance(expr, Div):
            left = self._simplify_once(expr.left)
            right = self._simplify_once(expr.right)
            expr = Div(left, right)
        elif isinstance(expr, Pow):
            base = self._simplify_once(expr.base)
            exponent = self._simplify_once(expr.exponent)
            expr = Pow(base, exponent)
        elif isinstance(expr, Neg):
            inner = self._simplify_once(expr.expr)
            expr = Neg(inner)
        elif isinstance(expr, Function):
            simplified_args = tuple(self._simplify_once(arg) for arg in expr.arguments)
            expr_type = type(expr)
            expr = expr_type(simplified_args[0])
        
        # Then apply rules to the expression
        for rule in self.rules:
            result = rule.apply(expr)
            if result is not None:
                return result
        
        return expr


def simplify_expression(expr: Expression) -> Expression:
    """Simplify an expression."""
    simplifier = Simplifier()
    return simplifier.simplify(expr)
