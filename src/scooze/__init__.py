import json
import logging
import pathlib
import sys

logger = logging.getLogger(__name__)

config_file = pathlib.Path("configs/logging_config.json")
with open(config_file) as f_in:
    logging_config = json.load(f_in)
logging.config.dictConfig(config=logging_config)
# TODO: Python 3.12 and higher supports QueueHandler for non-blocking logging

# NOTE: Use this flag to test scooze library logging. Default to False.
if DEBUG := False:
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    logger.debug("DEBUG ENABLED: scooze logger debug message")
    logger.info("DEBUG ENABLED: scooze logger info message")
    logger.warning("DEBUG ENABLED: scooze logger warning message")
    logger.exception("DEBUG ENABLED: scooze logger exception message")
    logger.critical("DEBUG ENABLED: scooze logger critical message")
