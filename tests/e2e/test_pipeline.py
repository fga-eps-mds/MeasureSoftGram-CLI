"""Fluxo feliz de ponta a ponta com as flags reais: init -> extract -> calculate -> list/diff/norm_diff."""

import csv
import json
import re
import shutil

import pytest

from tests.e2e.support import (
    DATA,
    GITHUB_METRICS,
    PERF_CSV_1,
    PERF_CSV_2,
    SONAR_DIR,
    after,
    normalize,
    rounded,
)

CALC_DONE = "All calculations performed successfully!"


@pytest.fixture
def sonar_extracted(msgram, tmp_path):
    """`.msgram/` com msgram.json do init e o .metrics extraído do Sonar de exemplo."""
    cfg = tmp_path / ".msgram"
    assert msgram("init", "-cp", cfg).returncode == 0
    result = msgram("extract", "-sp", SONAR_DIR, "-ep", cfg)
    assert result.returncode == 0, result.stdout
    assert "Metrics successfully extracted [1/1 files" in result.stdout
    return cfg


def read_calc_json(cfg):
    return rounded(json.loads((cfg / "calc_msgram.json").read_text()))


def test_sonar_calculate_json(msgram, sonar_extracted, json_snapshot):
    result = msgram("calculate", "-ep", sonar_extracted, "-cp", sonar_extracted, "-o", "json")

    assert result.returncode == 0, result.stdout
    assert read_calc_json(sonar_extracted) == json_snapshot


def test_sonar_calculate_csv(msgram, sonar_extracted, snapshot):
    result = msgram("calculate", "-ep", sonar_extracted, "-cp", sonar_extracted, "-o", "csv")

    assert result.returncode == 0, result.stdout
    header, row = list(csv.reader((sonar_extracted / "calc_msgram.csv").open()))
    assert dict(zip(header, rounded([_number(value) for value in row]))) == snapshot


@pytest.mark.parametrize("output_format", ["tabular", "tree"])
def test_sonar_calculate_terminal_output(msgram, sonar_extracted, tmp_path, snapshot, output_format):
    result = msgram("calculate", "-ep", sonar_extracted, "-cp", sonar_extracted, "-o", output_format)

    assert result.returncode == 0, result.stdout
    assert normalize(after(result.stdout, CALC_DONE), tmp_path) == snapshot


def test_list_shows_config_created_by_init(msgram, tmp_path, snapshot):
    cfg = tmp_path / "config"
    assert msgram("init", "-cp", cfg).returncode == 0

    result = msgram("list", "-cp", cfg)

    assert result.returncode == 0, result.stdout
    assert normalize(result.stdout, tmp_path) == snapshot


def test_diff_and_norm_diff_against_planned(msgram, sonar_extracted, tmp_path, snapshot):
    assert msgram("calculate", "-ep", sonar_extracted, "-cp", sonar_extracted, "-o", "json").returncode == 0
    developed = sonar_extracted / "calc_msgram.json"
    # o diff grava o resultado ao lado do arquivo planejado: a cópia fica no tmp_path
    planned = shutil.copy(DATA / "planned.json", tmp_path / "planned.json")

    diff = msgram("diff", "-rp", planned, "-rd", developed, "-of", "csv")
    norm = msgram("norm_diff", "-rp", planned, "-rd", developed)

    assert diff.returncode == 0, diff.stdout
    rows = list(csv.DictReader((tmp_path / "calc_diff_msgram.csv").open()))
    numbers = [{**row, "diff": _number(row["diff"]), "developed": _number(row["developed"])} for row in rows]
    assert rounded(numbers) == snapshot
    assert norm.returncode == 0, norm.stdout
    value = float(re.search(r"Norm Diff: ([\d.e-]+)", norm.stdout).group(1))
    assert round(value, 6) == snapshot


def test_github_metrics_calculate(msgram, tmp_path, json_snapshot):
    cfg = tmp_path / ".msgram"
    assert msgram("init", "-cp", cfg).returncode == 0
    shutil.copy(GITHUB_METRICS, cfg)

    result = msgram("calculate", "-ep", cfg, "-cp", cfg, "-o", "json")

    assert result.returncode == 0, result.stdout
    assert read_calc_json(cfg) == json_snapshot


def test_sonar_and_github_together_give_one_result_per_file(msgram, sonar_extracted, json_snapshot):
    shutil.copy(GITHUB_METRICS, sonar_extracted)

    result = msgram("calculate", "-ep", sonar_extracted, "-cp", sonar_extracted, "-o", "json")

    assert result.returncode == 0, result.stdout
    calculated = read_calc_json(sonar_extracted)
    assert len(calculated) == 2
    assert sorted(calculated, key=lambda item: item["repository"][0]["value"]) == json_snapshot


def test_performance_efficiency_extract_and_calculate(msgram, tmp_path, json_snapshot):
    cfg = tmp_path / ".msgram"
    assert msgram("init", "-cp", cfg).returncode == 0

    extract = msgram("extract", "-ep", cfg, "-p1", PERF_CSV_1, "-p2", PERF_CSV_2, "-pn", "perf-repo")
    calculate = msgram("calculate", "-ep", cfg, "-cp", cfg, "-o", "json")

    assert extract.returncode == 0, extract.stdout
    assert len(list(cfg.glob("perf-eff_perf-repo-*-extracted.metrics"))) == 1
    assert calculate.returncode == 0, calculate.stdout
    # O perf-eff do msgram-core usa RandomForest do scikit-learn (versão não fixada): a 4ª casa muda entre versões
    # (1.7 na CI com Python 3.10, 1.9 no 3.11). Duas casas pegam mudança de modelo sem depender do sklearn.
    calculated = rounded(json.loads((cfg / "calc_msgram.json").read_text()), digits=2)
    # a versão do perf-eff é a hora da extração (datetime.now no nome do arquivo)
    assert re.fullmatch(r"\d{2}-\d{2}-\d{4}-\d{2}-\d{2}", calculated[0]["version"][0]["value"])
    calculated[0]["version"][0]["value"] = "<EXTRACTION-TIME>"
    assert calculated == json_snapshot


def _number(text):
    try:
        return float(text)
    except ValueError:
        return text
