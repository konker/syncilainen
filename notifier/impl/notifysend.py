import subprocess

# try to locate the notify-send command line tool, or raise ImportError

def _exec_cmd(cmd):
    pipe = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (out, error) = pipe.communicate()
    pipe.wait()
    return out

if _exec_cmd("which notify-send") == '':
    raise ImportError()

class NotifierImpl(object):
    def __init__(self, title):
        self.title = title

    def notify(self, message):
        cmd = "notify-send %s %s" % (self.title, message)
        print(cmd)
        return _exec_cmd(cmd)
    

