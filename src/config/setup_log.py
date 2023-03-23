import sys
import logging
from datetime import datetime
from rich.logging import RichHandler


LOG_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}

LOG_FORMATS = {
    "RICH": "%(module)-12s: [line: %(lineno)-3s] %(message)s",
    "DEBUG": "%(levelname)-8s %(module)-12s %(funcName) -15s : %(lineno)-3s %(message)s",
    "INFO": "%(levelname)-8s: %(message)s",
    "WARNING": "%(levelname)-8s: %(module)-8s:%(lineno)-3s %(message)s",
    "ERROR": "%(asctime)s: %(levelname)-8s: %(funcName)s :%(lineno)d %(message)s",
    "CRITICAL": "%(asctime)-15s %(levelname)-8s %(filename)-15s %(module)-8s:%(lineno)-3s %(message)s",
}

# =================================================================================================

now = datetime.now()
date = now.strftime("%y%m%d")
datefmt = "%d %b %Y - %H:%M:%S"  # 30 Dec 2022 11:41:57
file_name = "src/logs/debug.log"


def config_logger(log_mod):
    if log_mod == "quiet":
        basic_config("INFO", "WARNING", "w")
    elif log_mod == "verbose":
        basic_config("DEBUG", "DEBUG", "w")
    else:
        basic_config("WARNING", "ERROR", "w")

# =================================================================================================


def basic_config(console_level_name, file_level_name, file_mode):

    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = logging.Formatter(LOG_FORMATS[console_level_name], datefmt)
    console_handler.setFormatter(console_formatter)
    # console_handler.setLevel(LOG_LEVELS[console_level_name])

    # file_handler = logging.FileHandler(file_name, file_mode)
    # file_formatter = logging.Formatter(LOG_FORMATS[file_level_name])
    # file_handler.setFormatter(file_formatter)
    # file_handler.setLevel(LOG_LEVELS[file_level_name])

    rich_handler = RichHandler(level=logging.DEBUG, rich_tracebacks=True)
    rich_handler.setFormatter(logging.Formatter(LOG_FORMATS["RICH"], datefmt))

    logger = logging.getLogger("msgram")
    logger.addHandler(console_handler)
    # logger.addHandler(rich_handler)
    # logger.addHandler(file_handler)
    logger.setLevel(LOG_LEVELS[console_level_name])

    logger_console = logging.getLogger("console")
    logger_console.addHandler(console_handler)
    logger_console.setLevel(LOG_LEVELS[console_level_name])

    logger_file = logging.getLogger("file")
    # logger_file.addHandler(file_handler)
    logger_file.addHandler(console_handler)
    logger_file.setLevel(LOG_LEVELS[file_level_name])


# =================================================================================================
# logging testing

# logger.log(logging.DEBUG, "This is an debug message.")
# logger.log(logging.INFO, "This is an info message.")
# logger.log(logging.ERROR, "This is an error message.")
# logger.log(logging.WARNING, "This is an warning message.")
# logger.log(logging.CRITICAL, "This is an critical message.")
# logger.error("[bold red blink]This is an error custom message[/]", extra={"markup": True})


# =================================================================================================
