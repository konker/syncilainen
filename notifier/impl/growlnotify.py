import subprocess
from shell.cmd import exec_cmd

# try to locate the growlnotify command line tool, or raise ImportError
if exec_cmd("which growlnotify") == '':
    raise ImportError()

NORMAL_LEVEL_IMPL = 0
ERROR_LEVEL_IMPL = 1

class NotifierImpl(object):
    def __init__(self, title):
        self.title = title

    def notify(self, message, level=NORMAL_LEVEL_IMPL):
        cmd = "growlnotify --message \"%s\" --priority %d --title \"%s\"" % (message, level, self.title)
        return exec_cmd(cmd)
    
