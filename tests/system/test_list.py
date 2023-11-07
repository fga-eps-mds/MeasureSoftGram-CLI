import subprocess
import tempfile
import shutil

from src.config.settings import DEFAULT_CONFIG_FILE_PATH


def capture(command):

    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_msgram_list_should_execute_sucessfully():
    temp_path = tempfile.mkdtemp()

    _, _, returncode = capture(["msgram", "init", "-cp", DEFAULT_CONFIG_FILE_PATH])

    assert returncode == 0
    shutil.rmtree(temp_path)
