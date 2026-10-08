from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from calculus.expressions.base import Expression, Number, Constant
from calculus.simplification.simplifier import simplify_expression


@dataclass(frozen=True)
class GammaValue(Expression):
    """Represents an exact or symbolic Gamma function value."""
    argument: Expression | float | int

    def __str__(self):
        return f"Γ({self.argument})"


class GammaCalculator:
    """Gamma function calculation and properties."""
    
    # Known exact values
    EXACT_VALUES = {
        1: Fraction(1),           # Γ(1) = 1
        2: Fraction(1),           # Γ(2) = 1
        3: Fraction(2),           # Γ(3) = 2
        4: Fraction(6),           # Γ(4) = 6
        5: Fraction(24),          # Γ(5) = 24
        Fraction(1, 2): "sqrt(π)", # Γ(1/2) = √π
        Fraction(3, 2): "sqrt(π)/2", # Γ(3/2) = √π/2
    }
    
    # Recursion relation: Γ(n+1) = n * Γ(n)
    @staticmethod
    def gamma_recurrence(n: float) -> Expression | None:
        """Use recurrence Γ(n+1) = n * Γ(n) to simplify."""
        if isinstance(n, int) and n >= 1:
            # Γ(n) = (n-1)!
            result = 1
            for i in range(1, n):
                result *= i
            return Number(result)
        return None
    
    @staticmethod
    def reflection_formula(n: float) -> Expression | None:
        """Euler's reflection formula: Γ(z) * Γ(1-z) = π / sin(πz)"""
        # TODO: Implement for complex arguments
        return None
    
    @staticmethod
    def duplication_formula(n: float) -> Expression | None:
        """Legendre's duplication formula for Gamma."""
        # TODO: Implement
        return None
    
    @staticmethod
    def evaluate_gamma(n: Expression | float | int) -> Expression | float:
        """Evaluate Gamma function if possible."""
        if isinstance(n, Number):
            val = n.value
            if val in GammaCalculator.EXACT_VALUES:
                exact = GammaCalculator.EXACT_VALUES[val]
                if isinstance(exact, Fraction):
                    return Number(exact)
                else:
                    return Constant(exact)
        
        # Try to use recurrence
        if isinstance(n, Number):
            result = GammaCalculator.gamma_recurrence(float(n.value))
            if result:
                return result
        
        # Cannot evaluate, return symbolic
        return GammaValue(n)
