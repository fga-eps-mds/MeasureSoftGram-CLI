"""Aviso da demo sobre medidas que dependem de dados do GitHub.

O dataset de exemplo só tem métricas do SonarQube. Sem o aviso, as medidas
do GitHub configuradas no msgram.json (e as características que dependem só
delas) somem do resultado sem nenhuma explicação.
"""

import copy
import json

from src.cli.commands.cmd_demo import command_demo, github_measures_in_config
from tests.unit.cli_output import normalize_cli_output
from staticfiles import DEFAULT_PRE_CONFIG as pre_config

GITHUB_MEASURES = ("team_throughput", "ci_feedback_time")


def _sonar_only_config():
    config = copy.deepcopy(pre_config)
    config["characteristics"] = [
        c for c in config["characteristics"] if c["key"] == "maintainability"
    ]
    config["characteristics"][0]["weight"] = 100
    return config


def test_github_measures_in_default_config(tmp_path):
    config_file = tmp_path / "msgram.json"
    config_file.write_text(json.dumps(pre_config))

    assert sorted(github_measures_in_config(config_file)) == sorted(GITHUB_MEASURES)


def test_github_measures_in_sonar_only_config(tmp_path):
    config_file = tmp_path / "msgram.json"
    config_file.write_text(json.dumps(_sonar_only_config()))

    assert github_measures_in_config(config_file) == []


def test_github_measures_with_unreadable_config(tmp_path):
    missing_file = tmp_path / "missing.json"
    invalid_file = tmp_path / "invalid.json"
    invalid_file.write_text("{not json")

    assert github_measures_in_config(missing_file) == []
    assert github_measures_in_config(invalid_file) == []


def test_demo_warns_about_github_measures(tmp_path, capsys):
    command_demo({"output_path": tmp_path / "demo", "output_format": "json"})

    out = normalize_cli_output(capsys.readouterr().out)
    assert "need GitHub data" in out
    for measure in GITHUB_MEASURES:
        assert measure in out


def test_demo_does_not_warn_without_github_measures(tmp_path, capsys):
    output_path = tmp_path / "demo"
    output_path.mkdir()
    (output_path / "msgram.json").write_text(json.dumps(_sonar_only_config()))

    command_demo({"output_path": output_path, "output_format": "json"})

    out = normalize_cli_output(capsys.readouterr().out)
    assert "need GitHub data" not in out
    assert "Demo finished successfully!" in out
