# CONTEXT.md

Archivo de contexto del proyecto, pensado para asistentes de IA (Vibe Coding).
Resume el propósito, la arquitectura y las convenciones del proyecto para que
cualquier herramienta o persona pueda colaborar sin perder coherencia.

## Propósito

`json2csv` es una herramienta de línea de comandos que convierte archivos en
formato **JSON** a formato **CSV**. Es el proyecto espejo del `csv2json` usado
en clase, desarrollado para la materia **Calidad de Software** (Ingeniería en
Informática, U.FASTA).

## Alcance

- Entrada: un archivo JSON que contiene **un objeto** o **una lista de objetos**.
- Salida: un archivo CSV con encabezado, donde las columnas son la unión de las
  claves de todos los registros.
- Los objetos anidados se **aplanan** con notación de puntos (`a.b.c`).
- Las listas dentro de un registro se serializan como texto JSON en una celda.
- Manejo robusto de excepciones para todas las condiciones de error previsibles.

## Arquitectura

Diseño en funciones pequeñas y puras (fáciles de testear) más una capa de CLI:

| Módulo | Responsabilidad |
| --- | --- |
| `src/json2csv/json2csv.py` | Lógica de conversión (núcleo). |
| `src/json2csv/cli.py` | Interfaz de línea de comandos (`argparse`). |
| `src/json2csv/__init__.py` | Versión del paquete (`__version__`). |
| `tests/` | Pruebas unitarias con `pytest`. |

Funciones núcleo (`json2csv.py`):

- `read_json(path)` — lee y parsea el JSON de entrada.
- `to_records(data)` — normaliza a una lista de registros (dicts).
- `flatten(record)` — aplana diccionarios anidados.
- `collect_fieldnames(records)` — calcula las columnas del CSV.
- `write_csv(records, fieldnames, path)` — escribe el archivo de salida.
- `convert(json_path, csv_path)` — orquesta todo el proceso.

## Manejo de errores

Jerarquía de excepciones, todas derivan de `Json2CsvError`:

- `InvalidJsonError` — el contenido no es JSON válido.
- `EmptyDataError` — el JSON no contiene registros.
- `UnsupportedStructureError` — la estructura no se puede mapear a filas.
- `FileNotFoundError` — el archivo de entrada no existe (estándar de Python).

## Convenciones de calidad

- Estilo: **PEP 8**, validado con **ruff** y **black**.
- Docstrings: **PEP 257**, validados con ruff (regla `D`).
- Tipado estático: **mypy** y **pyright** sin errores.
- Pruebas: **pytest** con cobertura mínima del **85 %**.
- Seguridad: **bandit** sin observaciones.
- Documentación API generada con **pdoc**.
- Integración continua: **GitHub Actions** (CI/CD).

## Uso

```bash
json2csv entrada.json salida.csv
json2csv entrada.json salida.csv --delimiter ";"
json2csv entrada.json salida.csv --no-flatten
```
