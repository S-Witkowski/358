import logging

def create_logger():
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename="my_log.log", filemode='w', level=logging.INFO)
    return logger

logger = logging.getLogger(__name__)