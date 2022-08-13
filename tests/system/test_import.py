import subprocess


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_import_metrics_folder_not_found_exception_handling():
    out, _, returncode = capture(
        ["measuresoftgram", "import", "sonarqube", "sonar-output-fake", "py"]
    )

    assert returncode == 0
    assert "Error: The folder was not found" in out.decode("utf-8")
