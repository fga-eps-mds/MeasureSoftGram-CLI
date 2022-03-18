from measuresoftgram import jsonReader
import pytest
import json


def test_ValidFileExtension():
    fileName = "sonar.json" 
    assert jsonReader.checkFileExtension(fileName) is True


def test_notValidFileExtension():
    fileName = "sonar.txt"
    with pytest.raises(Exception): 
        jsonReader.checkFileExtension(fileName)


def test_validSonarFormat():
    absoluteFilePath = r"C:\Users\pallo\Downloads\Bia\MDS\2021-2-MeasureSoftGram-CLI\tests\utils\sonar.json"
    f = open(absoluteFilePath, "r")
    jsonFile = json.load(f)
    assert jsonReader.checkSonarFormat(jsonFile) is True


def test_notValidSonarFormat():
    jsonFile = json.dumps(
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
    )
    assert len(jsonFile) == 2