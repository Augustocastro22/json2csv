# Changelog

Todos los cambios notables de este proyecto se documentan en este archivo.

El formato sigue [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/)
y el proyecto adhiere a [Versionado Semántico](https://semver.org/lang/es/).

## [No publicado]

### Agregado
- Archivos de proyecto: `README.md`, `CHANGELOG.md`, `requirements.txt`,
  `requirements-dev.txt`, `LICENSE` (MIT), `VERSION` y `BUILD`.

## [0.1.0] - 2026-06-23

### Agregado
- Esqueleto del proyecto generado con CookieCutter (inciso a).
- `CONTEXT.md` con el contexto del proyecto para asistentes de IA (inciso b).
- Módulo `json2csv.py` con la lógica de conversión: `read_json`, `to_records`,
  `flatten`, `collect_fieldnames`, `write_csv` y `convert`.
- Jerarquía de excepciones: `Json2CsvError`, `InvalidJsonError`,
  `EmptyDataError`, `UnsupportedStructureError`.
- Interfaz de línea de comandos `cli.py` con el comando `json2csv`.

[No publicado]: https://github.com/Augustocastro22/json2csv/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/Augustocastro22/json2csv/releases/tag/v0.1.0
