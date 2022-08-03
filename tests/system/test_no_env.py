import subprocess


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    out, err = proc.communicate()

    return out, err, proc.returncode


# def test_no_env():
#     out, err, returncode = capture(["measuresoftgram", "create", "path"])
#     assert returncode == 1
    # FIXME
    # assert "Name or service not known" in err.decode("utf-8")
