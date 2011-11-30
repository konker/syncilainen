import logging

NORMAL_LEVEL_IMPL = 0
ERROR_LEVEL_IMPL = 1

class NotifierImpl(object):
    def __init__(self, title):
        self.title = title
        logging.info("Using dummy notifications")

    def notify(self, message, level=NORMAL_LEVEL_IMPL):
        pass
