import os
import sys
import logging
    
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

logging_str = "[%(asctime)s: %(levelname)s: %(module)s: %(message)s]"

log_filepath = os.path.join(LOGS_DIR, "running_logs.log")

logging.basicConfig(
    level=logging.INFO,
    format=logging_str,
    handlers=[
        logging.FileHandler(log_filepath, encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger("AI-Trainer")
