import subprocess
import os

class Client:
    def __init__(self, cwd = os.getcwd(), stdout = subprocess.PIPE):
        self.cmd = "svn"
        self.log_content = None
        self.cwd = cwd
        self.stdout = stdout

    def log(self, decoding='utf8'):
        if self.log_content is None:
            self.log_content = subprocess.Popen([self.cmd, "log"], stdout = self.stdout, cwd = self.cwd).stdout.read()
        return bytes.decode(self.log_content, decoding)

    def diff(self, start_version, end_version = None, decoding='utf8'):
        if end_version is None:
            end_version = start_version
            start_version = str(int(v[1:]) - 1)
        diff_cmd = "{0} diff -r {1}:{2}".format(start_version, end_version)
        diff_content = subprocess.Popen([self.cmd, diff_cmd], stdout = self.stdout, cwd = self.cwd).stdout.read()
        return bytes.decode(diff_content, decoding)