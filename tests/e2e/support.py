"""Caminhos das fixtures de entrada e funções de apoio dos testes E2E."""

import json
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DATA = Path(__file__).parent / "data"
UNIT_DATA = REPO / "tests" / "unit" / "data"
SONAR_DIR = REPO / "examples" / "analytics-raw-data"
GITHUB_METRICS = (
    UNIT_DATA
    / "github_fga-eps-mds-2024.1-MeasureSoftGram-DOC-28-07-2024-00-00-22-extracted.metrics"
)
PERF_CSV_1 = UNIT_DATA / "perf-eff-data-1.csv"
PERF_CSV_2 = UNIT_DATA / "perf-eff-data-2.csv"

# Proxy inexistente: qualquer acesso à internet feito pelo binário falha na hora.
NO_NETWORK = "http://127.0.0.1:9"


def rounded(value, digits=6):
    """Arredonda floats em qualquer profundidade, para o golden não depender da última casa."""
    if isinstance(value, float):
        return round(value, digits)
    if isinstance(value, list):
        return [rounded(item, digits) for item in value]
    if isinstance(value, dict):
        return {key: rounded(item, digits) for key, item in value.items()}
    return value


def normalize(text, tmp_path):
    """Tira do texto o que muda a cada execução: caminho temporário, tempos e espaços de padding do rich."""
    text = text.replace(str(tmp_path), "<TMP>")
    text = re.sub(r"\d+\.\d+ seconds", "<T> seconds", text)
    return "\n".join(line.rstrip() for line in text.splitlines()).strip("\n") + "\n"


def after(text, marker):
    """Parte da saída depois do marcador; o antes tem barras de progresso, que não são estáveis."""
    assert marker in text, text
    return text.split(marker, 1)[1]


def write_default_config(path: Path):
    """Mesmo msgram.json que o `msgram init` grava, sem gastar um subprocess."""
    from staticfiles import DEFAULT_PRE_CONFIG

    path.mkdir(parents=True, exist_ok=True)
    (path / "msgram.json").write_text(json.dumps(DEFAULT_PRE_CONFIG, indent=4))
