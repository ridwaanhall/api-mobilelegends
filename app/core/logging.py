"""
Logging Configuration Module

This module sets up structured logging for the application.
"""

import logging
import sys
from typing import Any

from app.core.config import settings


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output."""
    
    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    
    FORMATS = {
        logging.DEBUG: grey + "%(levelname)s" + reset + " - %(message)s",
        logging.INFO: blue + "%(levelname)s" + reset + " - %(message)s",
        logging.WARNING: yellow + "%(levelname)s" + reset + " - %(message)s",
        logging.ERROR: red + "%(levelname)s" + reset + " - %(message)s",
        logging.CRITICAL: bold_red + "%(levelname)s" + reset + " - %(message)s"
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


def setup_logging() -> None:
    """
    Configure application logging.
    
    Sets up console handler with colored output and appropriate log level.
    """
    # Create logger
    logger = logging.getLogger("app")
    logger.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, settings.LOG_LEVEL))
    
    # Use colored formatter in development
    if settings.is_development:
        console_handler.setFormatter(ColoredFormatter())
    else:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (usually __name__)
        
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(f"app.{name}")
