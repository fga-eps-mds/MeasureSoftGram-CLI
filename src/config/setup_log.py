import sys
import logging

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

datefmt = "%d %b %Y - %H:%M:%S"  # 30 Dec 2022 11:41:57


def config_logger(log_mod):
    if log_mod == "quiet":
        basic_config("INFO")
    elif log_mod == "verbose":
        basic_config("DEBUG")
    else:
        basic_config("WARNING")


# =================================================================================================


class CLIConsoleHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            message = self.format(record)
            from src.cli.utils import print_error, print_info, print_warn

            if record.levelno >= logging.ERROR:
                print_error(message)
            elif record.levelno >= logging.WARNING:
                print_warn(message)
            else:
                print_info(message)
            self.flush()
        except Exception:
            self.handleError(record)


def basic_config(console_level_name):
    console_handler = CLIConsoleHandler(sys.stdout)
    console_formatter = logging.Formatter(LOG_FORMATS[console_level_name], datefmt)
    console_handler.setFormatter(console_formatter)

    logger = logging.getLogger("msgram")
    logger.addHandler(console_handler)
    logger.setLevel(LOG_LEVELS[console_level_name])

    logger_console = logging.getLogger("console")
    logger_console.addHandler(console_handler)
    logger_console.setLevel(LOG_LEVELS[console_level_name])


# =================================================================================================
