import logging
from src.config.setup_log import config_logger, basic_config


def test_logging_config_verbose(caplog):
    caplog.set_level(logging.DEBUG)

    config_logger("verbose")

    logger = logging.getLogger("msgram")
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

    assert "This is a debug message." in caplog.text
    assert "This is an info message." in caplog.text
    assert "This is a warning message." in caplog.text
    assert "This is an error message." in caplog.text


def test_basic_config(caplog):
    caplog.set_level(logging.INFO)

    basic_config("INFO", "ERROR", "w")

    logger = logging.getLogger("msgram")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")

    assert "This is an info message." in caplog.text
    assert "This is a warning message." in caplog.text
    assert "This is an error message." in caplog.text
