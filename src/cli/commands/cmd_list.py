from src.cli.utils import clear_console, color_tag, print_error, print_info, print_rule

from src.config.settings import (
    FILE_CONFIG,
    DEFAULT_CONFIG_PATH,
    DEFAULT_CONFIG_FILE_PATH,
)

from pathlib import Path

import json
import os


def print_json_tree(data):
    result = []
    stack = [(data, "")]
    is_top = True
    main_color = color_tag("main")
    success_color = color_tag("success")

    measure_to_metric = {}
    measure_to_metric["passed_tests"] = ["tests", "test_failures", "test_errors"]
    measure_to_metric["test_builds"] = ["tests", "test_execution_time"]
    measure_to_metric["test_coverage"] = ["coverage"]
    measure_to_metric["non_complex_file_density"] = ["functions", "complexity"]
    measure_to_metric["commented_file_density"] = ["comment_lines_density"]
    measure_to_metric["duplication_absense"] = ["duplicated_lines_density"]
    measure_to_metric["team_throughput"] = ["resolved_issues", "total_issues"]
    measure_to_metric["ci_feedback_time"] = ["sum_ci_feedback_times", "total_builds"]

    while stack:
        data, indent = stack.pop()
        key = data.get("key")

        if is_top:
            result.append(f"{main_color}\nCaracterística:")
            is_top = False
        result.append(f"{main_color}{indent}{success_color}{key}")

        weight = data.get("weight", 0)
        result.append(f"{main_color}{indent}Peso: {success_color}{weight}%")

        if "subcharacteristics" in data:
            for subchar in data["subcharacteristics"]:
                result.append(f"{main_color}{indent}Sub-característica(s):")
                stack.append(
                    (subchar, f"{indent}│  ")
                )  # Use the ASCII character │ (code 179)

        if "measures" in data:
            for measure in data["measures"]:
                result.append(f"{main_color}{indent}│  Medida(s):")
                measure_key = measure.get("key")
                result.append(
                    f"{main_color}{indent}{indent}│  {success_color}{measure_key}"
                )
                result.append(
                    f"{main_color}{indent}{indent}│  Peso: {success_color}{measure['weight']}%"
                )
                if "min_threshold" in measure and "max_threshold" in measure:
                    min_threshold = measure.get("min_threshold")
                    max_threshold = measure.get("max_threshold")
                    result.append(f"{main_color}{indent}{indent}│  Métrica(s):")
                    metrics = measure_to_metric.get(
                        measure_key, []
                    )  # Get associated metrics
                    min_max = ""
                    for metric in metrics:
                        result.append(
                            f"{main_color}{indent}{indent}│  └─{success_color}{metric}"
                        )
                        min_max = (
                            f"Min = {success_color}{min_threshold} {main_color}"
                            f"e Max = {success_color}{max_threshold}"
                        )
                    result.append(
                        f"{main_color}{indent}{indent}│  │ Valores de referência: {min_max}"
                    )
                    result.append(f"{main_color}{indent}{indent}│  Fim-Métrica(s)")
                result.append(f"{main_color}{indent}│  Fim-Medida(s)")
            result.append(f"{main_color}Fim-SubCaracterística")
    result.append(f"{main_color}Fim-Característica")

    return "\n".join(result)


def command_list(args):
    clear_console()

    file_path = DEFAULT_CONFIG_FILE_PATH
    try:
        config_path: Path = args["config_path"]

        if config_path != DEFAULT_CONFIG_PATH:
            print_info("Será usado arquivo informado pelo usuário: ")
            file_path = str(config_path) + "/msgram.json"
        else:
            print_info(
                "Não foi informado caminho do arquivo de configuração, será usado caminho padrão."
            )

    except Exception as e:
        print_error(f"KeyError: args[{e}] - non-existent parameters")
        exit(1)

    print_rule("Listing Configuration Parameters")

    if not (os.path.exists(file_path)):
        print_info("O arquivo de configuração não foi encontrado. \n")
        print_info(
            "Execute o comando 'msgram init' no projeto desejado para criá-lo.\n"
        )
        print_info(
            "Ou use 'msgram init --config_path <path>' para informar o caminho ate o arquivo."
        )
        exit()

    print_info(f"MSGram config file '{FILE_CONFIG}' exists already!")

    f = open(file_path)

    data = json.load(f)

    for characteristic in data.get("characteristics", []):
        output_string = print_json_tree(characteristic)
        print_info(output_string)

    print_info(
        "\nPara editar o arquivo de configuração utilize em seu terminal o seguinte comando:"
    )
    print_info("vim .msgram/msgram.json\n")
