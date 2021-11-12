import glob
import os
import time
import subprocess
import compress
import json
import hashlib
from pathlib import Path
def verifyChunk(count, verify_data, verify_failed, verify_info, total, writer):
    file = open(verify_info[count]["sha1"], "rb")
    max_size = verify_info[count]["size"]
    byte = file.read(max_size)
    hash = hashlib.sha1(byte).hexdigest()
    size = len(byte)
    sha1 = hash
    if verify_data["id"] == count and verify_data["sha1"] == sha1:
        print("chunk [%d:%d] %s == %s success" % (verify_data["id"], count, verify_data["sha1"], sha1))
    else:
        verify_failed += 1
        print("chunk [%d:%d] %s != %s failed" % (verify_data["id"], count, verify_data["sha1"], sha1))
    total += size
    if verify_failed == 0:
        writer.write(byte)
    file.close()
    return total, verify_failed

def save_info(file_info, outputfile):
    with open(outputfile, 'w') as outfile:
        json.dump(file_info, outfile)

def saveSliceFileInfo(chunk_info, chunk_size, hash, inputfile, outputfile, total):
    dir = checkPath(inputfile)
    dirpath = os.path.abspath(dir)
    with open(inputfile, "rb") as file:
        byte = file.read(total)
        hash = hashlib.sha1(byte).hexdigest()
    filename = os.path.basename(inputfile)
    file_info = {'filename':filename,'sha1': hash, 'size': total,'chunk_size':chunk_size, 'chunks': chunk_info }
    if outputfile != '':
        data_folder = Path(dirpath)
        filename = data_folder / outputfile
        save_info(file_info, filename)
    else:
        print(json.dumps(file_info))
    return dirpath

def checkPath(inputfile):
    dir = "{inputfile}_out".format(inputfile=inputfile)
    if os.path.exists(dir):
        pass
    else:
        os.mkdir(dir)
    return dir

def slice(byte, chunk_info, chunk_size, count, file, inputfile):
    total = 0
    dir = checkPath(inputfile)
    dirpath = os.path.abspath(dir)
    while byte:
        hash = hashlib.sha1(byte).hexdigest()
        size = len(byte)
        total += size
        name = hash
        data = {'id':count, 'sha1':name, 'size':size}
        chunk_info.append(data)
        data_folder = Path(dirpath)
        filename = data_folder / name
        with open(filename, "wb") as writer:
            writer.write(byte)
        byte = file.read(chunk_size)
        count = count + 1
    return byte, count, hash, total, dirpath

def SliceFile(chunk_size, inputfile, outputfile):
    file = open(inputfile, "rb")
    total = 0
    count = 0
    hash = ""
    byte = file.read(chunk_size)
    chunk_info = []
    byte, count, hash, total, dir = slice(byte, chunk_info, chunk_size, count, file, inputfile)
    file.close()
    saveSliceFileInfo(chunk_info, chunk_size, hash, inputfile, outputfile, total)
    return dir

def FindProgram(program):
    process = subprocess. run(
        ['which', program], capture_output=True, text=True)

    if process.returncode == 0:
        print(f'The program "{program}" is installed')

        print(f'The location of the binary is: {process.stdout}')
        return True
    else:
        print(f'Sorry the {program} is not installed')

        print(process.stderr)

    print('\n')

def ExecProgram(program, args, log = None):
    if log != None:
        logFile = open(log, 'w')
    cmd = [program]
    cmd.extend(args)
    process = subprocess.run(
        cmd, stdout=logFile)

    if process.returncode == 0:
        return logFile
    else:
        print(process.stderr)
    return logFile 

def ExecParallelProgram(program, args, log = None):
    if log != None:
        logFile = open(log, 'w')
    cmd = [program]
    cmd.extend(args)    
    process = subprocess.Popen(cmd, stdout=logFile, stderr=subprocess.PIPE, universal_newlines=True)
    return process, logFile 

def CompressFiles(dirPath, filename):
    files = ListDir(dirPath)
    zipName = "{name}.tar.gz".format(name=filename)
    comp = compress.Compress(zipName)
    #comp.Add(dirPath,filename)
    for file in files.GetNewFiles():
        comp.Add(file["path"], file["name"])
    comp.Close()
    return zipName

def DecompressFiles(filename, dirPath):
    comp = compress.Compress("{name}.tar.gz".format(name=filename))
    comp.Extract(dirPath)

def VerifyChunks(path, remove = False):
    cwd = os.getcwd()
    result = False
    if path != '':
        jsonList = ListDir(path, "/*.json")
        if jsonList != None:
            jsonfiles = jsonList.GetNewFiles()
            json_list = []
            for file in jsonfiles:
                json_list.append(file["path"])
        else:
            json_list = [path]
    for file in json_list:
        with open(file) as json_file:
            data = json.load(json_file)
            filename = "{name}".format(name=data["filename"])
            total = 0
            count = 0
            verify_failed = 0
            chunk_info = []
            verify_info = data["chunks"]
            os.chdir(path)
            with open(filename, "wb") as writer:
                for count in range(0, len(verify_info)):
                    verify_data = verify_info[count]
                    if os.path.exists(verify_info[count]["sha1"]):
                        total, verify_failed = verifyChunk(count, verify_data, verify_failed, verify_info, total, writer)
                    else:
                        print("chunk [%d:%d] %s not exist." % (verify_data["id"], count, verify_data["sha1"]))
                        #break
            max_size = data["size"]
            if total != max_size:
                print("file [%s] total size: %d != verify size: %d" % (filename, total, max_size))
                os.remove(data["filename"])
            else:
                file = open(filename, "rb")  
                byte = file.read(max_size)
                hash = hashlib.sha1(byte).hexdigest()
                print("file [%s] total size: %d == verify size: %d" % (filename, total, max_size))
                print("file [%s] sha1: %s, origin sha1: %s" % (filename, hash, data["sha1"]))
                result = True
                if remove == True:
                    for count in range(0, len(verify_info)):
                        os.remove(verify_info[count]["sha1"])
                #json_file.close()
        os.chdir(cwd)
    return result
class ListDir(object):
    """description of class"""
    def __init__(self, path, ext = None):
        self.fileserver = "udp_fileserver"
        self.files = {}
        self.ext = '/*'
        if ext != None:
            self.ext = ext
        self.dir_name = os.path.abspath(path)
        self.Update()
            #print(timestamp_str, ' -->', file_path)  
        #return self.files
    def Update(self):
        self.new_files = []
        # Get list of all files only in the given directory
        list_of_files = filter( os.path.isfile,
                                glob.glob(self.dir_name + self.ext) )
        # Sort list of files based on last modification time in ascending order
        #list_of_files = sorted( list_of_files,
        #                        key = os.path.getmtime)
        # Iterate over sorted list of files and print file path 
        # along with last modification date time 
        for file_path in list_of_files:
            timestamp = os.path.getmtime(file_path)

            if self.files.get(timestamp) == None:
                self.new_files.append(timestamp)
            self.files[timestamp] = file_path

    def GetNewFiles(self):
        files = []
        for key in self.new_files:
            filename = os.path.basename(self.files[key])
            files.append({'name':filename, 'path': self.files[key], 'update_time': key})
        return files


   