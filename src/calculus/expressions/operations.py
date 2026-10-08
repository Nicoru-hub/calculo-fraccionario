from __future__ import annotations

from dataclasses import dataclass

from calculus.expressions.base import Expression


@dataclass(frozen=True)
class Add(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"({self.left} + {self.right})"


@dataclass(frozen=True)
class Sub(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"({self.left} - {self.right})"


@dataclass(frozen=True)
class Mul(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"({self.left} * {self.right})"


@dataclass(frozen=True)
class Div(Expression):
    left: Expression
    right: Expression

    def __str__(self):
        return f"({self.left} / {self.right})"


@dataclass(frozen=True)
class Pow(Expression):
    base: Expression
    exponent: Expression

    def __str__(self):
        return f"({self.base}^{self.exponent})"


@dataclass(frozen=True)
class Neg(Expression):
    expr: Expression

    def __str__(self):
        return f"(-{self.expr})"
