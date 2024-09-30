import logging
import os

# Create a logger
logger = logging.getLogger('pyLogixLogger')
logger.setLevel(logging.DEBUG)  # Set the default logging level

# Set the log file path explicitly
log_file = os.path.join(os.getcwd(), 'pylogix.log')  # This will create the log file in the current working directory

# Alternatively, you can specify a directory in your package:
# log_file = os.path.join(os.path.dirname(__file__), 'logs', 'pylogix.log')
# os.makedirs(os.path.dirname(log_file), exist_ok=True)  # Create the logs directory if it doesn't exist

# Create a file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)  # Set the logging level for the file

# Create a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)  # Set the logging level for the console

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Set the formatter for the handlers
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

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
        file_handler.setLevel(levels[level])  # Set file handler log level
        console_handler.setLevel(levels[level])  # Set console handler log level
        logger.info(f"Log level set to {level}")
    else:
        logger.error(f"Invalid log level: {level}. Choose from {', '.join(levels.keys())}.")
