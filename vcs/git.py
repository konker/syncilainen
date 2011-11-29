import time
import subprocess

class VCS(object):
    def __init__(self, repo_directory):
        self.repo_directory = repo_directory

    def status(self):
        cmd = "git status --porcelain -uall"
        return self._parse_status(self._exec_cmd_(cmd))

    def add(self, filename):
        cmd = "git add %s" % filename
        return self._exec_cmd_(cmd)

    def commit(self, message):
        cmd = "git commit -m \"%s\"" % message
        return self._exec_cmd_(cmd)

    def pull(self, remote, branch):
        cmd = "git pull %s %s" % (remote, branch)
        return self._exec_cmd_(cmd)

    def push(self, remote, branch):
        cmd = "git push %s %s" % (remote, branch)
        return self._exec_cmd_(cmd)

    def _exec_cmd_(self, cmd):
        pipe = subprocess.Popen(cmd, shell=True, cwd=self.repo_directory, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (out, error) = pipe.communicate()
        pipe.wait()
        return out

    def _parse_status(self, s):
        ret = []
        for f in s.split("\n"):
            if not f == '':
                ret.append(tuple(f.split()))
        return ret
