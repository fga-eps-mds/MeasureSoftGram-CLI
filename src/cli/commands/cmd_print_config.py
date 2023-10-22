from rich.console import Console

from src.cli.utils import  print_info,  print_rule

from src.config.settings import FILE_CONFIG
from src.config.settings import DEFAULT_CONFIG_FILE_PATH

import json
import os

def print_json_tree(data):
    result = []  # Initialize an empty list to store the output as strings
    stack = [(data, "")]

    while stack:
        data, indent = stack.pop()

        key = data.get("key")
        result.append(f"[#FFFFFF]\nCaracterística:")
        result.append(f"[#FFFFFF]{indent}[#458B00]{key}")

        weight = data.get("weight", 0)
        result.append(f"[#FFFFFF]{indent}Peso: [#458B00]{weight}%")

        if "subcharacteristics" in data:
            for subchar in data["subcharacteristics"]:
                result.append(f"[#FFFFFF]{indent}Subcaracteristica(s):")
                stack.append((subchar, f"{indent}|  "))

        if "measures" in data:
            result.append(f"[#FFFFFF]{indent}Medida(s):")
            for measure in data["measures"]:
                result.append(f"[#FFFFFF]{indent}|  [#458B00]{measure['key']}")
                result.append(f"[#FFFFFF]{indent}|  Peso: [#458B00]{measure['weight']}%")
                if "min_threshold" in measure and "max_threshold" in measure:
                    min_threshold = measure.get("min_threshold")
                    max_threshold = measure.get("max_threshold")
                    result.append(f"[#FFFFFF]{indent}|  Métrica(s):")
                    result.append(f"[#FFFFFF]{indent}|  |  Valores de referência: Min: [#458B00]{min_threshold} [#FFFFFF]e Max: [#458B00]{max_threshold}")
                    result.append(f"[#FFFFFF]{indent}|  Fim-Metrica(s)")
                result.append(f"[#FFFFFF]{indent}Fim-Medida(s)")
            result.append("[#FFFFFF]Fim-SubCaracterística")
            
    result.append("[#FFFFFF]Fim-Característica")

    # Join the result list into a single string with newlines
    return '\n'.join(result)

def command_list_config(args):
    console = Console()
    console.clear()

    print_rule("[#FFFFFF] Listing Configuration Parameters[/]:")

    if not (os.path.exists(DEFAULT_CONFIG_FILE_PATH)):
        print_info(f"[#A9A9A9] O arquivo de configuração não foi encontrado. Execute o comando msgram init para criá-lo.")
        exit()

    print_info(f"MSGram config file [bold red]'{FILE_CONFIG}'[/] exists already!")

    f = open(DEFAULT_CONFIG_FILE_PATH)

    data = json.load(f)

    for characteristic in data.get("characteristics", []):
        output_string = print_json_tree(characteristic)
        print_info(output_string)

    print_info(
        "\n[#A9A9A9]Para editar o arquivo de configuração utilize em seu terminal o seguinte comando: vim <caminho_arquivo ../.msgram/.msgram/msgram.json>"
    )

