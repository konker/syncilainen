import logging

NORMAL_LEVEL_IMPL = 0
ERROR_LEVEL_IMPL = 1

class NotifierImpl(object):
    def __init__(self, title, disable_after_n_errors=-1):
        self.title = title
        logging.info("Using Notifier: dummy")

    def notify(self, message, level=NORMAL_LEVEL_IMPL):
        pass
