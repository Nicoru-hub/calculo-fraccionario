# Contributing

Thanks for considering a contribution to `calculo-fraccionario`.

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

## Running tests

```bash
pytest -v
```

## Code style

- Use clear and explicit names.
- Keep symbolic logic exact whenever possible.
- Prefer `Fraction` for exact numerical behavior.
- Add tests for new symbolic rules.

## Pull requests

Open a PR with:

- a clear description of the mathematical behavior,
- example expressions covered,
- validation status from tests.
