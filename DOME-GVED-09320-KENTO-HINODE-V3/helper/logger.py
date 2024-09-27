import logging

def setup_logger(log_file="error.log", level=logging.ERROR):
    """Sets up a logger with the specified configuration."""
    logging.basicConfig(filename=log_file, level=level,
                        format='%(asctime)s - %(levelname)s - %(message)s')