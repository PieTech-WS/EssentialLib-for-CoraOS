import os
from coraos.dynmodule import Module
from coraos.log.file import LogFile


class Lang:
    def __int__(self):
        self.log = LogFile("i18n API", "log")
        rs = Module().check()
        if rs == "None":
            self.log.error("没有该文件的映射名称.")
