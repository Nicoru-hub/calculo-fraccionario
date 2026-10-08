from __future__ import annotations

from calculus.expressions.base import Expression, Number, Variable, Constant
from calculus.expressions.operations import Add, Sub, Mul, Div, Pow, Neg
from calculus.expressions.functions import (
    Function, Sin, Cos, Tan, Cot, Sec, Csc, Exp, Ln, Log, Sqrt, Abs, Gamma
)
from calculus.constants.constants import pi, e, phi
from calculus.simplification.simplifier import simplify_expression
from fractions import Fraction


class DerivationRule:
    """Base class for differentiation rules."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        """Apply rule, return derivative or None if not applicable."""
        raise NotImplementedError


class ConstantRule(DerivationRule):
    """d/dx(c) = 0 where c is a constant."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if isinstance(expr, Number):
            return Number(0)
        if isinstance(expr, Constant):
            return Number(0)
        return None


class VariableRule(DerivationRule):
    """d/dx(x) = 1, d/dx(y) = 0 if y != x."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Variable):
            return None
        
        if expr.name == variable:
            return Number(1)
        else:
            return Number(0)


class LinearityRule(DerivationRule):
    """d/dx(f + g) = f' + g', d/dx(f - g) = f' - g'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if isinstance(expr, Add):
            left_deriv = differentiate(expr.left, variable)
            right_deriv = differentiate(expr.right, variable)
            return Add(left_deriv, right_deriv)
        
        if isinstance(expr, Sub):
            left_deriv = differentiate(expr.left, variable)
            right_deriv = differentiate(expr.right, variable)
            return Sub(left_deriv, right_deriv)
        
        return None


class ProductRule(DerivationRule):
    """d/dx(fg) = f'g + fg'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Mul):
            return None
        
        f = expr.left
        g = expr.right
        f_prime = differentiate(f, variable)
        g_prime = differentiate(g, variable)
        
        return Add(Mul(f_prime, g), Mul(f, g_prime))


class QuotientRule(DerivationRule):
    """d/dx(f/g) = (f'g - fg')/g^2."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Div):
            return None
        
        f = expr.left
        g = expr.right
        f_prime = differentiate(f, variable)
        g_prime = differentiate(g, variable)
        
        numerator = Sub(Mul(f_prime, g), Mul(f, g_prime))
        denominator = Pow(g, Number(2))
        
        return Div(numerator, denominator)


class ChainRuleBase(DerivationRule):
    """d/dx(f(g)) = f'(g) * g'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Function):
            return None
        
        # Get the inner function
        inner = expr.arguments[0]
        inner_prime = differentiate(inner, variable)
        
        # Get the outer derivative
        outer_prime = self._outer_derivative(expr, inner)
        
        return Mul(outer_prime, inner_prime)
    
    def _outer_derivative(self, expr: Function, inner: Expression) -> Expression:
        """Compute the derivative of the outer function."""
        raise NotImplementedError


class SinDerivativeRule(ChainRuleBase):
    """d/dx(sin(u)) = cos(u) * u'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Sin):
            return None
        return super().apply(expr, variable)
    
    def _outer_derivative(self, expr: Sin, inner: Expression) -> Expression:
        return Cos(inner)


class CosDerivativeRule(ChainRuleBase):
    """d/dx(cos(u)) = -sin(u) * u'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Cos):
            return None
        return super().apply(expr, variable)
    
    def _outer_derivative(self, expr: Cos, inner: Expression) -> Expression:
        return Neg(Sin(inner))


class TanDerivativeRule(ChainRuleBase):
    """d/dx(tan(u)) = sec^2(u) * u'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Tan):
            return None
        return super().apply(expr, variable)
    
    def _outer_derivative(self, expr: Tan, inner: Expression) -> Expression:
        return Pow(Sec(inner), Number(2))


class ExpDerivativeRule(ChainRuleBase):
    """d/dx(e^u) = e^u * u'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Exp):
            return None
        return super().apply(expr, variable)
    
    def _outer_derivative(self, expr: Exp, inner: Expression) -> Expression:
        return Exp(inner)


class LnDerivativeRule(ChainRuleBase):
    """d/dx(ln(u)) = (1/u) * u'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Ln):
            return None
        return super().apply(expr, variable)
    
    def _outer_derivative(self, expr: Ln, inner: Expression) -> Expression:
        return Div(Number(1), inner)


class LogDerivativeRule(ChainRuleBase):
    """d/dx(log(u)) = (1/(u*ln(10))) * u'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Log):
            return None
        return super().apply(expr, variable)
    
    def _outer_derivative(self, expr: Log, inner: Expression) -> Expression:
        # 1 / (u * ln(10))
        ln_10 = Ln(Number(10))
        return Div(Number(1), Mul(inner, ln_10))


class SqrtDerivativeRule(ChainRuleBase):
    """d/dx(sqrt(u)) = (1/(2*sqrt(u))) * u'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Sqrt):
            return None
        return super().apply(expr, variable)
    
    def _outer_derivative(self, expr: Sqrt, inner: Expression) -> Expression:
        # 1 / (2 * sqrt(u))
        return Div(Number(1), Mul(Number(2), Sqrt(inner)))


class PowerRuleSpecial(DerivationRule):
    """d/dx(u^n) = n * u^(n-1) * u' (power rule with chain rule)."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Pow):
            return None
        
        base = expr.base
        exponent = expr.exponent
        
        # Check if exponent is constant
        if not self._is_constant(exponent, variable):
            return None
        
        base_prime = differentiate(base, variable)
        new_exponent = Sub(exponent, Number(1))
        
        return Mul(Mul(exponent, Pow(base, new_exponent)), base_prime)
    
    @staticmethod
    def _is_constant(expr: Expression, variable: str) -> bool:
        """Check if expression is constant with respect to variable."""
        if isinstance(expr, Number):
            return True
        if isinstance(expr, Constant):
            return True
        if isinstance(expr, Variable):
            return expr.name != variable
        return False


class NegationRule(DerivationRule):
    """d/dx(-f) = -f'."""
    
    def apply(self, expr: Expression, variable: str) -> Expression | None:
        if not isinstance(expr, Neg):
            return None
        
        inner_prime = differentiate(expr.expr, variable)
        return Neg(inner_prime)


class Differentiator:
    """Main differentiation engine."""
    
    def __init__(self):
        self.rules = [
            ConstantRule(),
            VariableRule(),
            LinearityRule(),
            NegationRule(),
            SinDerivativeRule(),
            CosDerivativeRule(),
            TanDerivativeRule(),
            ExpDerivativeRule(),
            LnDerivativeRule(),
            LogDerivativeRule(),
            SqrtDerivativeRule(),
            PowerRuleSpecial(),
            ProductRule(),
            QuotientRule(),
        ]
    
    def differentiate(self, expr: Expression, variable: str) -> Expression:
        """Differentiate expression with respect to variable."""
        for rule in self.rules:
            result = rule.apply(expr, variable)
            if result is not None:
                return result
        
        # If no rule matches, raise error
        raise ValueError(f"Cannot differentiate: {expr}")


def differentiate(expr: Expression, variable: str) -> Expression:
    """Differentiate an expression."""
    differentiator = Differentiator()
    result = differentiator.differentiate(expr, variable)
    return simplify_expression(result)
