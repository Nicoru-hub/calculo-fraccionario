from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Iterable


class Expression:
    """Base class for all symbolic expressions."""

    def __add__(self, other):
        from calculus.expressions.operations import Add

        return Add(self, other)

    def __sub__(self, other):
        from calculus.expressions.operations import Sub

        return Sub(self, other)

    def __mul__(self, other):
        from calculus.expressions.operations import Mul

        return Mul(self, other)

    def __truediv__(self, other):
        from calculus.expressions.operations import Div

        return Div(self, other)

    def __pow__(self, other):
        from calculus.expressions.operations import Pow

        return Pow(self, other)

    def __neg__(self):
        from calculus.expressions.operations import Neg

        return Neg(self)

    def simplify(self):
        from calculus.simplification.simplifier import simplify_expression

        return simplify_expression(self)

    def diff(self, variable: str):
        from calculus.differentiation.rules import differentiate

        return differentiate(self, variable)

    def __str__(self):
        from calculus.formatter.formatter import to_string

        return to_string(self)

    def __repr__(self):
        return self.__str__()


@dataclass(frozen=True)
class Number(Expression):
    value: Fraction

    def __init__(self, value):
        if isinstance(value, int):
            value = Fraction(value, 1)
        elif isinstance(value, Fraction):
            pass
        elif isinstance(value, float):
            # Keep exact rational values when possible.
            value = Fraction(str(value)).limit_denominator()
        else:
            raise TypeError(f"Unsupported numeric type: {type(value)!r}")
        object.__setattr__(self, "value", value)

    def __str__(self):
        return str(self.value.numerator) if self.value.denominator == 1 else f"{self.value.numerator}/{self.value.denominator}"


@dataclass(frozen=True)
class Variable(Expression):
    name: str

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Constant(Expression):
    name: str
    value: str | None = None

    def __str__(self):
        return self.name


@dataclass(frozen=True)
class Rational(Number):
    pass


@dataclass(frozen=True)
class Integer(Number):
    pass
