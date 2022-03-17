import os

def fileReader():

    fileName = os.path.join( "D:\\", "Desktop", "vit", "Estudo", "Unb", "MDS", "MeasureSoftGram", "arquivos", "sonar.json")

    if fileName[-4:]!="json":
        print("Nao json")
        raise ValueError('ERROR, Apenas arquivos json são aceitos')
        
    #f = open(fileName, "r")
    #print(f.read())