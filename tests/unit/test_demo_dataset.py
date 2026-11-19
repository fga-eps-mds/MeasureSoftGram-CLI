"""Dataset de exemplo da demo.

A demo é usada para validar a US01.01 (medição de Dívida Técnica) com o PO,
então o dataset precisa ter a métrica do Sonar que alimenta
technical_debt_ratio. As duas cópias (pacote e examples/) precisam ser iguais
para não divergirem.
"""

import json
from pathlib import Path

from src.cli.commands.cmd_demo import command_demo, find_raw_data_dir
from src.cli.jsonReader import open_json_file
from tests.unit.cli_output import normalize_cli_output

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGED_DIR = REPO_ROOT / "src" / "cli" / "resources" / "demo_data"
EXAMPLES_DIR = REPO_ROOT / "examples" / "analytics-raw-data"


def _sonar_metrics(sonar_file: Path) -> set[str]:
    data = json.loads(sonar_file.read_text())
    measures = list(data["baseComponent"].get("measures", []))
    for component in data.get("components", []):
        measures.extend(component.get("measures", []))
    return {measure["metric"] for measure in measures}


def test_demo_dataset_has_technical_debt_metric():
    sonar_files = list(find_raw_data_dir().glob("*.json"))

    assert len(sonar_files) == 1
    assert "sqale_debt_ratio" in _sonar_metrics(sonar_files[0])


def test_demo_dataset_copies_are_identical():
    packaged = sorted(p.name for p in PACKAGED_DIR.glob("*.json"))
    examples = sorted(p.name for p in EXAMPLES_DIR.glob("*.json"))

    assert packaged == examples
    for name in packaged:
        assert (PACKAGED_DIR / name).read_bytes() == (EXAMPLES_DIR / name).read_bytes()


def test_demo_calculates_technical_debt_ratio(tmp_path, capsys):
    output_path = tmp_path / "demo"
    command_demo({"output_path": output_path, "output_format": "json"})

    result = open_json_file(output_path / "calc_msgram.json")[0]
    measure_keys = [m["key"] for m in result["measures"]]
    assert "technical_debt_ratio" in measure_keys

    out = normalize_cli_output(capsys.readouterr().out)
    assert "Missing metrics: sqale_debt_ratio" not in out
