import subprocess
import os

class Client:
    def __init__(self):
        self.cmd = "svn"
        self.log = None
        self.cwd = os.getcwd()
        self.stdout = subprocess.PIPE
        
    def log(self, decode='utf8'):
        if self.log is None:
            self.log = subprocess.Popen([self.cmd, "log"], stdout = self.stdout, cwd = self.cwd).stdout.read()
        return bytes.decode(v, decode)