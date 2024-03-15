from coraos.fs.Type.basictype import File

fp = File("test.json")
fp.Open()
fp.LoadContent()
print(fp.Content)
fp.sMove("test", overwrite=True)
