import pytest
import os
import pandas as pd

# from src.cli.commands.parse_generate.parse_generate import parse_generate
from src.cli.commands.parse_generate.generate_utils import GenerateUtils

VALID_CONFIG = '{"organization":{"name": "fga-eps-mds","id": 1},"product":{"name":"MeasureSoftGram","id":3}' + \
               ',"repositories":[{"2022-1-MeasureSoftGram-CLI":1},{"2022-1-MeasureSoftGram-Core":2},{"2022-' + \
               '1-MeasureSoftGram-Service":3},{"2022-1-MeasureSoftGram-Front":4}]}'
VALID_HOST = "https://measuresoftgram-service.herokuapp.com/"


def setup():
    f = open(".measuresoftgram", "w")
    f.write(VALID_CONFIG)
    f.close()


def teardown():
    try:
        os.remove(".measuresoftgram")
    except Exception:
        pass


@pytest.mark.parametrize(
    "format, value",
    [
        ("csv", True),
        ("json", False),
        ("xml", False),
        ("txt", False),
        ("CSV", True)
    ]
)
def test_available_formats(format, value):
    assert GenerateUtils.verify_available_format(format) == value


# @pytest.mark.parametrize(
#     "format, expect",
#     [
#         ("csv", 0),
#         ("json", 1)
#     ]
# )
# def test_fail_format_parse_generate(format, expect):
#     setup()
#     assert parse_generate(format, VALID_HOST) == expect
#     teardown()


# def test_host_communication():
#     setup()
#     assert parse_generate("csv", "dummy_host") == 1
#     assert parse_generate("csv", VALID_HOST) == 0
#     teardown()


# def test_no_config_file():
#     assert parse_generate("csv", VALID_HOST) == 1
#     f = open(".measuresoftgram", "w")
#     f.close()
#     assert parse_generate("csv", VALID_HOST) == 1
#     try:
#         os.remove(".measuresoftgram")
#     except Exception:
#         pass
# def test_output_file():
#     setup()
#     product_name = "MeasureSoftGram"
#     repositories = ["2022-1-MeasureSoftGram-CLI",
#                     "2022-1-MeasureSoftGram-Core",
#                     "2022-1-MeasureSoftGram-Service",
#                     "2022-1-MeasureSoftGram-Front"]
#     columns = [
#         'datetime',
#         'repository',
#         'em1',
#         'em2',
#         'em3',
#         'em4',
#         'em5',
#         'em6',
#         'em7',
#         'modifiability',
#         'functional_completeness',
#         'testing_status',
#         'maintainability',
#         'reliability',
#         'functional_suitability',
#         'sqc',
#     ]
#     assert parse_generate("csv", VALID_HOST) == 0
#     output = pd.read_csv(f"{product_name}.csv")
#     assert output.columns.tolist() == columns
#     assert output.iloc[random.randrange(output.shape[0])]['repository'] in repositories
#     teardown()


def test_create_dataframe():
    df = GenerateUtils.create_df()
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 0


def test_min_values():
    entity = {
        "results": [
            {"history": {"1": 1, "2": 2, "3": 3, "4": 4, }},
            {"history": {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, }},
            {"history": {"1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, }},
        ]
    }
    assert GenerateUtils.min_history_count(entity) == 4
    assert GenerateUtils.min_history_count(entity) != 5
    assert GenerateUtils.min_history_count(entity) != 6
