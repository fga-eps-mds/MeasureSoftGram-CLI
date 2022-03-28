from src.cli.cliRunner import main
from io import StringIO


class DummyResponse:
    def json(self):
        return {
            "characteristics": {
                "usability": {
                    "name": "Usability",
                },
                "performance": {
                    "name": "Performance",
                },
            }
        }


def test_handle_sigint_in_create_form(mocker):
    """
    Test for KeyboardInterrupt exception handling
    """
    mocker.patch("requests.get", return_value=DummyResponse())
    mocker.patch("inquirer.prompt", side_effect=KeyboardInterrupt())
    mocker.patch("sys.argv", ["measuresoftgram", "create"])

    with mocker.patch("sys.stdout", new=StringIO()) as fake_out:

        main()

        assert "\nYou pressed Ctrl + C! No pre conf created." in fake_out.getvalue()
