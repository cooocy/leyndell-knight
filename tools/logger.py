import os
import time

from tools import file_tools


class Logger:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def log(self, *strs):
        parent_path = file_tools.get_parent_full_dir(self.file_path)
        if not os.path.exists(parent_path):
            os.mkdir(parent_path)
        s = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime())
        for ss in strs:
            s = s + ' ' + ss
        with open(self.file_path, 'a+') as f:
            f.write('\n')
            f.write(s)
        f.close()

