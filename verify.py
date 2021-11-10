import os
import sys, time
import getopt
import hashlib
import json
import utils


def main(argv):
    inputfile = ''
    jsonfile = ''
    path = ''
    json_list = None
    remove = False
    monitor = 1
    jsonList = None
    try:
        opts, args = getopt.getopt(argv,"hv:d:m:r",["verify=", "dir=", "remove=", "monitor="])
    except getopt.GetoptError:
        print('-v <verify>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('-v <verify>')
            sys.exit()
        elif opt in ("-v", "--verify"):
            jsonfile = arg
        elif opt in ("-d", "--dir"):
            path = arg
        elif opt in ("-m", "--monitor"):
            monitor = int(arg, 10)
        elif opt in ("-r", "--remove"):
            remove = True
    if path == '':
        path = jsonfile

    while monitor > 0:
        utils.VerifyChunks(path, remove)        
        monitor -= 1

if __name__ == "__main__":
   main(sys.argv[1:])
