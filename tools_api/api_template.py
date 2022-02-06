from abc import ABC
import logging

LOGGER_NAME = "autobug-logger"
logger = logging.getLogger(LOGGER_NAME)

class API(ABC):
    pass