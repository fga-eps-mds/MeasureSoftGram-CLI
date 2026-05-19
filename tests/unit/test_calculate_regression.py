from unittest.mock import patch

from src.cli.commands.cmd_calculate import show_results

@patch("src.cli.commands.cmd_calculate.print_warn")
def test_show_results_empty_data_calculated_tabular_format(mock_print_warn):
    show_results(output_format="tabular", data_calculated=[], config_path="dummy_path")
    mock_print_warn.assert_called_once_with("WARNING: No extracted file read so no tabular was generated!")

@patch("src.cli.commands.cmd_calculate.print_warn")
def test_show_results_empty_data_calculated_raw_format(mock_print_warn):
    show_results(output_format="raw", data_calculated=[], config_path="dummy_path")
    mock_print_warn.assert_called_once_with("WARNING: No extracted file read so no raw was generated!")

@patch("src.cli.commands.cmd_calculate.print_warn")
def test_show_results_empty_data_calculated_tree_format(mock_print_warn):
    show_results(output_format="tree", data_calculated=[], config_path="dummy_path")
    mock_print_warn.assert_called_once_with("WARNING: No extracted file read so no tree was generated!")
