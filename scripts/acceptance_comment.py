"""Publica na issue de cada US, no repositório DOC, o resultado dos E2E da CLI por critério de aceitação.

Lê o junit.xml do pytest, agrupa os testes pela propriedade `ca` (gravada por `@pytest.mark.us("USxx.yy-CAn")`) e
mantém um único comentário por issue (achado pelo marcador), editado a cada run, com a tabela por CA e o histórico
dos últimos runs. O número da issue de cada US fica em tests/e2e/acceptance-issues.json.
Porta do scripts/e2e-acceptance-comment.mjs do Front, com marcador próprio para não editar o comentário do Front.

Uso: python scripts/acceptance_comment.py [junit.xml] [--dry-run]
No CI precisa de DOC_ISSUES_TOKEN (token com permissão de escrita em issues do DOC); sem ele, só avisa e sai.
"""

import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

CONFIG_PATH = Path(__file__).resolve().parents[1] / "tests" / "e2e" / "acceptance-issues.json"
MARKER = "<!-- e2e-aceitacao-cli -->"
HISTORY_MARKER = re.compile(r"<!-- e2e-historico-cli:(.*?) -->", re.S)
HISTORY_SIZE = 10
TAG = re.compile(r"^(US\d+\.\d+)-CA(\d+)$")

env = os.environ
API = env.get("GITHUB_API_URL", "https://api.github.com")
SERVER = env.get("GITHUB_SERVER_URL", "https://github.com")
REPO_URL = f"{SERVER}/{env.get('GITHUB_REPOSITORY', '')}"
RUN_URL = f"{REPO_URL}/actions/runs/{env['GITHUB_RUN_ID']}" if env.get("GITHUB_RUN_ID") else None
COMMIT_URL = f"{REPO_URL}/commit/{env['GITHUB_SHA']}" if env.get("GITHUB_SHA") else None


def collect(junit_path):
    """Um resultado por (teste, CA) para os testes com a propriedade `ca` no junit.xml."""
    out = []
    for case in ET.parse(junit_path).iter("testcase"):
        if case.find("failure") is not None or case.find("error") is not None:
            status = "failed"
        elif case.find("skipped") is not None:
            status = "skipped"
        else:
            status = "passed"
        for prop in case.iter("property"):
            match = TAG.match(prop.get("value", "")) if prop.get("name") == "ca" else None
            if match:
                out.append({"us": match[1], "ca": int(match[2]), "title": case.get("name"), "status": status})
    return out


def summarize(tests):
    count = {status: sum(t["status"] == status for t in tests) for status in ("passed", "failed", "skipped")}
    if count["failed"]:
        result = "falhou"
    elif count["passed"]:
        result = "passou (com itens manuais)" if count["skipped"] else "passou"
    else:
        result = "manual"
    return {"total": len(tests), **count, "result": result}


def link(text, url):
    return f"[{text}]({url})" if url else text


def render(us, tests, history):
    by_ca = {}
    for test in tests:
        by_ca.setdefault(test["ca"], []).append(test)
    rows = [{"ca": ca, **summarize(items)} for ca, items in sorted(by_ca.items())]
    result = "falhou" if any(row["failed"] for row in rows) else "passou"
    manual = [t for t in tests if t["status"] == "skipped"]

    entry = {
        "date": datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M"),
        "branch": env.get("GITHUB_REF_NAME", "local"),
        "sha": env.get("GITHUB_SHA", "local")[:7],
        "result": result,
        "run": RUN_URL,
    }
    next_history = [entry, *history][:HISTORY_SIZE]

    lines = [
        MARKER,
        "## Aceitação automática (E2E da CLI)",
        "",
        f"Testes `{us}-CAn` do repositório da CLI no último push para `{entry['branch']}`: **{result}**.",
        f"{link('Run ' + env.get('GITHUB_RUN_ID', 'local'), RUN_URL)} · commit "
        f"{link('`' + entry['sha'] + '`', COMMIT_URL)} · {entry['date']} (Brasília)",
        "",
        "| CA | Testes | Passaram | Falharam | Manuais | Resultado |",
        "| --- | --- | --- | --- | --- | --- |",
        *(
            f"| CA{r['ca']} | {r['total']} | {r['passed']} | {r['failed']} | {r['skipped']} | {r['result']} |"
            for r in rows
        ),
        "",
    ]
    if manual:
        lines += ["Verificação manual (pulados no E2E):", "", *(f"- CA{t['ca']}: {t['title']}" for t in manual), ""]
    lines += [
        f"<details><summary>Histórico (últimos {HISTORY_SIZE} runs)</summary>",
        "",
        "| Data | Branch | Commit | Resultado | Run |",
        "| --- | --- | --- | --- | --- |",
        *(
            f"| {h['date']} | {h['branch']} | `{h['sha']}` | {h['result']} | {link('abrir', h['run'])} |"
            for h in next_history
        ),
        "",
        "</details>",
        f"<!-- e2e-historico-cli:{json.dumps(next_history, ensure_ascii=False)} -->",
    ]
    return "\n".join(lines)


def github(path, method="GET", body=None):
    request = urllib.request.Request(
        f"{API}{path}",
        method=method,
        data=json.dumps(body).encode() if body is not None else None,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {env['DOC_ISSUES_TOKEN']}",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def find_comment(repository, issue):
    page = 1
    while True:
        comments = github(f"/repos/{repository}/issues/{issue}/comments?per_page=100&page={page}")
        found = next((c for c in comments if MARKER in (c.get("body") or "")), None)
        if found or len(comments) < 100:
            return found
        page += 1


def read_history(comment):
    match = HISTORY_MARKER.search((comment or {}).get("body") or "")
    try:
        return json.loads(match[1]) if match else []
    except ValueError:
        return []


def main(argv):
    dry_run = "--dry-run" in argv
    results = next((arg for arg in argv if not arg.startswith("--")), "junit.xml")
    if not Path(results).exists():
        print(f"Sem {results}: os testes não chegaram a rodar, nada a publicar.")
        return 0
    if not dry_run and not env.get("DOC_ISSUES_TOKEN"):
        print("::notice::DOC_ISSUES_TOKEN não configurado: o resultado não foi publicado nas issues das US.")
        return 0

    config = json.loads(CONFIG_PATH.read_text())
    repository = config["repository"]
    by_us = {}
    for test in collect(results):
        by_us.setdefault(test["us"], []).append(test)

    failures = 0
    for us, tests in sorted(by_us.items()):
        issue = config["issues"].get(us)
        if not issue:
            print(f"::warning::{us} tem E2E mas não está em tests/e2e/acceptance-issues.json.")
            continue
        try:
            if dry_run:
                print(f"--- {repository}#{issue} ({us}) ---\n{render(us, tests, [])}\n")
                continue
            comment = find_comment(repository, issue)
            body = {"body": render(us, tests, read_history(comment))}
            if comment:
                github(f"/repos/{repository}/issues/comments/{comment['id']}", "PATCH", body)
            else:
                github(f"/repos/{repository}/issues/{issue}/comments", "POST", body)
            print(f"{us}: {'atualizado' if comment else 'criado'} o comentário em {repository}#{issue}.")
        except Exception as error:  # um erro numa US não impede publicar as outras
            failures += 1
            print(f"::warning::{us}: não foi possível publicar em {repository}#{issue}: {error}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
