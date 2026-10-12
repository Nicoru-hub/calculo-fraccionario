from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


def _wrap(value) -> "Expression":
    if isinstance(value, Expression):
        return value
    return Number(value)


@dataclass(frozen=True)
class Expression:
    """Base class for all mathematical expressions."""

    def __str__(self) -> str:
        raise NotImplementedError

    # Operator overloading (imports are lazy to avoid circular imports)
    def __add__(self, other):
        from calculus.expressions.operations import Add
        return Add(self, _wrap(other))

    def __radd__(self, other):
        from calculus.expressions.operations import Add
        return Add(_wrap(other), self)

    def __sub__(self, other):
        from calculus.expressions.operations import Sub
        return Sub(self, _wrap(other))

    def __rsub__(self, other):
        from calculus.expressions.operations import Sub
        return Sub(_wrap(other), self)

    def __mul__(self, other):
        from calculus.expressions.operations import Mul
        return Mul(self, _wrap(other))

    def __rmul__(self, other):
        from calculus.expressions.operations import Mul
        return Mul(_wrap(other), self)

    def __truediv__(self, other):
        from calculus.expressions.operations import Div
        return Div(self, _wrap(other))

    def __rtruediv__(self, other):
        from calculus.expressions.operations import Div
        return Div(_wrap(other), self)

    def __pow__(self, other):
        from calculus.expressions.operations import Pow
        return Pow(self, _wrap(other))

    def __rpow__(self, other):
        from calculus.expressions.operations import Pow
        return Pow(_wrap(other), self)

    def __neg__(self):
        from calculus.expressions.operations import Neg
        return Neg(self)


@dataclass(frozen=True)
class Number(Expression):
    """Numeric literal with exact Fraction representation."""
    value: Fraction

    def __init__(self, value):
        if isinstance(value, Number):
            value = value.value
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


class Integer(Number):
    """Integer literal."""

    def __init__(self, value):
        super().__init__(int(value))


class Rational(Number):
    """Rational literal: Rational(3, 4) or Rational(Fraction(3, 4))."""

    def __init__(self, numerator, denominator=1):
        super().__init__(Fraction(numerator, denominator))


@dataclass(frozen=True)
class Variable(Expression):
    """Variable (e.g., x, y, z)."""
    name: str

    def __str__(self):
        return self.name


_CONSTANT_SYMBOLS = {"pi": "π", "phi": "φ"}


@dataclass(frozen=True)
class Constant(Expression):
    """Named constant (e.g., pi, e, phi)."""
    name: str

    def __str__(self):
        return _CONSTANT_SYMBOLS.get(self.name, self.name)
