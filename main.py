import streamlit as st


def main():
    st.title("Cálculo Simbólico - Derivación Fraccionaria")

    st.write(
        "Sistema de cálculo simbólico con soporte para derivación ordinaria, integral y fraccionaria."
    )

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        expression = st.text_input(
            "Expresión:", placeholder="x^2, sin(x), e^x, pi*x^2", value=""
        )

    with col2:
        order = st.text_input(
            "Orden de derivación:", placeholder="1, -1, 0.5, n", value="1"
        )

    if st.button("Derivar"):
        if not expression:
            st.error("Por favor ingresa una expresión.")
        else:
            st.info(f"Expresión: {expression}")
            st.info(f"Orden: {order}")
            st.warning("Sistema en desarrollo...")

    st.divider()
    st.markdown(
        """
    ## Ayuda
    
    - **Expresiones válidas:** `x^2`, `sin(x)`, `cos(x)`, `tan(x)`, `e^x`, `ln(x)`, `sqrt(x)`
    - **Constantes:** `pi`, `e`, `phi`
    - **Órdenes:** enteros (`1`, `2`, `-1`), fraccionarios (`0.5`, `1/3`), simbólicos (`n`)
    """
    )


if __name__ == "__main__":
    main()
