"""Pruebas unitarias del núcleo de conversión json2csv."""

import json

import pytest

from json2csv.json2csv import (
    EmptyDataError,
    InvalidJsonError,
    Json2CsvError,
    UnsupportedStructureError,
    collect_fieldnames,
    convert,
    flatten,
    read_json,
    to_records,
    write_csv,
)


# --- read_json ---


def test_read_json_valido(tmp_path):
    archivo = tmp_path / "datos.json"
    archivo.write_text('{"a": 1}', encoding="utf-8")
    assert read_json(archivo) == {"a": 1}


def test_read_json_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError):
        read_json(tmp_path / "no_existe.json")


def test_read_json_invalido(tmp_path):
    archivo = tmp_path / "malo.json"
    archivo.write_text("{ esto no es json", encoding="utf-8")
    with pytest.raises(InvalidJsonError):
        read_json(archivo)


# --- to_records ---


def test_to_records_objeto_unico():
    assert to_records({"a": 1}) == [{"a": 1}]


def test_to_records_lista():
    data = [{"a": 1}, {"a": 2}]
    assert to_records(data) == data


def test_to_records_lista_vacia():
    with pytest.raises(EmptyDataError):
        to_records([])


def test_to_records_tipo_no_soportado():
    with pytest.raises(UnsupportedStructureError):
        to_records(42)


def test_to_records_lista_con_no_dict():
    with pytest.raises(UnsupportedStructureError):
        to_records([{"a": 1}, "no soy dict"])


# --- flatten ---


def test_flatten_plano():
    assert flatten({"a": 1, "b": 2}) == {"a": 1, "b": 2}


def test_flatten_anidado():
    entrada = {"a": {"b": {"c": 1}}}
    assert flatten(entrada) == {"a.b.c": 1}


def test_flatten_lista_se_serializa():
    resultado = flatten({"tags": ["x", "y"]})
    assert resultado["tags"] == json.dumps(["x", "y"], ensure_ascii=False)


# --- collect_fieldnames ---


def test_collect_fieldnames_union_ordenada():
    records = [{"a": 1, "b": 2}, {"b": 3, "c": 4}]
    assert collect_fieldnames(records) == ["a", "b", "c"]


# --- write_csv ---


def test_write_csv_escribe_encabezado_y_filas(tmp_path):
    salida = tmp_path / "out.csv"
    write_csv([{"a": 1, "b": 2}], ["a", "b"], salida)
    contenido = salida.read_text(encoding="utf-8")
    assert "a,b" in contenido
    assert "1,2" in contenido


def test_write_csv_rellena_faltantes(tmp_path):
    salida = tmp_path / "out.csv"
    write_csv([{"a": 1}], ["a", "b"], salida)
    lineas = salida.read_text(encoding="utf-8").splitlines()
    assert lineas[1] == "1,"


def test_write_csv_ruta_invalida(tmp_path):
    inexistente = tmp_path / "no" / "existe" / "out.csv"
    with pytest.raises(Json2CsvError):
        write_csv([{"a": 1}], ["a"], inexistente)


# --- convert (integración) ---


def test_convert_lista_anidada(tmp_path):
    entrada = tmp_path / "in.json"
    salida = tmp_path / "out.csv"
    entrada.write_text(
        json.dumps([{"id": 1, "c": {"e": "a@x"}}, {"id": 2}]), encoding="utf-8"
    )
    filas = convert(entrada, salida)
    assert filas == 2
    contenido = salida.read_text(encoding="utf-8")
    assert "id,c.e" in contenido


def test_convert_sin_aplanar(tmp_path):
    entrada = tmp_path / "in.json"
    salida = tmp_path / "out.csv"
    entrada.write_text(json.dumps({"a": {"b": 1}}), encoding="utf-8")
    convert(entrada, salida, flatten_nested=False)
    assert "a" in salida.read_text(encoding="utf-8").splitlines()[0]


def test_convert_delimitador(tmp_path):
    entrada = tmp_path / "in.json"
    salida = tmp_path / "out.csv"
    entrada.write_text(json.dumps([{"a": 1, "b": 2}]), encoding="utf-8")
    convert(entrada, salida, delimiter=";")
    assert "a;b" in salida.read_text(encoding="utf-8")
