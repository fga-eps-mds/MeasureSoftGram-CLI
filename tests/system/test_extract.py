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
    msg, _, returncode = capture(
        [
            "msgram",
            "extract",
            "-ep",
            config_dirpath,
            "-sp",
            "sonar-output-fake",
        ]
    )

    assert returncode == 1
    message = "No JSON files found in the specified data_path:"
    assert message in msg.decode("utf-8")
    shutil.rmtree(config_dirpath)


def test_extract_metrics_config_folder_not_found_exception_handling():
    msg, _, returncode = capture(
        [
            "msgram",
            "extract",
            "-ep",
            "config-fake",
            "-sp",
            "sonar-output-fake",
        ]
    )

    assert returncode == 1
    assert "FileNotFoundError: extract directory" in msg.decode("utf-8")
