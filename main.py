import sys
from pathlib import Path

# Add src to Python path so calculus module is importable
sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st
from calculus.parser.parser import Parser
from calculus.differentiation.rules import differentiate
from calculus.simplification.simplifier import simplify_expression

# Page config
st.set_page_config(
    page_title="Cálculo Fraccionario",
    page_icon="π",
    layout="wide"
)

st.title("🧮 Calculadora de Cálculo Simbólico")
st.markdown("**Derivación de orden arbitrario · Simplificación**")

st.markdown("""
---
### ¿Cómo usarla?
1. Escribe la expresión matemática que quieras derivar o simplificar
2. Elige la operación
3. Presiona el botón para ver el resultado
""")

# Sidebar for operation selection
operation = st.sidebar.radio(
    "📊 Operación",
    ["Derivación", "Simplificación"],
    help="Elige qué operación deseas realizar"
)

variable = st.sidebar.text_input(
    "📝 Variable",
    value="x",
    max_chars=1,
    help="La variable con respecto a la que se derivará"
)

# Main input
st.markdown("---")
st.subheader("📐 Expresión Matemática")

expr_input = st.text_input(
    "Escribe tu expresión:",
    value="x^2",
    placeholder="Ejemplos: x^3, sin(x), e^x, sqrt(x), pi*x^2",
    help="Puedes usar números, variables, constantes y funciones"
)

# Syntax helper in sidebar
with st.sidebar:
    st.markdown("### 📖 Sintaxis Soportada")
    st.markdown("""
    **Números:**
    - Enteros: `2`, `5`
    - Decimales: `3.5`, `0.25`
    - Fracciones: `1/2`, `3/4`
    
    **Constantes:**
    - π (pi)
    - e (número de Euler)
    - φ (phi)
    
    **Operadores:**
    - Suma: `+`
    - Resta: `-`
    - Multiplicación: `*`
    - División: `/`
    - Potencia: `^` o `**`
    
    **Funciones:**
    - Trigonométricas: `sin()`, `cos()`, `tan()`
    - Exponencial: `exp()`
    - Logaritmo: `ln()`, `log()`
    - Raíz: `sqrt()`
    - Valor absoluto: `abs()`
    """)

if expr_input:
    try:
        expr = Parser.parse(expr_input)
        st.success(f"✅ Expresión correcta: {expr}")
        
        if operation == "Derivación":
            st.markdown("---")
            st.subheader("🔄 Derivación")
            
            order = st.slider(
                "Orden de la derivada",
                min_value=1,
                max_value=5,
                value=1,
                help="1ª derivada, 2ª derivada, etc."
            )
            
            col1, col2, col3 = st.columns(3)
            with col2:
                if st.button("🚀 Derivar", use_container_width=True):
                    try:
                        result = expr
                        for _ in range(order):
                            result = differentiate(result, variable)
                        st.markdown("### Resultado:")
                        st.latex(f"{result}")
                        st.code(f"{result}", language="text")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")
        
        elif operation == "Simplificación":
            st.markdown("---")
            st.subheader("✨ Simplificación")
            
            st.info("Se aplicarán reglas algebraicas para simplificar la expresión")
            
            col1, col2, col3 = st.columns(3)
            with col2:
                if st.button("🚀 Simplificar", use_container_width=True):
                    try:
                        result = simplify_expression(expr)
                        st.markdown("### Resultado:")
                        st.latex(f"{result}")
                        st.code(f"{result}", language="text")
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

    except Exception as e:
        st.error(f"❌ Error al procesar la expresión: {e}")
        st.info("Revisa la sintaxis en el panel de la izquierda")

# Examples section
st.markdown("---")
with st.expander("📚 Ejemplos"):
    examples = {
        "Polinomios": [
            ("x^2", "Derivada de x²"),
            ("x^3 + 2*x + 1", "Derivada de un polinomio"),
        ],
        "Trigonométricas": [
            ("sin(x)", "Derivada de seno"),
            ("cos(x)", "Derivada de coseno"),
        ],
        "Exponenciales": [
            ("e^x", "Derivada de exponencial"),
            ("exp(x)", "También exponencial"),
        ],
        "Logaritmos": [
            ("ln(x)", "Derivada de logaritmo natural"),
        ],
        "Raíces": [
            ("sqrt(x)", "Derivada de raíz cuadrada"),
            ("x^(1/2)", "También raíz cuadrada"),
        ],
    }
    
    for category, exs in examples.items():
        st.markdown(f"**{category}:**")
        for expr_str, description in exs:
            st.markdown(f"- `{expr_str}` — {description}")

st.markdown("""
---
**Proyecto:** Cálculo Fraccionario Simbólico  
**Desarrollado para:** Docentes y estudiantes de Cálculo
""")
