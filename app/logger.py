import logging
import sys
from config import settings


def get_logger(name: str = "app"):
    logger = logging.getLogger(name)
    logger.info(f"Starting with {settings}")

    if logger.handlers:  # already configured
        return logger

    # Set log level from settings or default
    level = getattr(logging, settings.log_level.upper(), logging.INFO)
    logger.setLevel(level)

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)

    # Log format
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Attach handler
    logger.addHandler(console_handler)

    return logger


# Global default logger
logger = get_logger("fastapi_app")
