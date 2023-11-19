from rich.console import Console
from src.cli.utils import print_info, print_rule, print_error

from src.config.settings import FILE_CONFIG, DEFAULT_CONFIG_PATH, DEFAULT_CONFIG_FILE_PATH

from pathlib import Path

import json
import os


def print_json_tree(data):
    result = []
    stack = [(data, "")]
    is_top = True

    measure_to_metric = {}
    measure_to_metric["passed_tests"] = ['test_success_density']
    measure_to_metric["test_builds"] = ['tests', 'tests_execution_time']
    measure_to_metric["test_coverage"] = ['coverage']
    measure_to_metric["non_complex_file_density"] = ['complexity_functions', 'total_number_of_files']
    measure_to_metric["commented_file_density"] = ['commented_lines_density']
    measure_to_metric["duplication_absence"] = ['duplication_lines_density']

    while stack:
        data, indent = stack.pop()
        key = data.get("key")

        if is_top:
            result.append("[#FFFFFF]\nCaracterística:")
            is_top = False
        result.append(f"[#FFFFFF]{indent}[#00FF00]{key}")

        weight = data.get("weight", 0)
        result.append(f"[#FFFFFF]{indent}Peso: [#00FF00]{weight}%")

        if "subcharacteristics" in data:
            for subchar in data["subcharacteristics"]:
                result.append(f"[#FFFFFF]{indent}Sub-característica(s):")
                stack.append((subchar, f"{indent}│  "))  # Use the ASCII character │ (code 179)

        if "measures" in data:
            for measure in data["measures"]:
                result.append(f"[#FFFFFF]{indent}│  Medida(s):")
                measure_key = measure.get("key")
                result.append(f"[#FFFFFF]{indent}{indent}│  [#00FF00]{measure_key}")
                result.append(f"[#FFFFFF]{indent}{indent}│  Peso: [#00FF00]{measure['weight']}%")
                if "min_threshold" in measure and "max_threshold" in measure:
                    min_threshold = measure.get("min_threshold")
                    max_threshold = measure.get("max_threshold")
                    result.append(f"[#FFFFFF]{indent}{indent}│  Métrica(s):")
                    metrics = measure_to_metric.get(measure_key, [])  # Get associated metrics
                    for metric in metrics:
                        result.append(f"[#FFFFFF]{indent}{indent}│  └─[#00FF00]{metric}")
                        min_max = f"Min = [#00FF00]{min_threshold} [#FFFFFF]e Max = [#00FF00]{max_threshold}"
                    result.append(f"[#FFFFFF]{indent}{indent}│  │ Valores de referência: {min_max}")
                    result.append(f"[#FFFFFF]{indent}{indent}│  Fim-Métrica(s)")
                result.append(f"[#FFFFFF]{indent}│  Fim-Medida(s)")
            result.append("[#FFFFFF]Fim-SubCaracterística")
    result.append("[#FFFFFF]Fim-Característica")

    return '\n'.join(result)


def command_list(args):

    console = Console()
    console.clear()

    file_path = DEFAULT_CONFIG_FILE_PATH
    try:
        config_path: Path = args["config_path"]

        if config_path != DEFAULT_CONFIG_PATH:
            print_info("[#A9A9A9] Será usado arquivo informado pelo usuário: ")
            file_path = str(config_path) + "/msgram.json"
        else:
            print_info(
                "[#A9A9A9]Não foi informado caminho do arquivo de configuração, será usado caminho padrão."
                )

    except Exception as e:
        print_error(f"KeyError: args[{e}] - non-existent parameters")
        exit(1)

    print_rule("[#FFFFFF]Listing Configuration Parameters")

    if not (os.path.exists(file_path)):
        print_info("[#A9A9A9] O arquivo de configuração não foi encontrado. \n")
        print_info("Execute o comando 'msgram init' no projeto desejado para criá-lo.\n")
        print_info("Ou use 'msgram init --config_path <path>' para informar o caminho ate o arquivo.")
        exit()

    print_info(f"MSGram config file [bold red]'{FILE_CONFIG}'[/] exists already!")

    f = open(file_path)

    data = json.load(f)

    for characteristic in data.get("characteristics", []):
        output_string = print_json_tree(characteristic)
        print_info(output_string)

    print_info("\n[#A9A9A9]Para editar o arquivo de configuração utilize em seu terminal o seguinte comando:")
    print_info("vim .msgram/msgram.json\n")
