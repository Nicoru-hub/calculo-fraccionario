# Cálculo simbólico con derivación fraccionaria, negativa y simbólica

## Qué es este proyecto

Este proyecto implementa un sistema de cálculo simbólico orientado a objetos en Python, con soporte para:

- derivación ordinaria,
- integración simbólica,
- derivadas de orden entero negativo,
- derivadas fraccionarias de tipo Riemann-Liouville,
- órdenes simbólicos como `n` o `m`,
- funciones como `sin`, `cos`, `tan`, `exp`, `ln`, `log`, `sqrt`, etc.,
- parser matemático propio,
- simplificación exacta,
- interfaz web con Streamlit.

La idea principal es que el núcleo del sistema no dependa de una sola librería que "lo haga todo". El sistema tiene su propio AST, parser, simplificador y reglas de diferenciación.

## Requisitos

- Python 3.13+
- GitHub Codespaces o entorno local con Python

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Ejecutar la aplicación

```bash
streamlit run main.py
```

La app estará disponible en el puerto 8501.

## Estructura del proyecto

```text
project/
├── src/
│   └── calculus/
│       ├── constants/
│       ├── differentiation/
│       ├── expressions/
│       ├── fractional/
│       ├── functions/
│       ├── integration/
│       ├── interface/
│       ├── parser/
│       ├── simplification/
│       └── formatter/
├── tests/
├── main.py
├── README.md
├── requirements.txt
├── pyproject.toml
└── .devcontainer/
```

## Sintaxis aceptada

Ejemplos válidos:

- `x^2`
- `x^3 + 2x + 1`
- `sin(x)`
- `cos(x)`
- `tan(x)`
- `e^x`
- `pi*x^2`
- `sqrt(x)`
- `ln(x)`
- `log(x)`
- `2sin(x)`
- `(x+1)(x-1)`
- `x^pi`
- `1/2`
- `3/7`
- `0.25`
- `pi/2`

## Constantes disponibles

- `pi`
- `e`
- `phi`
- `0`, `1`
- enteros y racionales exactos

## Funciones disponibles

- `sin(x)`
- `cos(x)`
- `tan(x)`
- `cot(x)`
- `sec(x)`
- `csc(x)`
- `exp(x)`
- `ln(x)`
- `log(x)`
- `sqrt(x)`
- `abs(x)`
- `gamma(x)`

## Soporte matemático implementado

### Derivadas ordinarias

- linealidad
- regla del producto
- regla del cociente
- regla de la cadena
- potencia
- funciones trigonométricas y exponenciales

### Órdenes enteros negativos

Se interpretan como integrales sucesivas:

- `D^-1(f(x)) = ∫ f(x) dx`
- `D^-2(f(x)) = ∬ f(x) dx dx`

Se representan con constantes de integración explícitas.

### Derivación fraccionaria

Se utiliza la definición de Riemann-Liouville:

```text
D^α f(x) = (d^n / dx^n) [ 1 / Γ(n−α) ∫_0^x (x−t)^(n−α−1) f(t) dt ]
```

donde `n = ceil(α)` para la extensión de RL.

Se documenta explícitamente que:

- α = 1/2 es una derivada fraccionaria real,
- no se intenta fingir que es `f'(x)/2`,
- cuando no existe una fórmula cerrada, se mantiene como `FractionalDerivative(f, α)`.

### Órdenes simbólicos

Ejemplo:

```text
D^n(x^m) = Γ(m+1)/Γ(m−n+1) * x^(m−n)
```

Se mantiene simbólico cuando corresponde.

## Limitaciones matemáticas

Este proyecto prioriza la exactitud sobre la "respuesta por fuerza":

- si no puede resolverse simbólicamente, no se inventa el resultado,
- se representa la operación matemáticamente,
- por ejemplo: `FractionalDerivative(sin(x), 1/2)` es válido.

## Arquitectura

La arquitectura se organiza en módulos:

- `expressions`: AST base y nodos de expresión
- `constants`: constantes matemáticas
- `functions`: funciones elementales y su registro
- `parser`: tokenizer y parser
- `differentiation`: reglas de derivación
- `integration`: reglas de integración
- `fractional`: cálculo fraccionario RL
- `simplification`: simplificador exacto
- `formatter`: impresión en texto y formato de UI
- `interface`: Streamlit

## Ejemplos

```text
Expresión: x^3
Orden: 2
Resultado: 6x
```

```text
Expresión: pi*x^2
Orden: 1
Resultado: 2*pi*x
```

```text
Expresión: e^x
Orden: 5
Resultado: e^x
```

```text
Expresión: x^2
Orden: -1
Resultado: x^3/3 + C
```

```text
Expresión: x^3
Orden: 0
Resultado: x^3
```

## Roadmap del proyecto

1. AST y expresiones
2. Parser
3. Simplificación
4. Derivación ordinaria
5. Constantes
6. Integración
7. Derivadas fraccionarias
8. Órdenes simbólicos
9. Gamma
10. Interfaz en Streamlit
11. Tests

## Licencia

Este proyecto se distribuye para uso educacional e investigativo.
