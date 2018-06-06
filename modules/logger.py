import logging


class Logger:

    def __init__(self):
        pass

    def __del__(self):
        pass

    @staticmethod
    def load_logger(file):
        # Create Logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)
        # Create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        # Create file handler and set level to debug
        fh = logging.FileHandler(file, mode='a', encoding=None, delay=False)
        fh.setLevel(logging.DEBUG)
        # Create formatter
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        # Add formatter to handlers
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        # Add handlers to logger
        logger.addHandler(ch)
        logger.addHandler(fh)

        return logger
