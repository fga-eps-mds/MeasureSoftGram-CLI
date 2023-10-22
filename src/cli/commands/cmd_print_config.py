import json
import logging
import os
import sys
from pathlib import Path

from rich.console import Console
from rich.prompt import Confirm
from staticfiles import DEFAULT_PRE_CONFIG

from src.cli.utils import print_error, print_info, print_panel, print_rule
from src.config.settings import FILE_CONFIG
from src.config.settings import DEFAULT_CONFIG_FILE_PATH
from src.config.settings import DEFAULT_CONFIG_PATH

logger = logging.getLogger("msgram")

def print_json_tree(data, indent="",isTop = True):
    if isTop:
        print_info("---------------------------- Listing Configuration Parameters ---------------------------\n\n")
   
    key = data.get("key")
    print_info(f"{indent}{key}")
   
    weight = data.get("weight", 0)
    print_info(f"{indent}Peso: {weight}%")

    if "subcharacteristics" in data:
        for subchar in data["subcharacteristics"]:
            print_info(f"{indent}Subcaracteristica (s):")
            print_json_tree(subchar, indent + "|      ",False)

    if "measures" in data:
        for measure in data["measures"]:
            print_info(f"{indent}Medida (s):")
            print_json_tree(measure, indent + "|      |       ",False)

    if "min_threshold" in data and "max_threshold" in data:
        min_threshold = data.get("min_threshold")
        max_threshold = data.get("max_threshold")
        print_info(f"{indent}Metrica (s):")
        print_info(f"{indent}|       [#458B00]coverage")
        print_info(f"{indent}|       Peso: {weight}%")
        print_info(f"{indent}|       Valores de referência: Min: {min_threshold} e Max: {max_threshold}")

def command_list_config(args):
    
    console = Console()
    console.clear()

    print_rule("MSGram", "[#708090] Reading of config file[/]:")

    if not (os.path.exists(DEFAULT_CONFIG_FILE_PATH)):
        print_info( f"[#A9A9A9] O arquivo de configuração não foi encontrado. Execute o comando msgram init para criá-lo." )
        exit()
    
    print_info(f"MSGram config file [bold red]'{FILE_CONFIG}'[/] exists already!")

    f = open(DEFAULT_CONFIG_FILE_PATH)
    data = json.load(f)


    for characteristic in data.get("characteristics", []):
        print_json_tree(characteristic)



    print_info("\n[#A9A9A9]Para editar o arquivo de configuração utilize em seu terminal o seguinte comando: vim <caminho_arquivo ../.msgram/.msgram/msgram.json>")