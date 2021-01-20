import subprocess
import os
import re
import xml.etree.ElementTree

class Client:
    def __init__(self, cwd = os.getcwd(), stdout = subprocess.PIPE):
        self.cmd = ["svn"]
        self.log_content = None
        self.cwd = cwd
        self.stdout = stdout
        self.diff_cache = {}

    def log(self, decoding = 'utf8'):
        log_cmd = self.cmd + ["log", "--xml"]

        if self.log_content is None:
            self.log_content = []

            data = subprocess.Popen(log_cmd, stdout = self.stdout, cwd = self.cwd).stdout.read()
            root = xml.etree.ElementTree.fromstring(data)

            for e in root.iter('logentry'):
                entry_info = {x.tag: x.text for x in list(e)}

                log_entry = {
                    'msg': entry_info.get('msg'),
                    'author': entry_info.get('author'),
                    'revision': int(e.get('revision')),
                    'date': entry_info.get('date')
                }

                cl = []
                for ch in e.findall('paths/path'):
                    cl.append((ch.attrib['action'], ch.text))

                log_entry['changelist'] = cl

                self.log_content.append(log_entry)

            return self.log_content

    def diff(self, start_version, end_version = None, decoding = 'utf8', cache = False):
        if end_version is None:
            end_version = start_version
            start_version = end_version - 1

        diff_cmd = self.cmd + ["diff", "-r", "{0}:{1}".format(start_version, end_version)]

        if cache and self.diff_cache.setdefault(start_version, {})[end_version]:
            diff_content = self.diff_cache[start_version][end_version]
        else:
            diff_content = []
            data = subprocess.Popen(diff_cmd, stdout = self.stdout, cwd = self.cwd).stdout.read()
            for b in data.split(b'\n'):
                try:
                    diff_content.append(bytes.decode(b, decoding))
                except:
                    diff_content.append(bytes.decode(b))
                else:
                    pass

        diff_content = "\n".join(diff_content)

        if cache and self.diff_cache[start_version][end_version] is None:
            self.diff_cache[start_version][end_version] = diff_content

        return diff_content

    def numstat(self, start_version, end_version = None, decoding = 'utf8', cache = False):
        stat = []
        file_name = None

        diff_content = self.diff(start_version, end_version, decoding, cache)
        for s in diff_content.split('\n'):
            if s.startswith('+++'):
                if file_name:    
                    stat.append((added, removed, file_name))
                added = 0
                removed = 0
                file_name = re.match(r'\+\+\+ (\S+)', s).group(1)
            elif s.startswith('---'):
                pass
            elif s.startswith('+'):
                added = added + 1
            elif s.startswith('-'):
                removed = removed + 1

        if file_name:
            stat.append((added, removed, file_name))
        
        return stat