"""`msgram extract -gr` sem rede.

O plugin GitHub do msgram-parser monta a URL fixa https://api.github.com, então o binário por subprocess não tem como
ser apontado para um servidor falso. Aqui a CLI roda no mesmo processo (src.cli.cli.main) e só o `requests.get` do
plugin é trocado por respostas gravadas em tests/e2e/data/github_api. O `calculate` em seguida roda pelo binário.
"""

import json
import sys

from src.cli import cli
from tests.e2e.support import DATA

API = DATA / "github_api"


class FakeResponse:
    status_code = 200

    def __init__(self, payload):
        self.payload = payload

    def json(self):
        return self.payload


def fake_github(url, headers=None):
    assert url.startswith("https://api.github.com/repos/fga-eps-mds/repo-falso/"), url
    if "/issues?" in url:
        return FakeResponse(json.loads((API / "issues.json").read_text()))
    if url.endswith("/actions/runs"):
        return FakeResponse(json.loads((API / "runs.json").read_text()))
    if "/dependabot/alerts?" in url:
        return FakeResponse(json.loads((API / "dependabot_alerts.json").read_text()))
    raise AssertionError(f"chamada inesperada à API do GitHub: {url}")


def run_in_process(monkeypatch, *args):
    monkeypatch.setattr(sys, "argv", ["msgram", "--theme", "light", *map(str, args)])
    cli.main()


def test_extract_github_then_calculate(msgram, tmp_path, monkeypatch, mocker, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    get = mocker.patch("genericparser.plugins.dinamic.github.requests.get", side_effect=fake_github)
    cfg = tmp_path / ".msgram"
    assert msgram("init", "-cp", cfg).returncode == 0

    run_in_process(monkeypatch, "extract", "-gr", "fga-eps-mds/repo-falso", "-ep", cfg, "-gw", "build", "-gl", "US")

    assert "Traceback" not in capsys.readouterr().out
    assert get.call_count == 3  # issues pela label US, workflow runs e alertas do Dependabot
    (extracted,) = cfg.glob("github_fga-eps-mds-repo-falso-*-extracted.metrics")
    metrics = {m["metric"]: m["value"] for m in json.loads(extracted.read_text())["fga-eps-mds/repo-falso"]}
    # 3 issues (2 fechadas); 2 runs "build" de 60 s e 120 s; o run "lint" fica fora pelo -gw; 3 alertas (1 aberto)
    assert metrics == {
        "total_issues": 3,
        "resolved_issues": 2,
        "resolved_ratio": 2 / 3,
        "sum_ci_feedback_times": 180,
        "total_builds": 2,
        "security_alerts_open": 1,
        "security_alerts_closed": 2,
    }

    result = msgram("calculate", "-ep", cfg, "-cp", cfg, "-o", "json")

    assert result.returncode == 0, result.stdout
    (calculated,) = json.loads((cfg / "calc_msgram.json").read_text())
    assert calculated["repository"][0]["value"] == "fga-eps-mds-repo-falso"
    assert {c["key"] for c in calculated["characteristics"]} == {"reliability", "functional_suitability"}
