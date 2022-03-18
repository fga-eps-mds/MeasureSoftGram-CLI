from measuresoftgram import jsonReader
import pytest
import json


def test_ValidFileExtension():
    '''
        Testa se a extensão do arquivo é válida (ex: .json)
    '''

    fileName = "sonar.json" 

    assert jsonReader.checkFileExtension(fileName) is True


def test_notValidFileExtension():
    '''
        Testa se a extensão do arquivo não é válida (ex: .txt, .png, .pdf)
    '''

    fileName = "sonar.txt"
    
    with pytest.raises(Exception): 
        jsonReader.checkFileExtension(fileName)


def test_validSonarFormat():
    '''
        Testa se um objeto json fornecido tem a formatação do Sonar
    '''

    relativeFilePath = "tests/utils/sonar.json"
    f = open(relativeFilePath, "r")
    jsonFile = json.load(f)

    assert jsonReader.checkSonarFormat(jsonFile) is True


def test_ifThereIsLessThanExpectedSonarAttributes():
    '''
        Testa se um objeto json fornecido possui menos atributos
        do que o esperado
    '''

    jsonFile = \
    {
        "paging": {
            "pageIndex": 1,
            "pageSize": 100,
            "total": 5
        },
        "baseComponent": {
            "id": "AX9FgyLHNIj_v_uQK41e",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI",
            "name": "2021-2-MeasureSoftGram-CLI",
            "qualifier": "TRK",
            "measures": [{
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True
                }
            ]
        }
    }
    
    with pytest.raises(Exception) as exec_info:
        jsonReader.checkSonarFormat(jsonFile) is True
    
    assert exec_info.value.args[0] == 'ERRO: Quantidade de atributos invalida.'


def test_ifThereIsMoreThanExpectedSonarAttributes():
    '''
        Testa se um objeto json fornecido possui mais atributos
        do que o esperado
    '''

    jsonFile = \
    {
        "paging": {
            "pageIndex": 1,
            "pageSize": 100,
            "total": 5
        },
        "baseComponent": {
            "id": "AX9FgyLHNIj_v_uQK41e",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI",
            "name": "2021-2-MeasureSoftGram-CLI",
            "qualifier": "TRK",
            "measures": [{
                    "metric": "duplicated_lines_density",
                    "value": "0.0",
                    "bestValue": True
                }
            ]
        },
        "components": [{
            "id": "AX9GDsKlZuVL7NjXSAZ4",
            "key": "fga-eps-mds_2021-2-MeasureSoftGram-CLI:tests/__init__.py",
            "name": "__init__.py",
            "qualifier": "UTS",
            "path": "tests/__init__.py",
            "language": "py",
            "measures": [{
                    "metric": "security_rating",
                    "value": "1.0",
                    "bestValue": True
                }]
        }],
        "someOtherAttribute": {
            "hello": "world",
            "value": None
        }
    }

    with pytest.raises(Exception) as exec_info:
        jsonReader.checkSonarFormat(jsonFile)
    
    assert exec_info.value.args[0] == 'ERRO: Quantidade de atributos invalida.'
