import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

from src.cli.commands import cmd_demo


def capture(command, env=None, cwd=None):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
        cwd=cwd,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def _build_and_install_wheel(tmp_path: Path) -> Path:
    repo_root = Path(__file__).resolve().parents[2]
    pkg_src = tmp_path / "pkg_src"
    pkg_src.mkdir()
    for item in ("pyproject.toml", "README.md", "LICENSE"):
        shutil.copy2(repo_root / item, pkg_src / item)
    shutil.copytree(repo_root / "src", pkg_src / "src")

    wheel_dir = tmp_path / "dist"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "wheel",
            str(pkg_src),
            "--no-deps",
            "--no-build-isolation",
            "-w",
            str(wheel_dir),
        ],
        check=True,
    )
    wheel_file = next(wheel_dir.glob("msgram-*.whl"))

    site_dir = tmp_path / "site"
    subprocess.run(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--no-deps",
            "--target",
            str(site_dir),
            str(wheel_file),
        ],
        check=True,
    )
    return site_dir


def test_msgram_demo_should_run_end_to_end(tmp_path):
    output_path = tmp_path / "msgram-demo"

    out, _, returncode = capture(["msgram", "demo", "-o", str(output_path)])

    assert returncode == 0
    assert "Demo finished successfully!" in out.decode("utf-8")

    # The pipeline must have produced the config and the calculated result.
    assert (output_path / "msgram.json").is_file()
    assert (output_path / "calc_msgram.csv").is_file()
    assert any(output_path.glob("*.metrics"))


def test_msgram_demo_json_output(tmp_path):
    output_path = tmp_path / "msgram-demo-json"

    _, _, returncode = capture(
        ["msgram", "demo", "-o", str(output_path), "-of", "json"]
    )

    assert returncode == 0
    assert (output_path / "calc_msgram.json").is_file()


def test_find_raw_data_dir_fallback_and_not_found(tmp_path, monkeypatch):
    missing_dir = tmp_path / "missing"
    fallback_dir = tmp_path / "examples" / "analytics-raw-data"
    fallback_dir.mkdir(parents=True)
    (fallback_dir / "sample.json").write_text("{}")

    monkeypatch.setattr(
        cmd_demo, "_candidate_raw_data_dirs", lambda: [missing_dir, fallback_dir]
    )
    assert cmd_demo.find_raw_data_dir() == fallback_dir

    monkeypatch.setattr(cmd_demo, "_candidate_raw_data_dirs", lambda: [missing_dir])
    with pytest.raises(FileNotFoundError, match="Could not find the embedded sample"):
        cmd_demo.find_raw_data_dir()


def test_msgram_demo_from_installed_wheel(tmp_path):
    site_dir = _build_and_install_wheel(tmp_path)
    packaged_data = site_dir / "src" / "cli" / "resources" / "demo_data"
    assert any(packaged_data.glob("*.json"))

    env = {**os.environ, "PYTHONPATH": str(site_dir)}
    out, err, returncode = capture(
        [
            sys.executable,
            "-c",
            "from src.cli.commands.cmd_demo import find_raw_data_dir; "
            "print(find_raw_data_dir())",
        ],
        env=env,
        cwd=str(tmp_path),
    )
    assert returncode == 0, err.decode("utf-8")
    assert Path(out.decode("utf-8").strip()) == packaged_data

    output_path = tmp_path / "msgram-demo-wheel"
    msgram_bin = str(site_dir / "bin" / "msgram")
    out, err, returncode = capture(
        [msgram_bin, "demo", "-o", str(output_path), "-of", "json"],
        env=env,
        cwd=str(tmp_path),
    )
    assert returncode == 0, err.decode("utf-8")
    assert "Demo finished successfully!" in out.decode("utf-8")

    config_path = output_path / "msgram.json"
    result_path = output_path / "calc_msgram.json"
    default_tsqmi = json.loads(result_path.read_text())[0]["tsqmi"][0]["value"]

    config = json.loads(config_path.read_text())
    config["characteristics"] = [
        c for c in config["characteristics"] if c["key"] != "reliability"
    ]
    weights = {"maintainability": 80, "functional_suitability": 20}
    for characteristic in config["characteristics"]:
        characteristic["weight"] = weights[characteristic["key"]]
    config_path.write_text(json.dumps(config))

    _, err, returncode = capture(
        [msgram_bin, "demo", "-o", str(output_path), "-of", "json"],
        env=env,
        cwd=str(tmp_path),
    )
    assert returncode == 0, err.decode("utf-8")
    assert json.loads(config_path.read_text()) == config
    edited_tsqmi = json.loads(result_path.read_text())[0]["tsqmi"][0]["value"]
    assert edited_tsqmi != default_tsqmi
