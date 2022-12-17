from src.cli.commands.parse_get_entity.parse_get_entity import parse_get_entity

DUMMY_HOST = "http://dummy_host.com/"

entity_name = "metrics"
entity_id = "1"
organization_id = "4"
repository_id = "10"
product_id = "5"
output_format_supported = "json"
output_format_not_supported = "xml"
history = "historical-values"


class DummyResponse:
    def __init__(self, status_code, res_data):
        self.status_code = status_code
        self.res_data = res_data

    def json(self):
        return self.res_data


def test_parse_get_entity_false():

    assert parse_get_entity(
        entity_name,
        entity_id,
        DUMMY_HOST,
        organization_id,
        repository_id,
        product_id,
        output_format_not_supported,
        history,
    ) is None


'''
def test_parse_get_entity_succes(mocker):

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:

        assert parse_get_entity(
            entity_name,
            entity_id,
            DUMMY_HOST,
            organization_id,
            repository_id,
            product_id,
            output_format_supported,
            history
        )

        expected_lines = [
            "id : 1",
        ]

    for line in expected_lines:
        assert line in fake_out.getvalue()
'''
