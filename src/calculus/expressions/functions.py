from __future__ import annotations

from dataclasses import dataclass
from calculus.expressions.base import Expression


@dataclass(frozen=True)
class Function(Expression):
    """Base class for mathematical functions."""
    name: str
    arguments: tuple[Expression, ...]

    def __str__(self):
        args = ", ".join(str(a) for a in self.arguments)
        return f"{self.name}({args})"


@dataclass(frozen=True)
class Sin(Function):
    """Sine function."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "sin")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Cos(Function):
    """Cosine function."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "cos")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Tan(Function):
    """Tangent function."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "tan")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Cot(Function):
    """Cotangent function."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "cot")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Sec(Function):
    """Secant function."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "sec")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Csc(Function):
    """Cosecant function."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "csc")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Exp(Function):
    """Exponential function (e^x)."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "exp")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Ln(Function):
    """Natural logarithm (ln)."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "ln")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Log(Function):
    """Logarithm base 10 (log)."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "log")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Sqrt(Function):
    """Square root."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "sqrt")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Abs(Function):
    """Absolute value."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "abs")
        object.__setattr__(self, "arguments", (expr,))


@dataclass(frozen=True)
class Gamma(Function):
    """Gamma function."""
    def __init__(self, expr: Expression):
        object.__setattr__(self, "name", "gamma")
        object.__setattr__(self, "arguments", (expr,))
