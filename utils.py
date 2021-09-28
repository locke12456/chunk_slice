import glob
import os
import time
import subprocess

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

def ExecProgram(program, args):
    cmd = [program]
    cmd.extend(args)
    process = subprocess. run(
        cmd)

    if process.returncode == 0:
        return True
    else:
        print(process.stderr)

    print('\n')
    return False 

class ListDir(object):
    """description of class"""
    def __init__(self, path):
        self.fileserver = "udp_fileserver"
        self.files = {}
        self.dir_name = os.path.abspath(path)
        self.Update()
            #print(timestamp_str, ' -->', file_path)  
        #return self.files
    def Update(self):
        self.new_files = []
        
        # Get list of all files only in the given directory
        list_of_files = filter( os.path.isfile,
                                glob.glob(self.dir_name + '/*') )
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
            files.append({'path': self.files[key], 'update_time': key})
        return files


   