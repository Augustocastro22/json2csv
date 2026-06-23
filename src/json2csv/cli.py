"""Interfaz de línea de comandos para la herramienta json2csv."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence

from . import __version__
from .json2csv import Json2CsvError, convert


def build_parser() -> argparse.ArgumentParser:
    """Construir el parser de argumentos de la línea de comandos.

    Returns:
        El parser configurado con las opciones del programa.
    """
    parser = argparse.ArgumentParser(
        prog="json2csv",
        description="Convierte un archivo JSON a formato CSV.",
    )
    parser.add_argument("input", help="Archivo JSON de entrada.")
    parser.add_argument("output", help="Archivo CSV de salida.")
    parser.add_argument(
        "-d",
        "--delimiter",
        default=",",
        help="Separador de campos del CSV (por defecto: ',').",
    )
    parser.add_argument(
        "--no-flatten",
        action="store_true",
        help="No aplanar objetos JSON anidados.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"json2csv {__version__}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Ejecutar la conversión desde la línea de comandos.

    Args:
        argv: Argumentos de la línea de comandos. Si es ``None`` se usan
            los de ``sys.argv``.

    Returns:
        Código de salida del proceso (0 si fue exitoso).
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        rows = convert(
            args.input,
            args.output,
            delimiter=args.delimiter,
            flatten_nested=not args.no_flatten,
        )
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except Json2CsvError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(f"OK: {rows} fila(s) escritas en {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
