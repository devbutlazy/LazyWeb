import sys
from loguru import logger


def logging_setup():
    format_info = "<blue>{time:HH:mm:ss.SS}</blue> | <green>{message}</green>"
    logger.remove()

    logger.add(sys.stdout, colorize=True, format=format_info, level="INFO")


logging_setup()
