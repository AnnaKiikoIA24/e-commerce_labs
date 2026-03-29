import logging
import json_log_formatter

def setup_logging():
    formatter = json_log_formatter.JSONFormatter()

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

    logger.info("Logging setup complete")