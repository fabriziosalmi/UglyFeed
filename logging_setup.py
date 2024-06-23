# logging_setup.py

import logging
import logging.config

# Define a logging configuration using a dictionary.
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
    },
    'handlers': {
        'console_info': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout',
        },
        'console_error': {
            'class': 'logging.StreamHandler',
            'level': 'WARNING',
            'formatter': 'standard',
            'stream': 'ext://sys.stderr',
        },
        # Optional: Add a file handler if you want to log to a file
        'file': {
            'class': 'logging.FileHandler',
            'level': 'DEBUG',
            'formatter': 'standard',
            'filename': 'app.log',
            'mode': 'a',
        },
    },
    'loggers': {
        '__main__': {
            'handlers': ['console_info', 'console_error'],  # Add 'file' if you want file logging
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console_info', 'console_error'],  # Add 'file' if you want file logging
        'level': 'DEBUG',
    },
}

def setup_logging() -> logging.Logger:
    try:
        logging.config.dictConfig(LOGGING_CONFIG)

        # Create the logger
        logger = logging.getLogger(__name__)

        # Log a diagnostics message to confirm successful setup
        logger.debug("Logging setup complete and operational.")

        return logger

    except Exception as e:
        print(f"Failed to configure logging: {e}")
        raise

def get_logger(name: str) -> logging.Logger:
    """Get a logger with the specified name."""
    return logging.getLogger(name)

# Usage example:
if __name__ == "__main__":
    logger = setup_logging()
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Additional logger for a different module or context
    another_logger = get_logger('another_module')
    another_logger.info("Logging from another module")
