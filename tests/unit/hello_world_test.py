# pytest unit hello world test
import pytest
from measuresoftgram import cli


@pytest.mark.skip(reason="tests wont't be empty")
def test_hello_world():
    # asset hello world was called
    assert cli.hello_world() is None
