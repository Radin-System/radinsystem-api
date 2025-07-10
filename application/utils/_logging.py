import logging

def init_logging(log_file: str, log_level: str) -> None:
    # Create handlers
    logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(log_file)

    # Set Log Levels
    _level = getattr(logging, log_level.upper(), logging.INFO)
    logger.setLevel(_level)
    console_handler.setLevel(_level)    
    file_handler.setLevel(_level)

    # Set Formaters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)