from __future__ import annotations

from dataclasses import dataclass
from calculus.expressions.base import Expression


@dataclass(frozen=True)
class Add(Expression):
    """Addition operation: a + b"""
    left: Expression
    right: Expression

    def __str__(self):
        return f"({self.left} + {self.right})"


@dataclass(frozen=True)
class Sub(Expression):
    """Subtraction operation: a - b"""
    left: Expression
    right: Expression

    def __str__(self):
        return f"({self.left} - {self.right})"


@dataclass(frozen=True)
class Mul(Expression):
    """Multiplication operation: a * b"""
    left: Expression
    right: Expression

    def __str__(self):
        return f"({self.left} * {self.right})"


@dataclass(frozen=True)
class Div(Expression):
    """Division operation: a / b"""
    left: Expression
    right: Expression

    def __str__(self):
        return f"({self.left} / {self.right})"


@dataclass(frozen=True)
class Pow(Expression):
    """Power operation: a ^ b (or a ** b)"""
    base: Expression
    exponent: Expression

    def __str__(self):
        return f"({self.base}^{self.exponent})"


@dataclass(frozen=True)
class Neg(Expression):
    """Negation operation: -a"""
    expr: Expression

    def __str__(self):
        return f"(-{self.expr})"
