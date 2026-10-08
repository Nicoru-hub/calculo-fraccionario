from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Expression:
    """Base class for all mathematical expressions."""

    def __str__(self) -> str:
        raise NotImplementedError


@dataclass(frozen=True)
class Number(Expression):
    value: Fraction

    def __init__(self, value):
        if isinstance(value, int):
            object.__setattr__(self, "value", Fraction(value))
        elif isinstance(value, Fraction):
            object.__setattr__(self, "value", value)
        else:
            object.__setattr__(self, "value", Fraction(str(value)))

    def __str__(self):
        if self.value.denominator == 1:
            return str(self.value.numerator)
        return str(self.value)


@dataclass(frozen=True)
class Variable(Expression):
    name: str

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Constant(Expression):
    name: str

    def __str__(self):
        return self.name


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


@dataclass(frozen=True)
class Function(Expression):
    name: str
    arguments: tuple[Expression, ...]

    def __str__(self):
        args = ", ".join(str(a) for a in self.arguments)
        return f"{self.name}({args})"


# Constant definitions
pi = Constant("pi")
e = Constant("e")
phi = Constant("phi")
