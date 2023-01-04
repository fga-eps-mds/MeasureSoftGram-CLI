import logging
import sys

logger = logging.getLogger("msgram")


def command_import(args):
    try:
        output_origin = args["output_origin"]
        dir_path = args["dir_path"]
        language_extension = args["language_extension"]
        host = args["host"]

    except Exception as e:
        logger.warning(f"KeyError: args['{e}'] - non-existent parameters")
        logger.error("Exiting with error ...")
        sys.exit(1)

    logger.debug(f"output_origin: {output_origin}")
    logger.debug(f"dir_path: {dir_path}")
    logger.debug(f"language_extension: {language_extension}")
    logger.debug(f"host: {host}")
