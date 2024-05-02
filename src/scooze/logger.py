import json
import logging
import logging.config
import sys

from scooze.config import CONFIG

# region Set Up Logging

logger = logging.getLogger(__name__)

config_file = CONFIG.package_root / "configs" / "logging_config.json"
with config_file.open() as f_in:
    logging_config = json.load(f_in)
logging.config.dictConfig(config=logging_config)

# TODO(py3.12): Python 3.12 supports QueueHandler for non-blocking logging

# NOTE: Allow DEBUG logging if the flag is set
if CONFIG.debug:
    logger.setLevel(logging.DEBUG)
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)

    logger.debug("scooze SCOOZE_DEBUG flag enabled!")
    # logger.info("SCOOZE_DEBUG ENABLED: scooze logger info message")
    # logger.warning("SCOOZE_DEBUG ENABLED: scooze logger warning message")
    # logger.exception("SCOOZE_DEBUG ENABLED: scooze logger exception message")
    # logger.critical("SCOOZE_DEBUG ENABLED: scooze logger critical message")

# endregion
