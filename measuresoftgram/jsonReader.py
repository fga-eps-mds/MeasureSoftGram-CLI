from fileinput import filename
from logging import raiseExceptions
import os
import json

def fileReader():

    fileName = os.path.join( "D:\\", "Desktop", "vit", "Estudo", "Unb", "MDS", "MeasureSoftGram", "arquivos", "sonar.json")

    if fileName[-4:]!="json":
        print("Nao json")
        raise ValueError('ERROR, Apenas arquivos json são aceitos')

    f = open(fileName, "r")
    jsonFile = json.load(f)

    metrics = jsonFile["baseComponent"]["measures"]

    checkMetrics(metrics)

def checkMetrics(metrics):

    for metric in metrics:

        try:
            value = float(metric["value"])
        except ValueError:
            raise Exception("ERROR, a métrica '{}' é invalida".format( metric["metric"] ))

        if value is None:
            raise ValueError('ERROR, Metrica NaN')