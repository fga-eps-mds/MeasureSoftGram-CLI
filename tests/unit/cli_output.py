import re


def normalize_cli_output(output: str) -> str:
    output = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", output)
    output = re.sub(r"\[[^\]]+\]", "", output)
    output = re.sub(r"\s+", " ", output)
    return output.strip()
