import subprocess

def exec_cmd(cmd, cwd=None):
    pipe = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout,stderr = pipe.communicate()
    pipe.wait()
    return stdout,stderr

