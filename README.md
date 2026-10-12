# Cálculo Fraccionario - Symbolic Math Engine

## Overview

**calculo-fraccionario** is a Python symbolic mathematics engine focused on fractional calculus, featuring:

- **Exact symbolic computation** using rational fractions
- **Ordinary differentiation** with symbolic rules
- **Symbolic integration** 
- **Integer-order derivatives and integrals** (positive and negative)
- **Fractional derivatives** (Riemann-Liouville definition)
- **Gamma function** support
- **Interactive Streamlit interface**

## Quick Start

### Installation

```bash
git clone https://github.com/Nicoru-hub/calculo-fraccionario.git
cd calculo-fraccionario
pip install -r requirements.txt
```

### Run Tests

```bash
python run_tests.py
# or
pytest -v
```

### Launch Interface

```bash
streamlit run main.py
```

## Project Structure

```
src/calculus/
├── expressions/       # AST and expression types
├── constants/         # Mathematical constants (π, e, φ)
├── parser/            # Tokenizer and parser
├── simplification/    # Symbolic simplifier
├── differentiation/   # Derivation rules and orders
├── integration/       # Integration rules
└── fractional/        # Fractional calculus (RL, Gamma)

tests/                 # Test suite
main.py               # Streamlit app
```

## Features

### Parsing

```python
from calculus.parser.parser import Parser

expr = Parser.parse("x^2 + 3*x + 1")
print(expr)  # (((x^2) + (3 * x)) + 1)
```

### Differentiation

```python
from calculus.differentiation.rules import differentiate

expr = Parser.parse("x^3")
derivative = differentiate(expr, "x")
print(derivative)  # 3*x^2 (after simplification)
```

### Integration

```python
from calculus.integration.rules import integrate

expr = Parser.parse("x^2")
integral = integrate(expr, "x")
print(integral)  # x^3/3 + C
```

### Fractional Derivatives

```python
from calculus.fractional.riemann_liouville import riemann_liouville_derivative

expr = Parser.parse("x^2")
rl_derivative = riemann_liouville_derivative(expr, 0.5)  # Γ(3)/Γ(2.5) * x^1.5
```

## Development Stages

1. ✅ **AST & Exact Arithmetic** - Expression classes with Fraction support
2. ✅ **Parser** - Tokenizer and recursive descent parser
3. ✅ **Simplifier** - Algebraic simplification rules
4. ✅ **Differentiation** - Ordinary derivatives with chain rule, product rule, etc.
5. ✅ **Orders** - Integer, negative, and symbolic derivative orders
6. ✅ **Integration** - Symbolic integration with elementary functions
7. ✅ **Fractional Calculus** - Riemann-Liouville derivatives
8. ✅ **Gamma Function** - Symbolic and exact values
9. ✅ **Streamlit Interface** - Interactive web UI
10. 🔄 **Validation & Testing** - Comprehensive test suite

## License

MIT License - See LICENSE for details

## Author

**Nicoru-hub** - GitHub: [@Nicoru-hub](https://github.com/Nicoru-hub)
