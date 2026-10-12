from __future__ import annotations

from typing import Optional
from calculus.expressions.base import Expression, Number, Variable
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import (
    Sin, Cos, Tan, Exp, Ln, Sqrt
)
from fractions import Fraction


class DifferentiationRule:
    """Base class for differentiation rules."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        """Apply rule, return derivative or None if not applicable."""
        raise NotImplementedError


class ConstantRule(DifferentiationRule):
    """d/dx [c] = 0"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if isinstance(expr, Number):
            return Number(0)
        return None


class VariableRule(DifferentiationRule):
    """d/dx [x] = 1, d/dx [y] = 0 (if differentiating w.r.t. x)"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Variable):
            return None
        
        if expr.name == variable:
            return Number(1)
        else:
            return Number(0)


class PowerRule(DifferentiationRule):
    """d/dx [x^n] = n * x^(n-1)"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Pow):
            return None
        
        base = expr.base
        exponent = expr.exponent
        
        # Only apply if base is the variable
        if not isinstance(base, Variable) or base.name != variable:
            return None
        
        # Exponent must be a number
        if not isinstance(exponent, Number):
            return None
        
        n = exponent.value
        
        # n * x^(n-1)
        new_exp = Pow(base, Number(n - 1))
        return Mul(Number(n), new_exp)


class ProductRule(DifferentiationRule):
    """d/dx [f*g] = f'*g + f*g'"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Mul):
            return None
        
        f = expr.left
        g = expr.right
        
        f_prime = differentiate(f, variable)
        g_prime = differentiate(g, variable)
        
        # f'*g + f*g'
        return Add(
            Mul(f_prime, g),
            Mul(f, g_prime)
        )


class QuotientRule(DifferentiationRule):
    """d/dx [f/g] = (f'*g - f*g') / g^2"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Div):
            return None
        
        f = expr.left
        g = expr.right
        
        f_prime = differentiate(f, variable)
        g_prime = differentiate(g, variable)
        
        # (f'*g - f*g') / g^2
        numerator = Sub(
            Mul(f_prime, g),
            Mul(f, g_prime)
        )
        denominator = Pow(g, Number(2))
        
        return Div(numerator, denominator)


class ChainRule(DifferentiationRule):
    """d/dx [f(g(x))] = f'(g(x)) * g'(x)"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        # This is handled by specific function rules
        return None


class SinRule(DifferentiationRule):
    """d/dx [sin(u)] = cos(u) * u'"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Sin):
            return None
        
        u = expr.arguments[0]
        u_prime = differentiate(u, variable)
        
        return Mul(Cos(u), u_prime)


class CosRule(DifferentiationRule):
    """d/dx [cos(u)] = -sin(u) * u'"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Cos):
            return None
        
        u = expr.arguments[0]
        u_prime = differentiate(u, variable)
        
        return Mul(Neg(Sin(u)), u_prime)


class TanRule(DifferentiationRule):
    """d/dx [tan(u)] = sec^2(u) * u'"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Tan):
            return None
        
        u = expr.arguments[0]
        u_prime = differentiate(u, variable)
        
        # sec^2(u) = 1 / cos^2(u)
        sec_squared = Div(Number(1), Pow(Cos(u), Number(2)))
        
        return Mul(sec_squared, u_prime)


class ExpRule(DifferentiationRule):
    """d/dx [e^u] = e^u * u'"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Exp):
            return None
        
        u = expr.arguments[0]
        u_prime = differentiate(u, variable)
        
        return Mul(Exp(u), u_prime)


class LnRule(DifferentiationRule):
    """d/dx [ln(u)] = u' / u"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Ln):
            return None
        
        u = expr.arguments[0]
        u_prime = differentiate(u, variable)
        
        return Div(u_prime, u)


class SqrtRule(DifferentiationRule):
    """d/dx [sqrt(u)] = u' / (2 * sqrt(u))"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Sqrt):
            return None
        
        u = expr.arguments[0]
        u_prime = differentiate(u, variable)
        
        denominator = Mul(Number(2), Sqrt(u))
        
        return Div(u_prime, denominator)


class Differentiator:
    """Main differentiation engine."""
    
    def __init__(self):
        self.rules = [
            ConstantRule(),
            VariableRule(),
            PowerRule(),
            SinRule(),
            CosRule(),
            TanRule(),
            ExpRule(),
            LnRule(),
            SqrtRule(),
            ProductRule(),
            QuotientRule(),
        ]
    
    def differentiate(self, expr: Expression, variable: str) -> Expression:
        """Differentiate expression with respect to variable."""
        for rule in self.rules:
            result = rule.apply(expr, variable)
            if result is not None:
                return result
        
        # If no rule matches, return 0 (constant)
        return Number(0)


def differentiate(expr: Expression, variable: str) -> Expression:
    """Differentiate an expression."""
    from calculus.simplification.simplifier import simplify_expression
    
    differentiator = Differentiator()
    result = differentiator.differentiate(expr, variable)
    return simplify_expression(result)
