import gzip, tarfile
class Compress(object):
    """description of class"""
    name = ""
    zip = None
    def __init__(self, name = None):
        self.name = name
        if name != None:
            self.zip = tarfile.open(name, 'w:gz')
    def Add(self, data, arc):
        self.zip.add(data, arcname=arc)
    def Extract(self, name):
        if self.zip != None:
            self.zip.close()
        self.zip = tarfile.open(name)
        self.zip.extractall()
        self.zip.close()
    def Close(self):
        self.zip.close()


