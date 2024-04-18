from logging import getLogger
from pathlib import Path

# Set Up CLI Logging
logger = getLogger(__name__)

# TODO: I want to do roughly this so the logs are always stored at ~/scooze/logs/
# it's not working as intended right now, so the current behavior will store the log wherever the script is run
# is this the desired behavior?
log_dir = Path.home() / "scooze" / "logs"
log_dir.mkdir(parents=True, exist_ok=True)
log_path = log_dir / "scooze.log.jsonl"

for handler in logger.handlers:
    if handler.name == "file":
        print(f"update {handler.name} to use {log_path}")
        handler.baseFilename = log_path
