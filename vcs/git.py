import os.path
import time
import subprocess
from shell.cmd import exec_cmd

class VCS(object):
    def __init__(self, repo_directory):
        self.repo_directory = repo_directory
        self.ignore_path = os.path.join(repo_directory, '.git')

    def status(self):
        cmd = "git status --porcelain -uall"
        out,error = exec_cmd(cmd, self.repo_directory)
        return self._parse_status(out, error)

    def add(self, filename='.'):
        cmd = "git add %s" % filename
        return exec_cmd(cmd, self.repo_directory)

    def commit(self, message):
        cmd = "git commit -m \"%s\"" % message
        return exec_cmd(cmd, self.repo_directory)

    def pull(self, remote='origin', branch='master'):
        cmd = "git pull %s %s" % (remote, branch)
        return exec_cmd(cmd, self.repo_directory)

    def push(self, remote='origin', branch='master'):
        cmd = "git push %s %s" % (remote, branch)
        return exec_cmd(cmd, self.repo_directory)

    def commit_and_push(self, message):
        self.add()
        self.commit(message)
        self.push()
        pass

    def _parse_status(self, out, error):
        ret = []
        for f in out.split("\n"):
            if not f == '':
                ret.append(tuple(f.split()))
        return ret

