import subprocess
from shell.cmd import exec_cmd

# try to locate the notify-send command line tool, or raise ImportError
if exec_cmd("which notify-send") == '':
    raise ImportError()


class NotifierImpl(object):
    def __init__(self, title):
        self.title = title

    def notify(self, message):
        cmd = "notify-send %s %s" % (self.title, message)
        return cmd.exec_cmd(cmd)
    

