import logging

from ..common.settings import settings

_LEVEL_MAP = {
    'CRITICAL': 50,
    'FATAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'WARN': 30,
    'INFO': 20,
    'DEBUG': 10,
    'NOTSET': 0,
}


def get_logger(name: str) -> logging.Logger:
    """
    Gets common logger with specified parameters.
    :param name: Logger name.
    :return: Logger instance.
    """
    logger = logging.getLogger(name)

    level = _LEVEL_MAP.get(settings['logging']['level'].upper(), 0)
    logger.setLevel(level)

    ch = logging.StreamHandler()
    ch.setLevel(level)
    fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)8s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    return logger
