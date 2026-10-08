from __future__ import annotations

from dataclasses import dataclass

from calculus.expressions.base import Expression


@dataclass(frozen=True)
class Function(Expression):
    name: str
    arguments: tuple[Expression, ...]

    def __str__(self):
        args = ", ".join(str(a) for a in self.arguments)
        return f"{self.name}({args})"


@dataclass(frozen=True)
class Sin(Function):
    def __init__(self, expr: Expression):
        super().__init__("sin", (expr,))


@dataclass(frozen=True)
class Cos(Function):
    def __init__(self, expr: Expression):
        super().__init__("cos", (expr,))


@dataclass(frozen=True)
class Tan(Function):
    def __init__(self, expr: Expression):
        super().__init__("tan", (expr,))


@dataclass(frozen=True)
class Exp(Function):
    def __init__(self, expr: Expression):
        super().__init__("exp", (expr,))


@dataclass(frozen=True)
class Ln(Function):
    def __init__(self, expr: Expression):
        super().__init__("ln", (expr,))


@dataclass(frozen=True)
class Log(Function):
    def __init__(self, expr: Expression):
        super().__init__("log", (expr,))


@dataclass(frozen=True)
class Sqrt(Function):
    def __init__(self, expr: Expression):
        super().__init__("sqrt", (expr,))


@dataclass(frozen=True)
class Gamma(Function):
    def __init__(self, expr: Expression):
        super().__init__("gamma", (expr,))
