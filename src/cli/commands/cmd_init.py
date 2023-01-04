import logging
import sys
import os
import json

from staticfiles import DEFAULT_PRE_CONFIG

logger = logging.getLogger("msgram")


def command_init(args):
    try:
        dir_path = args["dir_path"]

    except Exception as e:
        logger.error(f"KeyError: args['{e}'] - non-existent parameters")
        sys.exit(1)

    logger.info(dir_path)

    if os.path.isdir(dir_path):
        logger.error(f"DirExistsError: directory \"{dir_path}\" already exists")
        sys.exit(1)

    os.mkdir(dir_path)
    with open(f"{dir_path}/msgram.json", "w") as f:
        f.write(json.dumps(DEFAULT_PRE_CONFIG, indent=4))

    logger.info(f"The file {dir_path}/msgram.json was created successfully.")
