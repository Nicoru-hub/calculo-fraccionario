from __future__ import annotations

from calculus.expressions.base import Constant


class Pi(Constant):
    """Constante π = 3.14159265358979323846..."""

    def __init__(self):
        super().__init__("π")


class EulerE(Constant):
    """Constante e = 2.71828182845904523536..."""

    def __init__(self):
        super().__init__("e")


class GoldenRatio(Constant):
    """Constante φ (Golden Ratio) = 1.61803398874989484820..."""

    def __init__(self):
        super().__init__("φ")


# Singleton instances
pi = Pi()
e = EulerE()
phi = GoldenRatio()
