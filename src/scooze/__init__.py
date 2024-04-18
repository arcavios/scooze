import json
import logging
import logging.config
import os
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# TODO: fix logging path here - doesn't work in container
# config_file = Path("configs/logging_config.json")
# with open(config_file) as f_in:
#     logging_config = json.load(f_in)
# logging.config.dictConfig(config=logging_config)
# TODO(py3.12): Python 3.12 supports QueueHandler for non-blocking logging

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

MONGO_HOST = os.getenv("MONGO_HOST", "127.0.0.1")
