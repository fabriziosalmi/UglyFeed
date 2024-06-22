import logging
import logging.config
import queue
from typing import Union

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
        'queue': {
            'class': 'logging.handlers.QueueHandler',
            'queue': 'ext://logging.handlers.QueueHandler',
            'formatter': 'standard',
        },
    },
    'loggers': {
        '__main__': {
            'handlers': ['queue'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['queue'],
        'level': 'DEBUG',
    },
    'filters': {
        'warning_filter': {
            '()': 'logging.Filter',
            'name': 'warning_filter',
        },
    },
}


def setup_logging() -> logging.Logger:
    try:
        logging.config.dictConfig(LOGGING_CONFIG)

        # Create the logger
        logger = logging.getLogger(__name__)

        # Queue handler to manage asynchronous logging
        log_queue = queue.Queue(-1)
        queue_handler = logging.handlers.QueueHandler(log_queue)
        queue_listener = logging.handlers.QueueListener(log_queue, *logger.handlers)
        queue_listener.start()

        logger.addHandler(queue_handler)

        # Adding console handlers explicitly
        console_info_handler = logging.StreamHandler()
        console_info_handler.setLevel(logging.INFO)
        console_info_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        console_error_handler = logging.StreamHandler()
        console_error_handler.setLevel(logging.WARNING)
        console_error_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

        logger.addHandler(console_info_handler)
        logger.addHandler(console_error_handler)

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
