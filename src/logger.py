"""
===========================================================
Project : NaukriBot
Module  : logger.py
Author  : Gulshan Singh
Version : 1.0.0
===========================================================
"""

import logging
from pathlib import Path

from config.config import APP_LOG, ERROR_LOG, LOG_DIR

# ----------------------------------------------------------
# Create Log Folder
# ----------------------------------------------------------

LOG_DIR.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------
# Logger
# ----------------------------------------------------------

logger = logging.getLogger("NaukriBot")

logger.setLevel(logging.INFO)

# Prevent duplicate logs
logger.handlers.clear()

# ----------------------------------------------------------
# Log Format
# ----------------------------------------------------------

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)-8s | %(message)s",
    "%Y-%m-%d %H:%M:%S"
)

# ----------------------------------------------------------
# Application Log
# ----------------------------------------------------------

app_handler = logging.FileHandler(APP_LOG, encoding="utf-8")

app_handler.setLevel(logging.INFO)

app_handler.setFormatter(formatter)

# ----------------------------------------------------------
# Error Log
# ----------------------------------------------------------

error_handler = logging.FileHandler(ERROR_LOG, encoding="utf-8")

error_handler.setLevel(logging.ERROR)

error_handler.setFormatter(formatter)

# ----------------------------------------------------------
# Console Log
# ----------------------------------------------------------

console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)

console_handler.setFormatter(formatter)

# ----------------------------------------------------------
# Add Handlers
# ----------------------------------------------------------

logger.addHandler(app_handler)

logger.addHandler(error_handler)

logger.addHandler(console_handler)

# ----------------------------------------------------------
# Export Logger
# ----------------------------------------------------------

__all__ = ["logger"]