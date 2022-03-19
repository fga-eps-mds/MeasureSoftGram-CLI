import json

METRICS_SONAR = [
    "files",
    "functions",
    "complexity",
    "comment_lines_density",
    "duplicated_lines_density",
    "coverage",
    "ncloc",
    "tests",
    "test_errors",
    "test_failures",
    "test_execution_time",
    "security_rating",
]

def file_reader(absolute_path):

    check_file_extension(absolute_path)
   
    f = open(absolute_path, "r")
    json_file = json.load(f)

    check_sonar_format(json_file)

    metrics = json_file["baseComponent"]["measures"]

    check_metrics(metrics)
    check_expected_metrics(metrics)

    return metrics


def check_metrics(metrics):

    for metric in metrics:

        try:
            float(metric["value"])
        except ValueError:
            raise TypeError('''
                ERRO: A métrica "{}" é invalida.
                Valor: "{}"
            '''.format(metric["metric"], metric["value"]))


def check_expected_metrics(metrics):

    if len(metrics) != len(METRICS_SONAR):
        raise TypeError('''
            ERRO: Quantidade de métricas recebidas é diferente das métricas esperadas.
            Quantidade de métricas recebidas: {}
            Quantidade de métricas esperadas: {}
        '''.format(len(metrics), len(METRICS_SONAR)))

    sorted_recieved_metrics = sorted(metrics, key=lambda d: d['metric'])
    sorted_expected_metrics = sorted(METRICS_SONAR)

    for recieved, expected in zip(sorted_recieved_metrics, sorted_expected_metrics):
        if recieved["metric"] != expected:
            raise TypeError('''
                ERROR: As metricas informadas não coincidem com as métricas esperadas.
                Métrica informada: {}
                Métrica esperada: {}
            '''.format(recieved["metric"], expected))

    return True


def check_sonar_format(json_file):
    attributes = list(json_file.keys())

    if len(attributes) != 3:
        raise TypeError('ERRO: Quantidade de atributos invalida.')
    if attributes[0] != "paging" or attributes[1] != "baseComponent" or attributes[2] != "components":
        raise TypeError('ERROR, atributos incorretos')
    
    base_component = json_file["baseComponent"]
    base_component_attributs = list(base_component.keys())

    if len(base_component_attributs) != 5:
        raise TypeError('ERROR, Quantidade de atributos de baseComponent invalida')
    if base_component_attributs[0] != "id" or base_component_attributs[1] != "key" or base_component_attributs[2] != "name" or base_component_attributs[3] != "qualifier" or base_component_attributs[4] != "measures":
        raise TypeError('ERROR, Atributos de baseComponent incorretos')
    
    return True
    
def check_file_extension(fileName):
    if fileName[-4:] != "json":
        raise TypeError('ERRO: Apenas arquivos JSON são aceitos.')
    
    return True
