# import subprocess


# def capture(command):
#     proc = subprocess.Popen(
#         command,
#         stdout=subprocess.PIPE,
#         stderr=subprocess.PIPE,
#     )
#     out, err = proc.communicate()
#     return out, err, proc.returncode


# def test_analysis_return_code_invalid():
#     out, _, returncode = capture(["measuresoftgram", "analysis", "81357858"])

#     assert returncode == 1
