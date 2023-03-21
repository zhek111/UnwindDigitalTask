import logging


def setup_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.ERROR)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger