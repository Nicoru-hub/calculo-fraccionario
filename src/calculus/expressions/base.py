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
    """Numeric literal with exact Fraction representation."""
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
    """Variable (e.g., x, y, z)."""
    name: str

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Constant(Expression):
    """Named constant (e.g., pi, e, phi)."""
    name: str

    def __str__(self):
        return self.name
