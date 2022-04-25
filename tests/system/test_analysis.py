import subprocess


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate()
    return out, err, proc.returncode


def test_analysis_error_not_existent_ID():
    out, _, return_code = capture(
        ["measuresoftgram", "analysis", "6265b525ab15bc00c4effbd1"]
    )

    assert return_code == 0
    assert (
        "There is no pre configurations with ID 6265b525ab15bc00c4effbd1"
        in out.decode("utf-8")
    )


def test_analysis_not_valid_ID():
    out, _, return_code = capture(["measuresoftgram", "analysis", "ABCDE123"])

    assert return_code == 0
    assert "ABCDE123 is not a valid ID" in out.decode("utf-8")
