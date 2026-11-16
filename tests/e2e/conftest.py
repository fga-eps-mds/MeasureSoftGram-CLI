"""Infra dos testes E2E: rodam o binário `msgram` de verdade, isolado em tmp_path e sem rede."""

import os
import subprocess

import pytest
from syrupy.extensions.json import JSONSnapshotExtension

from tests.e2e.support import NO_NETWORK


@pytest.fixture
def msgram_env(tmp_path):
    home = tmp_path / "home"
    home.mkdir()
    env = {k: v for k, v in os.environ.items() if k not in ("GITHUB_TOKEN", "LOG")}
    env.update(
        HOME=str(home),
        NO_COLOR="1",
        COLUMNS="120",
        TERM="dumb",
        COLORFGBG="0;15",  # evita o subprocess de detecção de tema do SO
        HTTPS_PROXY=NO_NETWORK,
        HTTP_PROXY=NO_NETWORK,
        NO_PROXY="",
    )
    return env


@pytest.fixture
def msgram(tmp_path, msgram_env):
    """Roda `msgram --theme light <args>` com cwd=tmp_path (isola `.msgram` padrão e `.env`)."""

    def run(*args, input=""):
        result = subprocess.run(
            ["msgram", "--theme", "light", *map(str, args)],
            cwd=tmp_path,
            env=msgram_env,
            input=input,
            capture_output=True,
            text=True,
            timeout=120,
        )
        output = result.stdout + result.stderr
        assert "Traceback" not in output, output
        return result

    return run


@pytest.fixture
def json_snapshot(snapshot):
    return snapshot.use_extension(JSONSnapshotExtension)
