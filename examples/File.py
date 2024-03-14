from coraos.fs.Type.basictype import File

fp = File("test.json")
fp.Open()
fp.sMove("test", overwrite=True)
