import logging
from .logger import logger
import time 

def set_log_level(level):
    """
    Set the logging level for the logger.

    :param level: Logging level as a string. Options: 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'.
    """
    levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    if level in levels:
        logger.setLevel(levels[level])
        logger.info(f"Log level set to {level}")
    else:
        logger.error(f"Invalid log level: {level}. Choose from {', '.join(levels.keys())}.")

def track_time(func):
    """
    A decorator to track the execution time of a function.

    :param func: The function to be decorated.
    :return: The wrapped function with time tracking.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()  # Start time
        result = func(*args, **kwargs)  # Execute the function
        end_time = time.time()  # End time
        execution_time = end_time - start_time  # Calculate duration
        logger.info(f"Execution time for {func.__name__}: {execution_time:.4f} seconds")
        return result  # Return the result of the function
    return wrapper
