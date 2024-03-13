import os.path
from file import File


class Folder:
    def __init__(self, path: str):
        if os.path.exists(path):
            if not os.path.isdir(path):
                raise TypeERROR("{} is not a folder.".format(path))
        else:
            raise FolderNotFound("Folder named {} can't be found.".format(path))
        self.path = os.path.abspath(path)

    def is_empty(self):
        if len(os.listdir(self.path)) == 0:
            return True

    def searchFile(self, keyword: str, childfolder: bool = False):
        """
        Search in childfolder is not available.
        """
        files = os.listdir(self.path)
        result = {}
        for i in files:
            if keyword in i:
                path = "{}/{}".format(self.path, i)
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

    def newChildFolder(self, name):
        try:
            Folder("{}/{}".format(self.path, name))
        except FolderNotFound:
            os.mkdir("{}/{}".format(self.path, name))


class TypeERROR(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class FolderNotFound(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message
