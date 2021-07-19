import logging


def logging_setting():
    formatter = '%(levelname)s %(funcName)s %(message)s'
    logging.basicConfig(level=logging.INFO, format=formatter)
