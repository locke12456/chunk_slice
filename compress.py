import gzip, tarfile
class Compress(object):
    """description of class"""
    name = ""
    zip = None
    def __init__(self, name):
        self.name = name
        self.zip = tarfile.open(name, 'w:gz')
    def Add(self, data, arc):
        self.zip.add(data, arcname=arc)
    def Extract(self, path):
        self.zip.close()
        self.zip = tarfile.open(self.name)
        self.zip.extractall()
        self.zip.close()
    def Close(self):
        self.zip.close()


