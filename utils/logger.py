"""
logger.py
---------
Centralized logging configuration for the SkillMantra automation framework.
All modules should import `get_logger` and call it with their __name__.
"""

import logging
import os
from datetime import datetime

LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reports", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def _build_root_logger() -> logging.Logger:
    """Configure and return the root logger for the framework."""
    log_filename = os.path.join(
        LOG_DIR,
        f"test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    )

    root = logging.getLogger("skillmantra")
    root.setLevel(logging.DEBUG)

    if not root.handlers:
        # Console handler — INFO and above
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))

        # File handler — DEBUG and above
        file_handler = logging.FileHandler(log_filename, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT))

        root.addHandler(console_handler)
        root.addHandler(file_handler)

    return root


# Build root logger once at import time
_root_logger = _build_root_logger()


def get_logger(name: str) -> logging.Logger:
    """
    Return a child logger under the 'skillmantra' namespace.

    Usage:
        from utils.logger import get_logger
        logger = get_logger(__name__)
    """
    return logging.getLogger(f"skillmantra.{name}")
