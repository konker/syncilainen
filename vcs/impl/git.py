# -*- coding: utf-8 -*-
#
# vcs.impl.git
#
# Wrapper around the git command
#
# Authors: Konrad Markus <konker@gmail.com>
#

import logging
import os.path
import time
import subprocess
from shell.cmd import exec_cmd, exec_cmd_out

OK = True
NOT_OK = False

# try to locate the git command line tool, or raise ImportError
GIT = exec_cmd_out("which git").strip()
if GIT == '':
    raise ImportError()


class VCSImpl(object):
    def __init__(self, repo_directory):
        self.repo_directory = repo_directory
        self.ignore_path = os.path.join(repo_directory, '.git')
        logging.info("Using VCS: git")

    def status(self):
        cmd = "%s status --porcelain -uall" % GIT
        stdout,stderr = exec_cmd(cmd, self.repo_directory)
        return self._parse_status(stdout, stderr)

    def add(self, filename='.'):
        cmd = "%s add %s" % (GIT, filename)
        stdout,stderr =  exec_cmd(cmd, self.repo_directory)
        if (stderr != ''):
            return NOT_OK,stderr

        return OK,stdout

    def commit(self, message):
        cmd = "%s commit -m \"%s\"" % (GIT, message)
        stdout,stderr =  exec_cmd(cmd, self.repo_directory)
        if (stderr != ''):
            return NOT_OK,stderr

        return OK,stdout

    def commit_all(self, message):
        cmd = "%s commit --all -m \"%s\"" % (GIT, message)
        stdout,stderr =  exec_cmd(cmd, self.repo_directory)
        if (stderr != ''):
            return NOT_OK,stderr

        return OK,stdout

    def handle_conflict(self):
        print("CONFLICT!!!:")
        # fetch state from remote
        cmd = "%s fetch" % GIT
        stdout,stderr = exec_cmd(cmd, self.repo_directory)
        if (stderr != ''):
            return NOT_OK,stderr

        # check for unmerged files
        cmd = "%s ls-files -u" % GIT
        stdout,stderr = exec_cmd(cmd, self.repo_directory)
        ls_files = self._parse_ls_files(stdout, stderr)
        print(ls_files)
        if len(ls_files) >= 3 and len(ls_files[2]) >= 4:
            # copy 3 ("their's") to a temporary file
            cmd = "%s show %s > %s.%s" % (GIT, ls_files[2][1], ls_files[2][1], ls_files[2][3])
            stdout,stderr = exec_cmd(cmd, self.repo_directory)
            if (stderr != ''):
                return NOT_OK,stderr

            # checkout "our's"
            cmd = "%s checkout --ours %s" % (GIT, ls_files[2][3])
            stdout,stderr = exec_cmd(cmd, self.repo_directory)
            if (stderr != ''):
                return NOT_OK,stderr

            # add and commit "our's"
            code,message = self.add(ls_files[2][3])
            if (code != OK):
                return code,message

            # push
            code,message = self.push()
            if (code != OK):
                return code,message

            return OK,"Conflict found. File renamed to: %s.%s" % (ls_files[2][1], ls_files[2][3])

        return OK,"No conflict detected"

    def pull(self, remote='origin', branch='master'):
        cmd = "%s pull --no-ff %s %s" % (GIT, remote, branch)
        stdout,stderr = exec_cmd(cmd, self.repo_directory)
        if ('conflict' in stdout):
            return self.handle_conflict()

        return OK,stdout

    def push(self, remote='origin', branch='master'):
        cmd = "%s push --porcelain %s %s" % (GIT, remote, branch)
        stdout,stderr = exec_cmd(cmd, self.repo_directory)
        if ('[rejected]' in stdout or 'fatal' in stderr):
            return self.handle_conflict()

        return OK,stdout

    def _parse_status(self, stdout, stderr):
        ret = []
        for f in stdout.split("\n"):
            if not f == '':
                ret.append(tuple(f.split()))
        return ret

    def _parse_ls_files(self, stdout, stderr):
        #[FIXME: exactly the same as _parse_status?]
        ret = []
        for f in stdout.split("\n"):
            if not f == '':
                ret.append(tuple(f.split()))
        return ret

