"""Pruebas de la interfaz de línea de comandos."""

import json

import pytest

from json2csv.cli import main


def test_cli_exitoso(tmp_path, capsys):
    entrada = tmp_path / "in.json"
    salida = tmp_path / "out.csv"
    entrada.write_text(json.dumps([{"a": 1}]), encoding="utf-8")
    rc = main([str(entrada), str(salida)])
    assert rc == 0
    assert salida.exists()
    assert "OK" in capsys.readouterr().out


def test_cli_archivo_inexistente(tmp_path):
    rc = main([str(tmp_path / "no.json"), str(tmp_path / "out.csv")])
    assert rc == 2


def test_cli_json_invalido(tmp_path):
    entrada = tmp_path / "malo.json"
    entrada.write_text("{ malo", encoding="utf-8")
    rc = main([str(entrada), str(tmp_path / "out.csv")])
    assert rc == 1


def test_cli_no_flatten(tmp_path):
    entrada = tmp_path / "in.json"
    salida = tmp_path / "out.csv"
    entrada.write_text(json.dumps({"a": {"b": 1}}), encoding="utf-8")
    rc = main([str(entrada), str(salida), "--no-flatten"])
    assert rc == 0


def test_cli_version(capsys):
    with pytest.raises(SystemExit) as exc:
        main(["--version"])
    assert exc.value.code == 0
    assert "json2csv" in capsys.readouterr().out
