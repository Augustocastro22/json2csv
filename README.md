# json2csv

Herramienta de línea de comandos para convertir archivos **JSON** a formato
**CSV**, con controles robustos para las condiciones de excepción. Proyecto
espejo del `csv2json` usado en clase, desarrollado para la materia **Calidad de
Software** (Ingeniería en Informática, U.FASTA).

[![CI](https://github.com/Augustocastro22/json2csv/actions/workflows/ci.yml/badge.svg)](https://github.com/Augustocastro22/json2csv/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## Características

- Convierte un **objeto** JSON o una **lista de objetos** a CSV.
- **Aplana** objetos anidados con notación de puntos (`contacto.email`).
- Serializa listas internas como texto JSON en una celda.
- Encabezado del CSV = unión ordenada de las claves de todos los registros.
- Manejo robusto de errores con excepciones específicas.
- Delimitador configurable (`,`, `;`, etc.).

## Instalación

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# Linux / macOS
source .venv/bin/activate

pip install -e .
```

## Uso

```bash
json2csv entrada.json salida.csv
json2csv entrada.json salida.csv --delimiter ";"
json2csv entrada.json salida.csv --no-flatten
json2csv --version
```

Ejemplo de entrada (`entrada.json`):

```json
[
  {"id": 1, "nombre": "Ana", "contacto": {"email": "ana@x.com"}},
  {"id": 2, "nombre": "Beto", "contacto": {"email": "beto@x.com"}}
]
```

Salida (`salida.csv`):

```csv
id,nombre,contacto.email
1,Ana,ana@x.com
2,Beto,beto@x.com
```

## Desarrollo

```bash
pip install -r requirements-dev.txt

ruff check .          # linting (PEP 8 + PEP 257)
black --check .       # formato consistente
mypy src              # tipado estático
pyright               # tipado estático
pytest --cov=json2csv --cov-report=term-missing   # tests + cobertura
bandit -r src         # análisis de seguridad
pdoc src/json2csv -o docs   # documentación de la API
```

## Estructura

```
json2csv/
├── src/json2csv/
│   ├── __init__.py      # versión y build del paquete
│   ├── json2csv.py      # lógica de conversión (núcleo)
│   └── cli.py           # interfaz de línea de comandos
├── tests/               # pruebas unitarias (pytest)
├── CONTEXT.md           # contexto para asistentes de IA
├── CHANGELOG.md         # registro de cambios
├── VERSION / BUILD      # registro de versión y build
├── LICENSE              # licencia MIT
└── pyproject.toml       # metadatos y configuración de herramientas
```

## Versión

Ver los archivos [`VERSION`](VERSION) y [`BUILD`](BUILD). El historial de
cambios está en [`CHANGELOG.md`](CHANGELOG.md).

## Licencia

Distribuido bajo licencia **MIT**. Ver [`LICENSE`](LICENSE).
