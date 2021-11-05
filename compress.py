import gzip
class Compress(object):
    """description of class"""
    name = ""
    zip = None
    def __init__(self, name):
        self.name = name
        self.zip = gzip.open(name, 'wb')
    def Add(self, data):
        self.zip.write(data)
    def Close(self):
        self.zip.close()


