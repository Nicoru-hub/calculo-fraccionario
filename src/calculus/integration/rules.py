from __future__ import annotations

from calculus.expressions.base import Expression, Number, Variable, Constant
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import (
    Sin, Cos, Tan, Exp, Ln, Sqrt
)
from calculus.constants.constants import pi, e
from calculus.simplification.simplifier import simplify_expression
from fractions import Fraction


class IntegrationRule:
    """Base class for integration rules."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        """Apply rule, return integral or None if not applicable."""
        raise NotImplementedError


class ConstantRule(IntegrationRule):
    """∫ c dx = c*x + C"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if isinstance(expr, Number):
            return Add(Mul(expr, Variable(variable)), Constant("C"))
        if isinstance(expr, Constant):
            return Add(Mul(expr, Variable(variable)), Constant("C"))
        return None


class VariableRule(IntegrationRule):
    """∫ x dx = x^2/2 + C, ∫ y dy = y^2/2 + C"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Variable):
            return None
        
        if expr.name == variable:
            # ∫ x dx = x^2/2 + C
            integral = Mul(
                Pow(expr, Number(2)),
                Number(Fraction(1, 2))
            )
            return Add(integral, Constant("C"))
        else:
            # ∫ y dx = y*x + C (y is constant w.r.t. x)
            return Add(
                Mul(expr, Variable(variable)),
                Constant("C")
            )


class PowerRule(IntegrationRule):
    """∫ u^n du = u^(n+1)/(n+1) + C (n != -1)"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Pow):
            return None
        
        base = expr.base
        exponent = expr.exponent
        
        # Check if base is just the variable
        if not isinstance(base, Variable) or base.name != variable:
            return None
        
        # Check if exponent is a number and not -1
        if not isinstance(exponent, Number):
            return None
        
        if exponent.value == Fraction(-1):
            # Special case: ∫ x^(-1) dx = ln(x) + C
            return Add(Ln(base), Constant("C"))
        
        # General case: x^(n+1) / (n+1) + C
        new_exp = Number(exponent.value + 1)
        integral = Div(
            Pow(base, new_exp),
            new_exp
        )
        return Add(integral, Constant("C"))


class LinearityRule(IntegrationRule):
    """∫ (f + g) dx = ∫ f dx + ∫ g dx"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if isinstance(expr, Add):
            left_integral = integrate(expr.left, variable)
            right_integral = integrate(expr.right, variable)
            # Combine and remove duplicate constants
            return Add(left_integral, right_integral)
        
        if isinstance(expr, Sub):
            left_integral = integrate(expr.left, variable)
            right_integral = integrate(expr.right, variable)
            return Sub(left_integral, right_integral)
        
        return None


class ExpRule(IntegrationRule):
    """∫ e^x dx = e^x + C"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Exp):
            return None
        
        inner = expr.arguments[0]
        if not isinstance(inner, Variable) or inner.name != variable:
            return None
        
        return Add(Exp(inner), Constant("C"))


class LnRule(IntegrationRule):
    """∫ ln(x) dx = x*ln(x) - x + C"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Ln):
            return None
        
        inner = expr.arguments[0]
        if not isinstance(inner, Variable) or inner.name != variable:
            return None
        
        # x*ln(x) - x + C
        integral = Sub(
            Mul(inner, expr),
            inner
        )
        return Add(integral, Constant("C"))


class SinRule(IntegrationRule):
    """∫ sin(x) dx = -cos(x) + C"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Sin):
            return None
        
        inner = expr.arguments[0]
        if not isinstance(inner, Variable) or inner.name != variable:
            return None
        
        return Add(Neg(Cos(inner)), Constant("C"))


class CosRule(IntegrationRule):
    """∫ cos(x) dx = sin(x) + C"""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Cos):
            return None
        
        inner = expr.arguments[0]
        if not isinstance(inner, Variable) or inner.name != variable:
            return None
        
        return Add(Sin(inner), Constant("C"))


class Integrator:
    """Main integration engine."""
    
    def __init__(self):
        self.rules = [
            ConstantRule(),
            VariableRule(),
            PowerRule(),
            ExpRule(),
            LnRule(),
            SinRule(),
            CosRule(),
            LinearityRule(),
        ]
    
    def integrate(self, expr: Expression, variable: str) -> Expression:
        """Integrate expression with respect to variable."""
        for rule in self.rules:
            result = rule.apply(expr, variable)
            if result is not None:
                return result
        
        # If no rule matches, raise error
        raise ValueError(f"Cannot integrate: {expr}")


def integrate(expr: Expression, variable: str) -> Expression:
    """Integrate an expression."""
    integrator = Integrator()
    result = integrator.integrate(expr, variable)
    return simplify_expression(result)
