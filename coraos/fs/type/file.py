import io
import json
import mimetypes
import os
import shutil
import time


class FileIO_NOT_FOUND(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class FileIO_MODE_ERROR(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class File:
    """
    File type
    Basic type of file.
    """

    def __init__(self, path: str):
        self.FileIO = None
        self.FileIO_info = None
        self.Path = os.path.abspath(path)
        self.Type = mimetypes.guess_type(self.Path)[0]
        stats = os.stat(self.Path)
        self.Size = stats.st_size
        self.CreatedTime = time.localtime(stats.st_mtime)

    def Open(self, mode: str = "w+", encoding: str = "utf-8"):
        self.FileIO = open(self.Path, mode, encoding=encoding)
        self.FileIO_info = {"Mode": mode, "Encoding": encoding}

    def smoveTo(self, pathTo: str):
        """
        coraos.fs.type.file.File.smoveTo
        Move target file to target path in a secure way.
        """
        if self.FileIO is None:
            raise FileIO_NOT_FOUND("FileIO is not open. Please use 'File.Open' to open a FileIO")
        try:
            content = self.FileIO.read()
        except io.UnsupportedOperation as e:
            raise FileIO_MODE_ERROR("FileIO Mode is error. This operation requires w+ or r+ mode, but FileIO is "
                                    "currentlyin {}.".format(self.FileIO_info["Mode"]))
