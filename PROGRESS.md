# Stage 1: AST and Constants
- Basic expression nodes (Number, Variable, Constant)
- Numeric exactness (Fraction-based)
- Mathematical constants (π, e, φ)
- Operations (Add, Sub, Mul, Div, Pow, Neg)
- Functions (Sin, Cos, Exp, Ln, Sqrt)
- Operator overloading

## Completed
✓ Expression base class
✓ Number, Variable, Constant classes
✓ Rational number support using fractions.Fraction
✓ Constants: π, e, φ as singletons
✓ Operation nodes: Add, Sub, Mul, Div, Pow, Neg
✓ Function nodes: Sin, Cos, Tan, Exp, Ln, Log, Sqrt, Gamma
✓ __str__ methods for all nodes
✓ Operator overloading (__add__, __sub__, __mul__, etc.)
✓ Test suite for Stage 1

## Next: Parser
Create tokenizer and parser for mathematical expressions.
