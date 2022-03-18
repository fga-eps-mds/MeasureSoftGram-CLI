import os
import json
from parser import METRICS_SONAR

def fileReader():

    fileName = os.path.join( "C:\\", "Users", "pallo", "Downloads", "Bia", "MDS", "sonar.json")

    if fileName[-4:] != "json":
        raise Exception('ERRO: Apenas arquivos JSON são aceitos.')

    f = open(fileName, "r")
    jsonFile = json.load(f)

    checkSonarFormat(jsonFile)

    metrics = jsonFile["baseComponent"]["measures"]

    checkMetrics(metrics)
    checkExpectedMetrics(metrics)


def checkMetrics(metrics):

    for metric in metrics:

        try:
            value = float(metric["value"])
        except ValueError:
            raise Exception('''
                ERRO: A métrica "{}" é invalida.
                Valor: "{}"
            '''.format(metric["metric"], metric["value"]))


def checkExpectedMetrics(metrics):

    if len(metrics) != len(METRICS_SONAR):
        raise Exception('''
            ERRO: Quantidade de métricas recebidas é diferente das métricas esperadas.
            Quantidade de métricas recebidas: {}
            Quantidade de métricas esperadas: {}
        '''.format(len(metrics), len(METRICS_SONAR)))

    sortedRecievedMetrics = sorted(metrics, key=lambda d: d['metric'])
    sortedExpectedMetrics = sorted(METRICS_SONAR)

    for recieved, expected in zip(sortedRecievedMetrics, sortedExpectedMetrics):
        if recieved["metric"] != expected:
            raise Exception('''
                ERROR: As metricas informadas não coincidem com as métricas esperadas.
                Métrica informada: {}
                Métrica esperada: {}
            '''.format(recieved["metric"], expected))

def checkSonarFormat(jsonFile):
    attributes = list(jsonFile.keys())
    if len(attributes) != 3:
        raise Exception('ERROR, quantidade de atributos invalida')
    if attributes[0] != "paging" or attributes[1] != "baseComponent" or attributes[2] != "components":
        raise Exception('ERROR, atributos incorretos')
    
    baseComponent = jsonFile["baseComponent"]
    baseComponentAttributs = list(baseComponent.keys())
    if len(baseComponentAttributs) != 5:
        raise Exception('ERROR, Quantidade de atributos de baseComponent invalida')
    if baseComponentAttributs[0] != "id" or baseComponentAttributs[1] != "key" or baseComponentAttributs[2] != "name" or baseComponentAttributs[3] != "qualifier" or baseComponentAttributs[4] != "measures":
        raise Exception('ERROR, Atributos de baseComponent incorretos')