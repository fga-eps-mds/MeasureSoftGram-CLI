from fileinput import filename
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

    print(metrics)