import json
import logging
import sys
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm
from rich.tree import Tree
from rich import print
from rich.prompt import Prompt
from staticfiles import DEFAULT_PRE_CONFIG as pre_config

from src.cli.utils import print_error, print_info, print_panel, print_rule
from src.config.settings import FILE_CONFIG

logger = logging.getLogger("msgram")

def print_json_tree(data, indent=""):
    output = []
    output.append("------------------------------ Listing Configuration Parameters ------------------------------")
    key = data.get("key")
    weight = data.get("weight", 0)
    output.append(f"{indent}{key}\n")
    output.append(f"{indent}Peso: {weight}%")

    if "subcharacteristics" in data:
        for subchar in data["subcharacteristics"]:
            output.append(f"{indent}Subcaracteristica (s):")
            output.extend(print_json_tree(subchar, indent + "|      "))
            output.append(f"{indent}Fim-Subcaracteristica(s)")

    if "measures" in data:
        for measure in data["measures"]:
            output.append(f"{indent}Medida (s):")
            output.extend(print_json_tree(measure, indent + "|      |       "))
            output.append(f"{indent}Fim-Medida(s)")

    if "min_threshold" in data and "max_threshold" in data:
        min_threshold = data.get("min_threshold")
        max_threshold = data.get("max_threshold")
        output.append(f"{indent}Metrica (s):")
        output.append(f"{indent}|       coverage")
        output.append(f"{indent}|       Peso: {weight}%")
        output.append(f"{indent}|       Valores de referência: Min: {min_threshold} e Max: {max_threshold}")
        output.append(f"{indent}Fim-Metrica(s)")

    output.append(f"{indent}Fim-Caracteristica")
    return output

def command_list_config():
    try:
        #config_path = args[none]
        print("teste")
    except Exception as e:
        logger.error(f"KeyError: args[{e}] - non-existent parameters")
        print_error(f"Parâmetro inválido. Para exibir a configuração do modelo, informe o parâmetro -config!")
        sys.exit(1)

    logger.debug(config_path)
    file_path = config_path / FILE_CONFIG

    console = Console()
    console.clear()
    print_rule("MSGram", "[#708090] Reading of config file[/]:")

    data_print = []
    output = []

    if not config_path.exists():
        output.append("\n [#A9A9A9] O arquivo de configuração não foi encontrado. Execute o comando msgram init para criá-lo.")
    else:
        output.append(f"MSGram config file [bold red]'{FILE_CONFIG}'[/] exists already!")
        data_print = open_json_file(file_path)
        for characteristic in data_print.get("characteristics", []):
            output.extend(print_json_tree(characteristic))

    output = "\n".join(output)
    print_info(output)

    print_info("\n[#A9A9A9]Para editar o arquivo de configuração utilize em seu terminal o seguinte comando: vim <caminho_arquivo ../.msgram/.msgram/msgram.json>")



# def command_list_config(args):
#     try:
#         config_path: Path = args["config"]

#     except Exception as e:
#         logger.error(f"KeyError: args[{e}] - non-existent parameters")
#         print_error(f"Parâmetro inválido. Para exibir a configuração do modelo, informe o parâmetro -config!")
#         sys.exit(1)

#     logger.debug(config_path)
#     file_path = config_path / FILE_CONFIG

#     console = Console()
#     console.clear()
#     print_rule("MSGram", "[#708090] Reading of config file[/]:")

#     data_print = {}
#     if not config_path.exists():
#         print_info(f"O arquivo de configuração não foi encontrado. Execute o comando msgram init para criá-lo.") 
#     else:
#         print_info(f"MSGram config file [bold red]'{FILE_CONFIG}'[/] exists already!")
#         data_print = open_json_file(file_path)

#         import json

# def print_json_tree(data, indent=""):
#     print("---------------------------- Listing Configuration Parameters ---------------------------\n\n")
#     key = data.get("key")
#     weight = data.get("weight", 0)
#     print(f"{indent}{key} \n\n")
#     print(f"{indent}Peso: {weight}%")

#     if "subcharacteristics" in data:
#         for subchar in data["subcharacteristics"]:
#             print(f"{indent}Subcaracteristica (s):")
#             print_json_tree(subchar, indent + "|      ")

#     if "measures" in data:
#         for measure in data["measures"]:
#             print(f"{indent}Medida (s):")
#             print_json_tree(measure, indent + "|      |       ")

#     if "min_threshold" in data and "max_threshold" in data:
#         min_threshold = data.get("min_threshold")
#         max_threshold = data.get("max_threshold")
#         print(f"{indent}Metrica (s):")
#         print(f"{indent}|       coverage [Verde]")
#         print(f"{indent}|       Peso: {weight}%")
#         print(f"{indent}|       Valores de referência: Min: {min_threshold} e Max: {max_threshold}")

#     # # Carregue o JSON externo
#     # with open('seuarquivo.json', 'r') as json_file:
#     #     json_data = json.load(json_file)

#     # Comece a partir das características
#     for characteristic in json_data.get("characteristics", []):
#         print_json_tree(characteristic)

# print_info("\n[#A9A9A9]Para editar o arquivo de configuração utilize em seu terminal o seguinte comando: vim <caminho_arquivo ../.msgram/.msgram/msgram.json>")


# def get_obj_by_element(object_list: list, element_key: str, element_to_find):
#     return next((obj for obj in object_list if obj[element_key] == element_to_find), {})

# def show_tree(data_calculated):
#     tsqmi = data_calculated["tsqmi"][0]
#     characteristics = data_calculated["characteristics"]
#     subcharacteristics = data_calculated["subcharacteristics"]
#     measures = data_calculated["measures"]
#     metrics = data_calculated["metrics"]

#     print("---------------------------- Listing Configuration Parameters ---------------------------\n\n")
#     tsqmi_tree = Tree("")

#     for char_c, char in zip(pre_config["characteristics"], characteristics):
#         char_tree = tsqmi_tree.add(f"{char['Peso']}: [green]{char['weight']}")

#         for subchar_c in char_c["subcharacteristics"]:
#             subchar = get_obj_by_element(subcharacteristics, "key", subchar_c["key"])
#             sub_char_tree = char_tree.add(f"{subchar['Peso']}: [green]{subchar['weight']}")

#             for measure_c in subchar_c["measures"]:
#                 measure = get_obj_by_element(measures, "key", measure_c["key"])
#                 sub_char_tree.add(f"{measure['Peso']}: [green]{measure['weight']}")

#                 for metric_c in measure_c["metrics"]:
#                     metric = get_obj_by_element(metrics, "metric", metric_c["metric"])
#                     sub_char_tree.add(f"{metric['metric']} {metric['value']}")

#     print(tsqmi_tree)