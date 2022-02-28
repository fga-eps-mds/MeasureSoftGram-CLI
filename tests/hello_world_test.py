# pytest unit hello world test
import pytest

from measuresoftgram import cli

def test_hello_world():
    # asset hello world was called
    assert cli.hello_world() == None

def test_main():
    # asset main was called
    assert cli.main() == None
    