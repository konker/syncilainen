import subprocess
from shell.cmd import exec_cmd

# try to locate the notify-send command line tool, or raise ImportError
if exec_cmd("which notify-send") == '':
    raise ImportError()

NORMAL_LEVEL_IMPL = 0
ERROR_LEVEL_IMPL = 1

class NotifierImpl(object):
    def __init__(self, title, disable_after_n_errors=-1):
        self.title = title
        self.disable_after_n_errors = disable_after_n_errors
        self._consecutive_errors = 0

    def notify(self, message, level=NORMAL_LEVEL_IMPL):
        if level == ERROR_LEVEL_IMPL:
            self._consecutive_errors = self._consecutive_errors + 1
        else:
            self._consecutive_errors = 0

        if self.disable_after_n_errors > 0:
            if self._consecutive_errors < self.disable_after_n_errors:
                cmd = "notify-send %s %s" % (self.title, message)
                cmd.exec_cmd(cmd)
    

