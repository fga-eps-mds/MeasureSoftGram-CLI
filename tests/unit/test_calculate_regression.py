import pytest

from src.cli.commands.cmd_calculate import show_results

def test_show_results_empty_data_calculated_tabular_format():
    with pytest.raises(IndexError):
        show_results(output_format="tabular", data_calculated=[], config_path="dummy_path")

def test_show_results_empty_data_calculated_raw_format():
    with pytest.raises(IndexError):
        show_results(output_format="raw", data_calculated=[], config_path="dummy_path")

def test_show_results_empty_data_calculated_tree_format():
    with pytest.raises(IndexError):
        show_results(output_format="tree", data_calculated=[], config_path="dummy_path")
