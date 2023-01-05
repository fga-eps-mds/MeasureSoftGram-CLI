import subprocess


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_show_help():
    out, err, returncode = capture(["msgram", "-h"])
    assert returncode == 0
    assert "usage: msgram [-h]" in out.decode("utf-8")

    out, err, returncode = capture(["msgram"])
    assert returncode == 0
    assert "usage: msgram [-h]" in out.decode("utf-8")
