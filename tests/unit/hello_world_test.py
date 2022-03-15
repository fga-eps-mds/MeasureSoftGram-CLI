# pytest unit hello world test
from measuresoftgram import cli


def test_hello_world():
    # asset hello world was called
    assert cli.hello_world() is None

