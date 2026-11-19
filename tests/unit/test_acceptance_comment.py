import importlib.util
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "acceptance_comment.py"
spec = importlib.util.spec_from_file_location("acceptance_comment", SCRIPT)
acceptance_comment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(acceptance_comment)

JUNIT = """<?xml version="1.0" encoding="utf-8"?>
<testsuites><testsuite name="pytest">
  <testcase name="test_ok"><properties><property name="ca" value="US01.01-CA1" />
    <property name="ca" value="US01.01-CA2" /></properties></testcase>
  <testcase name="test_falha"><properties><property name="ca" value="US01.01-CA2" /></properties>
    <failure message="boom" /></testcase>
  <testcase name="test_manual"><properties><property name="ca" value="US02.03-CA1" /></properties>
    <skipped message="manual" /></testcase>
  <testcase name="test_sem_ca" />
  <testcase name="test_outra_prop"><properties><property name="ca" value="nao-e-ca" /></properties></testcase>
</testsuite></testsuites>
"""


def test_collect_reads_one_result_per_test_and_criterion(tmp_path):
    junit = tmp_path / "junit.xml"
    junit.write_text(JUNIT)

    tests = acceptance_comment.collect(junit)

    assert [(t["us"], t["ca"], t["title"], t["status"]) for t in tests] == [
        ("US01.01", 1, "test_ok", "passed"),
        ("US01.01", 2, "test_ok", "passed"),
        ("US01.01", 2, "test_falha", "failed"),
        ("US02.03", 1, "test_manual", "skipped"),
    ]


def test_render_marks_failed_criterion_and_keeps_history(tmp_path):
    junit = tmp_path / "junit.xml"
    junit.write_text(JUNIT)
    tests = [t for t in acceptance_comment.collect(junit) if t["us"] == "US01.01"]
    old = [{"date": "01/11/2026 10:00", "branch": "develop", "sha": "abc1234", "result": "passou", "run": None}]

    body = acceptance_comment.render("US01.01", tests, old)

    assert body.startswith(acceptance_comment.MARKER)
    assert "**falhou**" in body
    assert "| CA1 | 1 | 1 | 0 | 0 | passou |" in body
    assert "| CA2 | 2 | 1 | 1 | 0 | falhou |" in body
    history = acceptance_comment.read_history({"body": body})
    assert [h["sha"] for h in history] == ["local", "abc1234"]


def test_summarize_only_skipped_is_manual():
    assert acceptance_comment.summarize([{"status": "skipped"}])["result"] == "manual"


def test_read_history_tolerates_missing_or_broken_marker():
    assert acceptance_comment.read_history(None) == []
    assert acceptance_comment.read_history({"body": "<!-- e2e-historico-cli:{quebrado -->"}) == []
