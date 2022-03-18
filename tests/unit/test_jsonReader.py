from measuresoftgram import jsonReader
import pytest

def test_ValidFileExtension():
    fileName = "sonar.json" 
    assert jsonReader.checkFileExtention(fileName) is True

def test_notValidFileExtension():
    fileName = "sonar.txt"
    with pytest.raises(Exception): 
        jsonReader.checkFileExtention(fileName)