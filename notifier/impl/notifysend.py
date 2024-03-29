# -*- coding: utf-8 -*-
#
# watcher.impl.notifysend
# 
# notify-send implementation of the Notifier interface (Linux)
#
# Authors: Konrad Markus <konker@gmail.com>
#

import logging
import subprocess
from shell.cmd import exec_cmd, exec_cmd_out

# try to locate the notify-send command line tool, or raise ImportError
NOTIFY_SEND = exec_cmd_out("which notify-send").strip() 
if NOTIFY_SEND == '':
    raise ImportError()

NORMAL_LEVEL_IMPL = 0
ERROR_LEVEL_IMPL = 1

class NotifierImpl(object):
    def __init__(self, title, disable_after_n_errors=-1):
        self.title = title
        self.disable_after_n_errors = disable_after_n_errors
        self._consecutive_errors = 0
        logging.info("Using Notifier: %s" % NOTIFY_SEND)

    def notify(self, message, level=NORMAL_LEVEL_IMPL):
        if message == "":
            return

        if level == ERROR_LEVEL_IMPL:
            self._consecutive_errors = self._consecutive_errors + 1
        else:
            self._consecutive_errors = 0

        if self.disable_after_n_errors > 0:
            if self._consecutive_errors < self.disable_after_n_errors:
                cmd = "%s \"%s\" \"%s\"" % (NOTIFY_SEND, self.title, message)
                exec_cmd(cmd)
    

