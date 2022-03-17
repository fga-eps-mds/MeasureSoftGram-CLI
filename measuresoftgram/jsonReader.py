import os
import json
from parser import METRICS_SONAR

def fileReader():

    fileName = os.path.join( "D:\\", "Desktop", "vit", "Estudo", "Unb", "MDS", "MeasureSoftGram", "arquivos", "sonar.json")

    if fileName[-4:] != "json":
        raise Exception('ERRO: Apenas arquivos JSON são aceitos.')

    f = open(fileName, "r")
    jsonFile = json.load(f)

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

