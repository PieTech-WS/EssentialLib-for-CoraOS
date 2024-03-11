import os, mimetypes, time

class File:
    '''
    File type
    Basic type of file.
    '''
    def __init__(self, path: str):
        self.Path = os.path.abspath(path)
        self.Type = mimetypes.guess_type(self.path)[0]
        stats = os.stat(self.path)
        self.Size = stats.st_size
        filetime = time.localtime(stats.st_mtime)
        self.CreatedTime = time.strftime("%Y-%M-%d", filetime)
