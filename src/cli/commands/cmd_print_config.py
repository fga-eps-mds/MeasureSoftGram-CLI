from rich.console import Console
from src.cli.utils import  print_info,  print_rule
from src.config.settings import FILE_CONFIG
from src.config.settings import DEFAULT_CONFIG_FILE_PATH
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
    measure_to_metric["duplication_absense"] = ['duplication_lines_density']
    
    while stack:
        data, indent = stack.pop()
        key = data.get("key")

        if is_top:
            result.append(f"[#FFFFFF]\nCaracterística:")
            is_top = False
        result.append(f"[#FFFFFF]{indent}[#00FF00]{key}")

        weight = data.get("weight", 0)
        result.append(f"[#FFFFFF]{indent}Peso: [#00FF00]{weight}%")

        if "subcharacteristics" in data:
            for subchar in data["subcharacteristics"]:
                result.append(f"[#FFFFFF]{indent}Subcaracteristica(s):")
                stack.append((subchar, f"{indent}│  "))  # Use the ASCII character │ (code 179)

        if "measures" in data:
            for measure in data["measures"]:
                measure_key = measure.get("key")
                result.append(f"[#FFFFFF]{indent}│  [#00FF00]{measure_key}")  # Use the ASCII character │ (code 179)
                result.append(f"[#FFFFFF]{indent}│  Peso: [#00FF00]{measure['weight']}%")
                if "min_threshold" in measure and "max_threshold" in measure:
                    min_threshold = measure.get("min_threshold")
                    max_threshold = measure.get("max_threshold")
                    result.append(f"[#FFFFFF]{indent}│  Métrica(s):")  # Use the ASCII character │ (code 179)
                    result.append(f"[#FFFFFF]{indent}│  │  Valores de referência: Min: [#00FF00]{min_threshold} [#FFFFFF]e Max: [#00FF00]{max_threshold}")
                    metrics = measure_to_metric.get(measure_key, [])  # Get associated metrics
                    for metric in metrics:
                        result.append(f"[#FFFFFF]{indent}│  │  [#00FF00]{metric}")  # Print metrics in green color
                    result.append(f"[#FFFFFF]{indent}│  Fim-Metrica(s)")
                
                result.append(f"[#FFFFFF]{indent}│  Fim-Medida(s)")

            result.append("[#FFFFFF]Fim-SubCaracterística")
            
    result.append("[#FFFFFF]Fim-Característica")

    return '\n'.join(result)




def command_list_config(args):
    console = Console()
    console.clear()

    print_rule("[#FFFFFF] Listing Configuration Parameters[/]:")

    if not (os.path.exists(DEFAULT_CONFIG_FILE_PATH)):
        print_info(f"[#A9A9A9] O arquivo de configuração não foi encontrado. Execute o comando msgram init para criá-lo.")
        exit()

    print_info(f"MSGram config file [bold red]'{FILE_CONFIG}'[/] exists already!")

    #get data
    f = open(DEFAULT_CONFIG_FILE_PATH)

    data = json.load(f)

    #dictionary of metrics and measures
    
    for characteristic in data.get("characteristics", []):
        output_string = print_json_tree(characteristic)
        print_info(output_string)

    print_info(
        "\n[#A9A9A9]Para editar o arquivo de configuração utilize em seu terminal o seguinte comando: vim <caminho_arquivo ../.msgram/.msgram/msgram.json>"
    )

