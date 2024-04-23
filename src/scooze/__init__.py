import json
import logging
import logging.config
import os
import sys
from pathlib import Path

# region Environment Variables

DEBUG = os.getenv("SCOOZE_DEBUG", "False") == "True"

# endregion


# region Set Up Logging

logger = logging.getLogger(__name__)

config_file = Path("configs/logging_config.json")
with open(config_file) as f_in:
    logging_config = json.load(f_in)
logging.config.dictConfig(config=logging_config)
# TODO(py3.12): Python 3.12 supports QueueHandler for non-blocking logging

# NOTE: Allow DEBUG logging if the flag is set
if DEBUG:
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    logger.debug("scooze DEBUG flag enabled!")
    # logger.info("DEBUG ENABLED: scooze logger info message")
    # logger.warning("DEBUG ENABLED: scooze logger warning message")
    # logger.exception("DEBUG ENABLED: scooze logger exception message")
    # logger.critical("DEBUG ENABLED: scooze logger critical message")

# endregion
