"""Conversión de archivos JSON a CSV con manejo robusto de excepciones.

Este módulo expone funciones pequeñas y testeables que, en conjunto,
permiten convertir un archivo JSON (un objeto o una lista de objetos)
a un archivo CSV. Cada etapa del proceso valida sus entradas y reporta
errores mediante excepciones específicas derivadas de :class:`Json2CsvError`.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any

StrPath = str | Path


class Json2CsvError(Exception):
    """Error base de la herramienta de conversión JSON a CSV."""


class InvalidJsonError(Json2CsvError):
    """El contenido del archivo no es JSON válido."""


class EmptyDataError(Json2CsvError):
    """El JSON no contiene registros para convertir."""


class UnsupportedStructureError(Json2CsvError):
    """La estructura del JSON no se puede mapear a filas de CSV."""


def read_json(path: StrPath) -> Any:
    """Leer y parsear un archivo JSON.

    Args:
        path: Ruta del archivo JSON de entrada.

    Returns:
        El objeto Python resultante de deserializar el JSON.

    Raises:
        FileNotFoundError: Si el archivo no existe.
        InvalidJsonError: Si el contenido no es JSON válido.
        Json2CsvError: Ante cualquier otro error de lectura.
    """
    source = Path(path)
    try:
        text = source.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise FileNotFoundError(f"No se encontró el archivo: {source}") from None
    except OSError as exc:
        raise Json2CsvError(f"No se pudo leer el archivo {source}: {exc}") from exc

    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise InvalidJsonError(f"JSON inválido en {source}: {exc}") from exc


def to_records(data: Any) -> list[dict[str, Any]]:
    """Normalizar el JSON deserializado a una lista de registros.

    Acepta un objeto (un único registro) o una lista de objetos.

    Args:
        data: Estructura Python deserializada desde JSON.

    Returns:
        Lista de diccionarios, cada uno representando una fila.

    Raises:
        EmptyDataError: Si no hay registros.
        UnsupportedStructureError: Si la estructura no es un objeto ni
            una lista de objetos.
    """
    if isinstance(data, dict):
        records = [data]
    elif isinstance(data, list):
        records = data
    else:
        raise UnsupportedStructureError(
            "El JSON debe ser un objeto o una lista de objetos."
        )

    if not records:
        raise EmptyDataError("El JSON no contiene registros para convertir.")

    if not all(isinstance(record, dict) for record in records):
        raise UnsupportedStructureError(
            "Todos los elementos de la lista deben ser objetos JSON."
        )

    return records


def flatten(
    record: dict[str, Any], parent_key: str = "", separator: str = "."
) -> dict[str, Any]:
    """Aplanar un diccionario anidado usando notación de puntos.

    Los valores de tipo lista se serializan como texto JSON para que
    puedan representarse en una única celda.

    Args:
        record: Diccionario, posiblemente anidado.
        parent_key: Prefijo de clave usado en la recursión.
        separator: Separador entre niveles de anidamiento.

    Returns:
        Diccionario de un solo nivel con claves compuestas.
    """
    items: dict[str, Any] = {}
    for key, value in record.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else str(key)
        if isinstance(value, dict):
            items.update(flatten(value, new_key, separator))
        elif isinstance(value, list):
            items[new_key] = json.dumps(value, ensure_ascii=False)
        else:
            items[new_key] = value
    return items


def collect_fieldnames(records: list[dict[str, Any]]) -> list[str]:
    """Reunir las columnas del CSV como la unión ordenada de claves.

    Args:
        records: Lista de registros ya normalizados.

    Returns:
        Lista de nombres de columna en orden de aparición.
    """
    fieldnames: list[str] = []
    for record in records:
        for key in record:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_csv(
    records: list[dict[str, Any]],
    fieldnames: list[str],
    path: StrPath,
    delimiter: str = ",",
) -> None:
    """Escribir los registros a un archivo CSV.

    Args:
        records: Registros a escribir.
        fieldnames: Columnas del CSV.
        path: Ruta del archivo CSV de salida.
        delimiter: Separador de campos.

    Raises:
        Json2CsvError: Si no se puede escribir el archivo de salida.
    """
    target = Path(path)
    try:
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(
                handle,
                fieldnames=fieldnames,
                delimiter=delimiter,
                extrasaction="ignore",
            )
            writer.writeheader()
            for record in records:
                writer.writerow({key: record.get(key, "") for key in fieldnames})
    except OSError as exc:
        raise Json2CsvError(f"No se pudo escribir el CSV {target}: {exc}") from exc


def convert(
    json_path: StrPath,
    csv_path: StrPath,
    *,
    delimiter: str = ",",
    flatten_nested: bool = True,
) -> int:
    """Convertir un archivo JSON a CSV.

    Orquesta la lectura, normalización, aplanado opcional, detección de
    columnas y escritura del CSV de salida.

    Args:
        json_path: Ruta del archivo JSON de entrada.
        csv_path: Ruta del archivo CSV de salida.
        delimiter: Separador de campos del CSV.
        flatten_nested: Si es ``True``, aplana objetos anidados.

    Returns:
        Cantidad de filas de datos escritas (sin contar el encabezado).

    Raises:
        Json2CsvError: Ante cualquier error de conversión.
        FileNotFoundError: Si el archivo de entrada no existe.
    """
    data = read_json(json_path)
    records = to_records(data)
    if flatten_nested:
        records = [flatten(record) for record in records]
    fieldnames = collect_fieldnames(records)
    write_csv(records, fieldnames, csv_path, delimiter=delimiter)
    return len(records)
