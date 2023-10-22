import unittest
from unittest.mock import patch
from io import StringIO
import sys
import json

from src.cli.commands.cmd_print_config import print_json_tree
from src.cli.utils import  print_info,  print_rule

    
def test_print_json_tree():

    file = open("tests/unit/data/msgram.json")
    data = json.load(file)

    captured_output = StringIO()
    sys.stdout = captured_output

    characteristics = data.get("characteristics", [])

    result = print_json_tree(characteristics[0])

    fileExpected = open("tests/unit/data/expected_list.txt")

    compare = fileExpected.read()

    assert result == compare