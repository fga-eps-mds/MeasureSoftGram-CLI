"""US01.01 — Operacionalizar a medição de Dívida Técnica na CLI (fga-eps-mds/2026.2-MeasureSoftGram-DOC#76).

Cada teste marca os critérios que cobre com @pytest.mark.us("US01.01-CAn"); o resultado por CA é publicado na issue.
A entrada é o Sonar de exemplo com o `sqale_debt_ratio` de cada arquivo (qualifier FIL) trocado pelo valor do cenário.
"""

import json

import pytest

from tests.e2e.support import SONAR_DIR

SONAR_FILE = next(SONAR_DIR.glob("*.json"))
MODIFIABILITY_MEASURES = ["non_complex_file_density", "commented_file_density", "duplication_absense",
                          "technical_debt_ratio"]


@pytest.fixture
def config(msgram, tmp_path):
    """msgram.json padrão do `msgram init`, devolvido como (caminho, dict) para os cenários que o editam."""
    cfg = tmp_path / "cfg"
    assert msgram("init", "-cp", cfg).returncode == 0
    return cfg, json.loads((cfg / "msgram.json").read_text())


@pytest.fixture
def calculate(msgram, tmp_path, config):
    """Extrai e calcula o Sonar de exemplo com a dívida técnica dada (None: sem a métrica) e devolve o resultado."""
    cfg, _ = config

    def run(debt_ratio):
        name = f"debt-{debt_ratio}"
        sonar, extracted = tmp_path / f"sonar-{name}", tmp_path / f"extracted-{name}"
        sonar.mkdir(exist_ok=True)
        extracted.mkdir(exist_ok=True)  # mesmo cenário duas vezes (CA7): o .metrics é regravado
        data = json.loads(SONAR_FILE.read_text())
        # o dataset de exemplo (export 2026.2) já traz sqale_debt_ratio em FIL, UTS, DIR e no projeto:
        # remove todos e põe só o valor do cenário nos arquivos (FIL)
        for component in [data["baseComponent"], *data["components"]]:
            component["measures"] = [m for m in component["measures"] if m["metric"] != "sqale_debt_ratio"]
            if debt_ratio is not None and component["qualifier"] == "FIL":
                component["measures"].append({"metric": "sqale_debt_ratio", "value": str(debt_ratio)})
        (sonar / SONAR_FILE.name).write_text(json.dumps(data))
        assert msgram("extract", "-sp", sonar, "-ep", extracted).returncode == 0
        result = msgram("calculate", "-ep", extracted, "-cp", cfg, "-o", "json")
        assert result.returncode == 0, result.stdout
        (calculated,) = json.loads((cfg / "calc_msgram.json").read_text())
        values = {
            entity["key"]: entity["value"]
            for level in ("measures", "subcharacteristics", "characteristics", "tsqmi")
            for entity in calculated[level]
        }
        return values, result.stdout

    return run


def save(config, data):
    cfg, _ = config
    (cfg / "msgram.json").write_text(json.dumps(data))


def modifiability_entry(data):
    (maintainability,) = [c for c in data["characteristics"] if c["key"] == "maintainability"]
    (modifiability,) = [s for s in maintainability["subcharacteristics"] if s["key"] == "modifiability"]
    return modifiability


def debt_measure(data):
    (measure,) = [m for m in modifiability_entry(data)["measures"] if m["key"] == "technical_debt_ratio"]
    return measure


@pytest.mark.us("US01.01-CA1")
@pytest.mark.parametrize("debt_ratio, score", [(0, 1.0), (5, 0.75), (10, 0.5), (20, 0.0), (35, 0.0)])
def test_ca1_score_is_linear_between_0_and_20_percent(calculate, debt_ratio, score):
    values, _ = calculate(debt_ratio)

    assert values["technical_debt_ratio"] == pytest.approx(score)


@pytest.mark.us("US01.01-CA1")
def test_ca1_more_debt_means_lower_score(calculate):
    scores = [calculate(debt)[0]["technical_debt_ratio"] for debt in (2, 8, 14)]

    assert scores == sorted(scores, reverse=True) and len(set(scores)) == 3


@pytest.mark.us("US01.01-CA2")
def test_ca2_uses_thresholds_from_msgram_json(calculate, config):
    _, data = config
    debt_measure(data)["max_threshold"] = 40
    save(config, data)

    values, _ = calculate(10)

    assert values["technical_debt_ratio"] == pytest.approx(0.75)


@pytest.mark.us("US01.01-CA3")
def test_ca3_list_shows_measure_under_modifiability_and_maintainability(msgram, config):
    cfg, _ = config

    result = msgram("list", "-cp", cfg)

    assert result.returncode == 0, result.stdout
    maintainability = result.stdout.split("maintainability", 1)[1].split("Fim-Característica", 1)[0]
    modifiability = maintainability.split("modifiability", 1)[1]
    assert "technical_debt_ratio" in modifiability
    assert "sqale_debt_ratio" in modifiability
    assert "Valores de referência: Min = 0 e Max = 20" in modifiability.split("technical_debt_ratio", 1)[1]


@pytest.mark.us("US01.01-CA4", "US01.01-CA5")
def test_ca4_ca5_measure_changes_modifiability_maintainability_and_tsqmi(calculate):
    no_debt, _ = calculate(0)
    full_debt, _ = calculate(20)

    # só a dívida técnica muda entre as duas execuções
    for measure in MODIFIABILITY_MEASURES[:3]:
        assert no_debt[measure] == full_debt[measure]
    for level in ("modifiability", "maintainability", "tsqmi"):
        assert no_debt[level] > full_debt[level], level
    # maintainability tem só modifiability: as duas notas andam juntas
    assert no_debt["maintainability"] == pytest.approx(no_debt["modifiability"])
    assert full_debt["maintainability"] == pytest.approx(full_debt["modifiability"])


@pytest.mark.us("US01.01-CA6", "US01.01-CA8")
def test_ca6_ca8_default_config_has_measure_with_25_percent_each(config):
    _, data = config

    measures = {m["key"]: m for m in modifiability_entry(data)["measures"]}

    assert list(measures) == MODIFIABILITY_MEASURES
    assert {key: m["weight"] for key, m in measures.items()} == dict.fromkeys(MODIFIABILITY_MEASURES, 25)
    assert sum(m["weight"] for m in measures.values()) == 100
    assert (measures["technical_debt_ratio"]["min_threshold"], measures["technical_debt_ratio"]["max_threshold"]) == (
        0,
        20,
    )


@pytest.mark.us("US01.01-CA7")
def test_ca7_custom_weight_changes_aggregation(calculate, config):
    default, _ = calculate(20)
    _, data = config
    for measure in modifiability_entry(data)["measures"]:
        measure["weight"] = 70 if measure["key"] == "technical_debt_ratio" else 10
    save(config, data)

    custom, _ = calculate(20)

    # a medida vale 0 com 20% de dívida: com mais peso, modifiability cai
    assert custom["technical_debt_ratio"] == default["technical_debt_ratio"] == 0
    assert custom["modifiability"] < default["modifiability"]
    assert custom["tsqmi"] < default["tsqmi"]


@pytest.mark.us("US01.01-CA9")
def test_ca9_missing_metric_warns_and_other_measures_are_calculated(calculate):
    values, stdout = calculate(None)

    assert "Measure 'technical_debt_ratio' could not be calculated. Missing metrics: sqale_debt_ratio" in stdout
    assert "technical_debt_ratio" not in values
    for measure in MODIFIABILITY_MEASURES[:3]:
        assert 0 <= values[measure] <= 1
    assert "tsqmi" in values
