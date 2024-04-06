import json
import logging.config
import pathlib
from logging import getLogger

logger = getLogger(__name__)
print("MY LOGGER NAME IS:")
print(logger.name)

config_file = pathlib.Path("configs/logging_config.json")
with open(config_file) as f_in:
    logging_config = json.load(f_in)
logging.config.dictConfig(config=logging_config)

# TODO: add handler to the root logger if debug flag is active
if DEBUG := True:
    root = getLogger()

        # "": {
        #     "level": "DEBUG",
        #     "handlers": ["debug"]
        # },
        # "debug": {
        #     "class": "logging.StreamHandler",
        #     "level": "DEBUG",
        #     "formatter": "simple",
        #     "stream": "ext://sys.stdout"
        # },
