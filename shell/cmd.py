import subprocess

def exec_cmd(cmd, cwd=None):
    pipe = subprocess.Popen(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out,error = pipe.communicate()
    pipe.wait()
    return out,error

