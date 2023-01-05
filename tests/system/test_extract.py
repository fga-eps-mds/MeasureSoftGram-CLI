import subprocess
import tempfile
import shutil


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_extract_metrics_folder_not_found_exception_handling():
    config_dirpath = tempfile.mkdtemp()
    _, err, returncode = capture(
        ["msgram", "extract", "sonarqube", config_dirpath, "sonar-output-fake", "py"]
    )

    assert returncode == 1
    assert "Error: The folder was not found" in err.decode("utf-8")
    shutil.rmtree(config_dirpath)


def test_extract_metrics_config_folder_not_found_exception_handling():
    _, err, returncode = capture(
        ["msgram", "extract", "sonarqube", "config-fake", "sonar-output-fake", "py"]
    )

    assert returncode == 1
    assert "FileNotFoundError: config directory" in err.decode("utf-8")
