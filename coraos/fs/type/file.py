import io
import json
import mimetypes
import os
import shutil
import time
from folder import Folder


def CreateFile(path: str):
    with open(path, "w") as a:
        a.write("")
    return File(path)


class FileIO_NOT_FOUND(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class FileIO_MODE_ERROR(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class File_SecureMove_Check_ERROR(Exception):
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
        self.Name = os.path.basename(self.Path)
        self.Type = mimetypes.guess_type(self.Path)[0]
        stats = os.stat(self.Path)
        self.Size = stats.st_size
        self.CreatedTime = time.localtime(stats.st_mtime)

    def Open(self, mode: str = "w+", encoding: str = "utf-8"):
        self.FileIO = open(self.Path, mode, encoding=encoding)
        self.FileIO_info = {"Mode": mode, "Encoding": encoding}

    def smoveTo(self, pathTo: str, overwrite: bool=False):
        """
        coraos.fs.type.file.File.smoveTo
        Move target file to target path in a secure way.
        """
        if self.FileIO is None:
            raise FileIO_NOT_FOUND("FileIO is not open. Please use 'File.Open' to open a FileIO")
        try:
            content = self.FileIO.read()
        except io.UnsupportedOperation:
            raise FileIO_MODE_ERROR("FileIO Mode is error. This operation requires w+ or r+ mode, but FileIO is "
                                    "currentlyin {}.".format(self.FileIO_info["Mode"]))
        targetPath = Folder(pathTo)
        # check files
        if targetPath.checkFile(self.Name):
            if overwrite:
                pass
            else:
                raise File_SecureMove_Check_ERROR("There is already a file with the same name in the target "
                                                  "directory, but overwrite is set to False")
