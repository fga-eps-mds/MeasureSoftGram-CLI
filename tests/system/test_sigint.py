import signal
import subprocess
from time import sleep
# import pytest


def capture(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    sleep(0.5)

    proc.send_signal(signal.SIGINT)

    out, err = proc.communicate()

    return out, err, proc.returncode


# @pytest.mark.xfail
# def test_sigint():
#     out, err, returncode = capture(["measuresoftgram", "create"])

#     print(out)
#     print(err)
#     assert returncode == 0
#     assert "\n\nExiting MeasureSoftGram..." in out.decode("utf-8")
