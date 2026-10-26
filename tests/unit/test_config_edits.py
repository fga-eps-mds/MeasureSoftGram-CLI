"""
Regressão do defeito encontrado pelo P.O. na validação da US01.01: editar o
msgram.json (remover características e mudar pesos) precisa mudar o resultado
do cálculo e a saída exibida.
"""

import copy
import csv
import json
import shutil
import tempfile
from pathlib import Path

from src.cli.commands.cmd_calculate import calculate_all, command_calculate
from src.cli.commands.cmd_demo import command_demo
from src.cli.commands.cmd_init import command_init
from src.cli.jsonReader import open_json_file
from tests.unit.cli_output import normalize_cli_output
from staticfiles import DEFAULT_PRE_CONFIG as pre_config

SONAR_METRICS = "fga-eps-mds-2022-2-MeasureSoftGram-CLI-01-05-2023-21-40-30-develop-extracted.metrics"
REMOVED_ENTITIES = (
    "reliability",
    "testing_status",
    "passed_tests",
    "test_builds",
    "test_coverage",
)


def _edited_config():
    config = copy.deepcopy(pre_config)
    config["characteristics"] = [
        c for c in config["characteristics"] if c["key"] != "reliability"
    ]
    for characteristic in config["characteristics"]:
        characteristic["weight"] = {
            "maintainability": 80,
            "functional_suitability": 20,
        }[characteristic["key"]]
    return config


def _tsqmi(result):
    return result["tsqmi"][0]["value"]


def test_init_generates_config_without_performance_efficiency():
    config_path = Path(tempfile.mkdtemp()) / ".msgram"

    command_init({"config_path": config_path})

    config = open_json_file(config_path / "msgram.json")
    keys = [c["key"] for c in config["characteristics"]]
    assert "performance_efficiency" not in keys
    assert sum(c["weight"] for c in config["characteristics"]) == 100
    for characteristic in config["characteristics"]:
        subchars = characteristic["subcharacteristics"]
        assert sum(sc["weight"] for sc in subchars) == 100
        for subcharacteristic in subchars:
            assert sum(m["weight"] for m in subcharacteristic["measures"]) == 100

    shutil.rmtree(config_path.parent)


def test_calculate_uses_edited_config_weights():
    json_data = open_json_file(Path(f"tests/unit/data/{SONAR_METRICS}"))

    default_result = calculate_all(json_data, SONAR_METRICS, pre_config)
    edited_result = calculate_all(json_data, SONAR_METRICS, _edited_config())

    edited_keys = [
        item["key"]
        for group in ("characteristics", "subcharacteristics", "measures")
        for item in edited_result[group]
    ]
    for removed_key in REMOVED_ENTITIES:
        assert removed_key not in edited_keys
    assert _tsqmi(edited_result) != _tsqmi(default_result)


def test_tree_output_follows_the_edited_config(capsys):
    config_dirpath = Path(tempfile.mkdtemp())
    extract_dirpath = Path(tempfile.mkdtemp())
    (config_dirpath / "msgram.json").write_text(json.dumps(_edited_config()))
    shutil.copy(f"tests/unit/data/{SONAR_METRICS}", extract_dirpath / SONAR_METRICS)

    command_calculate(
        {
            "output_format": "tree",
            "config_path": config_dirpath,
            "extracted_path": extract_dirpath / SONAR_METRICS,
        }
    )

    out = normalize_cli_output(capsys.readouterr().out)
    for removed_key in REMOVED_ENTITIES:
        assert removed_key not in out
    assert "maintainability:" in out
    maintainability_block = out.split("maintainability:", 1)[1]
    assert "modifiability" in maintainability_block.split("functional_suitability")[0]

    shutil.rmtree(config_dirpath)
    shutil.rmtree(extract_dirpath)


def test_tabular_json_and_csv_outputs_follow_the_edited_config(capsys, tmp_path):
    extract_path = tmp_path / SONAR_METRICS
    shutil.copy(f"tests/unit/data/{SONAR_METRICS}", extract_path)

    default_dir = tmp_path / "default"
    default_dir.mkdir()
    (default_dir / "msgram.json").write_text(json.dumps(pre_config))

    edited_dir = tmp_path / "edited"
    edited_dir.mkdir()
    (edited_dir / "msgram.json").write_text(json.dumps(_edited_config()))

    for output_format in ("tabular", "json", "csv"):
        command_calculate(
            {
                "output_format": output_format,
                "config_path": default_dir,
                "extracted_path": extract_path,
            }
        )
        default_out = normalize_cli_output(capsys.readouterr().out)

        command_calculate(
            {
                "output_format": output_format,
                "config_path": edited_dir,
                "extracted_path": extract_path,
            }
        )
        edited_out = normalize_cli_output(capsys.readouterr().out)

        if output_format == "tabular":
            for removed_key in REMOVED_ENTITIES:
                assert removed_key in default_out
                assert removed_key not in edited_out
            assert "maintainability" in edited_out
            assert "modifiability" in edited_out

    default_json = open_json_file(default_dir / "calc_msgram.json")[0]
    edited_json = open_json_file(edited_dir / "calc_msgram.json")[0]
    assert _tsqmi(edited_json) != _tsqmi(default_json)
    edited_json_keys = [
        item["key"]
        for group in ("characteristics", "subcharacteristics", "measures")
        for item in edited_json[group]
    ]
    for removed_key in REMOVED_ENTITIES:
        assert removed_key not in edited_json_keys

    with open(default_dir / "calc_msgram.csv", newline="") as f:
        default_csv = list(csv.DictReader(f))[0]
    with open(edited_dir / "calc_msgram.csv", newline="") as f:
        edited_csv = list(csv.DictReader(f))[0]

    assert edited_csv["tsqmi"] != default_csv["tsqmi"]
    for removed_key in REMOVED_ENTITIES:
        assert removed_key in default_csv
        assert removed_key not in edited_csv


def test_demo_keeps_an_edited_config(tmp_path):
    default_dir = tmp_path / "padrao"
    command_demo({"output_path": default_dir, "output_format": "json"})
    default_tsqmi = _tsqmi(open_json_file(default_dir / "calc_msgram.json")[0])

    edited_dir = tmp_path / "editado"
    edited_dir.mkdir()
    edited_config = _edited_config()
    (edited_dir / "msgram.json").write_text(json.dumps(edited_config))

    command_demo({"output_path": edited_dir, "output_format": "json"})

    assert open_json_file(edited_dir / "msgram.json") == edited_config
    edited_result = open_json_file(edited_dir / "calc_msgram.json")[0]
    edited_tsqmi = _tsqmi(edited_result)
    assert edited_tsqmi != default_tsqmi
    edited_measure_keys = [m["key"] for m in edited_result["measures"]]
    for removed_key in ("passed_tests", "test_builds", "test_coverage"):
        assert removed_key not in edited_measure_keys
