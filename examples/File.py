from coraos.fs.type.file import File
fileObj = File("test.json")
fileObj.Open()
fileObj.smoveTo(".")
