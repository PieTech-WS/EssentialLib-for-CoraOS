import io
import mimetypes
import os
import time


# coraos.fs.type.File
def CreateFile(path: str):
    try:
        return File(path)
    except FileNotFound:
        with open(path, "w") as a:
            a.write("")
        return File(path)
    except TypeERROR:
        raise TypeERROR("There is already a folder with the same name.")


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
        if not os.path.isfile(path):
            raise TypeERROR("{} is not a file.".format(path))
        else:
            pass
        self.Content = None
        self.FileIO = None
        self.FileIO_info = None
        self.Path = os.path.abspath(path)
        self.Parent = os.path.dirname(self.Path)
        self.Name = os.path.basename(self.Path)
        self.Type = mimetypes.guess_type(self.Path)[0]
        stats = os.stat(self.Path)
        self.Size = stats.st_size
        self.CreatedTime = time.localtime(stats.st_mtime)

    def Open(self, mode: str = "r+", encoding: str = "utf-8"):
        self.FileIO = open(self.Path, mode, encoding=encoding)
        self.FileIO_info = {"Mode": mode, "Encoding": encoding}

    def Write(self, content):
        self.FileIO.write(content)

    def GetContent(self):
        self.Content = self.FileIO.read()

    def sMove(self, pathTo: str, overwrite: bool = False, returnFile: bool = False):
        """
        coraos.fs.type.file.File.smoveTo
        Move target file to target path in a secure way.
        """
        if self.FileIO is None:
            raise FileIO_NOT_FOUND("FileIO is not open. Please use 'File.Open' to open a FileIO")
        try:
            content = self.FileIO.read()
            del content
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
        targetFile = targetPath.newFile(self.Name)
        targetFile.Open()
        self.GetContent()
        targetFile.Write(self.Content)
        if returnFile:
            return targetFile


class TypeERROR(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class FileNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


# coraos.fs.type.Folder
def CreateFolder(path: str):
    try:
        Folder(path)
    except FolderNotFound:
        os.mkdir(path)
    except TypeERROR:
        raise TypeERROR("There is already a file with the same name")


class Folder:
    def __init__(self, path: str):
        if os.path.exists(path):
            if not os.path.isdir(path):
                raise TypeERROR("{} is not a folder.".format(path))
        else:
            raise FolderNotFound("Folder {} can't be found.".format(path))
        self.Path = os.path.abspath(path)

    def is_empty(self):
        if len(os.listdir(self.Path)) == 0:
            return True

    def searchFile(self, keyword: str, childfolder: bool = False):
        """
        Search in childfolder is not available.
        """
        files = os.listdir(self.Path)
        result = {}
        for i in files:
            if keyword in i:
                path = "{}/{}".format(self.Path, i)
                try:
                    result[i] = Folder(path)
                except TypeERROR:
                    result[i] = File(path)
        return result

    def checkFile(self, name: str):
        result: dict = self.searchFile(name)
        for i in result.keys():
            if i == name:
                return True

    def newFile(self, name: str):
        CreateFile("{}/{}".format(self.Path, name))
        return File(name)

    def newChildFolder(self, name):
        try:
            Folder("{}/{}".format(self.Path, name))
        except FolderNotFound:
            os.mkdir("{}/{}".format(self.Path, name))


class FolderNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
