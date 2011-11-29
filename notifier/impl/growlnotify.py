import subprocess

# try to locate the growlnotify command line tool, or raise ImportError

def _exec_cmd(cmd):
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pipe.communicate()
    pipe.wait()
    return out

if _exec_cmd("which growlnotify") == '':
    raise ImportError()

class NotifierImpl(object):
    def __init__(self, title):
        self.title = title

    def notify(self, message):
        cmd = "growlnotify --message \"%s\" --title \"%s\"" % (message, self.title)
        print(cmd)
        return _exec_cmd(cmd)
    
