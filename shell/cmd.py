# -*- coding: utf-8 -*-
#
# shell.cmd
# 
# Execute shell commands in a subprocess
#
# Authors: Konrad Markus <konker@gmail.com>
#

import subprocess

def exec_cmd_out(cmd, cwd=None):
    stdout,stderr = exec_cmd(cmd, cwd)
    return stdout

def exec_cmd_err(cmd, cwd=None):
    stdout,stderr = exec_cmd(cmd, cwd)
    return stderr

def exec_cmd(cmd, cwd=None):
    print cmd
    pipe = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = pipe.communicate()
    pipe.wait()
    return stdout,stderr

