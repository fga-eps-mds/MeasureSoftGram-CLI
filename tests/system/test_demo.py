import subprocess


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_msgram_demo_should_run_end_to_end(tmp_path):
    output_path = tmp_path / "msgram-demo"

    out, _, returncode = capture(
        ["msgram", "demo", "-o", str(output_path)]
    )

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
