import os.path


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

    def new_child_folder(self, name):
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
