from fileinput import filename
from logging import raiseExceptions
import os
import json
from parser import METRICS_SONAR

def fileReader():

    fileName = os.path.join( "D:\\", "Desktop", "vit", "Estudo", "Unb", "MDS", "MeasureSoftGram", "arquivos", "sonar.json")

    if fileName[-4:]!="json":
        print("Nao json")
        raise ValueError('ERROR, Apenas arquivos json são aceitos')

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
            raise Exception("ERROR, a métrica '{}' é invalida".format( metric["metric"] ))

        if value is None:
            raise ValueError('ERROR, Metrica NaN')

def checkExpectedMetrics(metrics):

    if len(metrics) != len(METRICS_SONAR):
        raise Exception("ERROR, a quantidade de métricas recebidas e diferente das métricas esperadas")

    newlist = sorted(metrics, key=lambda d: d['metric'])
    sortedMetrics = sorted(METRICS_SONAR)

    i = 0
    while i < len(metrics):
        if newlist[i]["metric"] != sortedMetrics[i]:
            raise Exception("ERROR, as metricas informadas não coincidem")
        i = i + 1
