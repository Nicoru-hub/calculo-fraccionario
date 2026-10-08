import streamlit as st
from calculus.parser.parser import Parser
from calculus.differentiation.rules import differentiate
from calculus.differentiation.order import evaluate_order
from calculus.integration.rules import integrate
from calculus.simplification.simplifier import simplify_expression
from calculus.expressions.base import Expression

# Page config
st.set_page_config(
    page_title="Cálculo Fraccionario",
    page_icon="π",
    layout="wide"
)

st.title("🧮 Cálculo Simbólico: Derivación Fraccionaria")

st.markdown("""
Bienvenido a la calculadora de cálculo simbólico. Puedes:
- **Derivar** expresiones de orden entero, fraccionario, negativo o simbólico
- **Integrar** expresiones simbólicamente
- **Simplificar** expresiones exactamente
""")

# Sidebar for operation selection
operation = st.sidebar.radio(
    "Operación",
    ["Derivación", "Integración", "Simplificación"]
)

variable = st.sidebar.text_input("Variable", value="x", max_chars=1)

# Main input
st.subheader("Expresión")
expr_input = st.text_input(
    "Ingresa una expresión matemática:",
    value="x^2",
    placeholder="Ejemplo: x^3 + 2*x, sin(x), e^x, pi*x^2"
)

if expr_input:
    try:
        expr = Parser.parse(expr_input)
        st.success(f"✓ Expresión parsed: `{expr}`")
        
        if operation == "Derivación":
            st.subheader("Derivación")
            
            # Order input
            col1, col2 = st.columns(2)
            with col1:
                order_type = st.radio(
                    "Tipo de orden",
                    ["Entero positivo", "Cero", "Entero negativo", "Fraccionario", "Simbólico"]
                )
            
            with col2:
                if order_type == "Entero positivo":
                    order = st.number_input("Orden", value=1, min_value=1, step=1)
                elif order_type == "Cero":
                    order = 0
                elif order_type == "Entero negativo":
                    order = -st.number_input("Orden (negativo)", value=1, min_value=1, step=1)
                elif order_type == "Fraccionario":
                    order = st.number_input("Orden (fraccionario)", value=0.5, min_value=0.0, max_value=1.0, step=0.1)
                else:  # Simbólico
                    order = st.text_input("Orden (simbólico)", value="n", max_chars=1)
            
            if st.button("Derivar"):
                try:
                    if order_type == "Entero positivo" or order_type == "Cero" or order_type == "Entero negativo":
                        result = evaluate_order(expr, order, variable)
                    else:
                        result = evaluate_order(expr, order, variable)
                    
                    st.markdown(f"### Resultado: `{result}`")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif operation == "Integración":
            st.subheader("Integración")
            
            if st.button("Integrar"):
                try:
                    result = integrate(expr, variable)
                    st.markdown(f"### Resultado: `{result}`")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        elif operation == "Simplificación":
            st.subheader("Simplificación")
            
            if st.button("Simplificar"):
                try:
                    result = simplify_expression(expr)
                    st.markdown(f"### Resultado: `{result}`")
                except Exception as e:
                    st.error(f"Error: {e}")
    
    except Exception as e:
        st.error(f"Error al parsear la expresión: {e}")

# Footer
st.markdown("""
---
**Sintaxis soportada:**
- Números: `2`, `3.5`, `1/2`, `0.25`
- Constantes: `pi`, `e`, `phi`
- Variables: `x`, `y`, `z`, `t`
- Operadores: `+`, `-`, `*`, `/`, `^` o `**`
- Funciones: `sin()`, `cos()`, `tan()`, `exp()`, `ln()`, `log()`, `sqrt()`, `abs()`, `gamma()`

**Ejemplos:**
- `x^3 + 2*x + 1`
- `sin(x)`
- `pi*x^2`
- `e^x`
- `sqrt(x)`
""")
