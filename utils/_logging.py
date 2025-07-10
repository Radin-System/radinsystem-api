import logging

def initiate_logging(logging_config) -> None:
    # Create handlers
    logger = logging.getLogger()
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(logging_config['log_file'])

    # Set Log Levels
    log_level = getattr(logging, logging_config['log_level'], logging.INFO)
    logger.setLevel(log_level)
    console_handler.setLevel(log_level)    
    file_handler.setLevel(log_level)

    # Set Formaters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add the handlers to the logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)