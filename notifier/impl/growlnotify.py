import subprocess
from shell.cmd import exec_cmd

# try to locate the growlnotify command line tool, or raise ImportError
if exec_cmd("which growlnotify") == '':
    raise ImportError()


class NotifierImpl(object):
    def __init__(self, title):
        self.title = title

    def notify(self, message):
        cmd = "growlnotify --message \"%s\" --title \"%s\"" % (message, self.title)
        return exec_cmd(cmd)
    
