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

def print_json_tree(data, indent="", isTop = True):
    key = data.get("key")
    value = data.get("metric")

    if isTop:
        print_info(f"[#FFFFFF]\nCaracterística:")
        print_info(f"[#FFFFFF]{indent}{indent}[#458B00]{key}")
    else:
        print_info(f"[#FFFFFF]{indent}{indent}[#458B00]{key}")
   
    weight = data.get("weight", 0)
    print_info(f"[#FFFFFF]{indent}{indent}Peso: [#458B00]{weight}%")

    if "subcharacteristics" in data:
        for subchar in data["subcharacteristics"]:
            print_info(f"[#FFFFFF]{indent}Subcaracteristica (s):")
            print_json_tree(subchar, indent + "|  ",False)
            print_info(f"[#FFFFFF]{indent}{indent}Fim-Subcaracterística\n")

    if "measures" in data:
        for measure in data["measures"]:
            print_info(f"[#FFFFFF]{indent}{indent}Medida (s):")
            print_json_tree(measure, indent + "|  ",False)
            print_info(f"[#FFFFFF]{indent}{indent}Fim-Medida(s)\n")

    if "min_threshold" in data and "max_threshold" in data:
            print_info(f"[#FFFFFF]{indent}{indent}Métrica (s):")
            value = data.get("metric")
            #print_info("{indent} |     |     |      {value}")
            min_threshold = data.get("min_threshold")
            max_threshold = data.get("max_threshold")
            print_info(f"[#FFFFFF]{indent}|    Valores de referência: Min: [#458B00]{min_threshold} [#FFFFFF]e Max: [#458B00]{max_threshold}")
            print_info(f"[#FFFFFF]{indent}{indent}Fim-Metrica(s)\n")

def command_list_config(args):
    console = Console()
    console.clear()

    print_rule("[#FFFFFF] Listing Configuration Parameters[/]:")

    if not (os.path.exists(DEFAULT_CONFIG_FILE_PATH)):
        print_info( f"[#A9A9A9] O arquivo de configuração não foi encontrado. Execute o comando msgram init para criá-lo." )
        exit()
    
    print_info(f"MSGram config file [bold red]'{FILE_CONFIG}'[/] exists already!")

    f = open(DEFAULT_CONFIG_FILE_PATH)
    
    data = json.load(f)

    isTop = True
    for data in data.get("characteristics", []):
        print_json_tree(data, "", isTop)
        print_info(f"[#FFFFFF]Fim-Característica\n")
        isTop = False

    print_info("\n[#A9A9A9]Para editar o arquivo de configuração utilize em seu terminal o seguinte comando: vim <caminho_arquivo ../.msgram/.msgram/msgram.json>")