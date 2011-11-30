# -*- coding: utf-8 -*-
#
# vcs/impl/git.py
# Wrapper around the git command
#
# Authors: Konrad Markus <konker@gmail.com>
#

import logging
import os.path
import time
import subprocess
from shell.cmd import exec_cmd

OK = True
NOT_OK = False

# try to locate the git command line tool, or raise ImportError
if exec_cmd("which git") == '':
    raise ImportError()


class VCSImpl(object):
    def __init__(self, repo_directory):
        self.repo_directory = repo_directory
        self.ignore_path = os.path.join(repo_directory, '.git')
        logging.info("Using git VCS")

    def status(self):
        cmd = "git status --porcelain -uall"
        stdout,stderr = exec_cmd(cmd, self.repo_directory)
        return self._parse_status(stdout, stderr)

    def add(self, filename='.'):
        cmd = "git add %s" % filename
        stdout,stderr =  exec_cmd(cmd, self.repo_directory)
        if (stderr != ''):
            return NOT_OK,stderr

        return OK,stdout

    def commit_all(self, message):
        cmd = "git commit --all -m \"%s\"" % message
        stdout,stderr =  exec_cmd(cmd, self.repo_directory)
        if (stderr != ''):
            return NOT_OK,stderr

        return OK,stdout

    def pull(self, remote='origin', branch='master'):
        cmd = "git pull %s %s" % (remote, branch)
        stdout,stderr = exec_cmd(cmd, self.repo_directory)
        if ('conflict' in stdout):
            return NOT_OK,stdout

        return OK,stdout

    def push(self, remote='origin', branch='master'):
        cmd = "git push --porcelain %s %s" % (remote, branch)
        stdout,stderr = exec_cmd(cmd, self.repo_directory)
        if ('[rejected]' in stdout or 'fatal' in stderr):
            return NOT_OK,stderr

        return OK,stdout

    def _parse_status(self, stdout, stderr):
        ret = []
        for f in stdout.split("\n"):
            if not f == '':
                ret.append(tuple(f.split()))
        return ret

