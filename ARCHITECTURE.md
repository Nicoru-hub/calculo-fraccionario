# calculo-fraccionario / README

## Proyecto

Este repositorio desarrolla una biblioteca de cálculo simbólico para Python, enfocada en:

- derivación ordinaria,
- integración simbólica,
- derivadas fraccionarias de orden real,
- órdenes enteros negativos,
- órdenes simbólicos,
- cálculo con funciones elementales,
- interfaz Streamlit.

## Arquitectura

La base del sistema está organizada en módulos:

- `src/calculus/expressions/`: AST de expresiones
- `src/calculus/constants/`: constantes matemáticas
- `src/calculus/functions/`: funciones elementales
- `src/calculus/parser/`: tokenizer y parser
- `src/calculus/simplification/`: simplificador exacto
- `src/calculus/differentiation/`: derivación ordinaria y órdenes
- `src/calculus/integration/`: integración simbólica
- `src/calculus/fractional/`: cálculo fraccionario y gamma
- `src/calculus/interface/`: Streamlit

## Fases implementadas

1. AST base
2. Parser matemático
3. Simplificación
4. Derivación ordinaria
5. Órdenes enteros, negativos y simbólicos
6. Integración simbólica
7. Derivación fraccionaria RL
8. Γ y funciones asociadas

## Objetivo

El proyecto prioriza exactitud y representaciones simbólicas sobre respuestas aproximadas.

## Ejecución

```bash
pip install -r requirements.txt
streamlit run main.py
```
