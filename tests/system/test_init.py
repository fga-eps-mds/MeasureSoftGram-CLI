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


def test_msgram_init_should_execute_sucessfully():
    temp_path = tempfile.mkdtemp()
    dir_path = f"{temp_path}/.msgram"

    _, _, returncode = capture(
        ["msgram", "init", "-cp", dir_path]
    )

    assert returncode == 0
    shutil.rmtree(temp_path)


def test_init_should_create_pre_config_in_existent_directory():
    temp_path = tempfile.mkdtemp()

    _, err, returncode = capture(
        ["msgram", "init", "-cp", temp_path]
    )

    assert returncode == 0
    shutil.rmtree(temp_path)
