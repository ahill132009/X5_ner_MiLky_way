import logging
import sys

def setup_logger(log_file: str = "app.log") -> logging.Logger:
    # Create logger
    logger = logging.getLogger("logger_parser")
    logger.setLevel(logging.DEBUG)  # capture everything DEBUG+

    # Formatter for log messages
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)  # console shows INFO+
    console_handler.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)  # file stores DEBUG+
    file_handler.setFormatter(formatter)

    # Avoid duplicate handlers if function is called multiple times
    if not logger.handlers:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger