import sys, os
import getopt
import hashlib
import json

def save_info(file_info, outputfile):

    with open(outputfile, 'w') as outfile:
        json.dump(file_info, outfile)
    #json_file = open(outputfile, "w+")
    #json_file.write(json.dumps(file_info))
    #json_file.flush()
    #json_file.close()

def check_path(inputfile):
    dir = "{inputfile}_out".format(inputfile=inputfile)
    if os.path.exists(dir):
        pass
    else:
        os.mkdir(dir)
    return dir

def slice(byte, chunk_info, chunk_size, count, file, inputfile):
    total = 0
    dir = check_path(inputfile)
    dirpath = os.path.abspath(dir)
    while byte:
        hash = hashlib.sha1(byte).hexdigest()
        size = len(byte)
        total += size
        name = hash
        data = {'id':count, 'sha1':name, 'size':size}
        chunk_info.append(data)
        filename = "{dirpath}\{name}".format(dirpath=dirpath, name=name)
        with open(filename, "wb") as writer:
            writer.write(byte)
        byte = file.read(chunk_size)
        count = count + 1
    return byte, count, hash, total

def save_file_info(chunk_info, chunk_size, hash, inputfile, outputfile, total):
    dir = check_path(inputfile)
    dirpath = os.path.abspath(dir)
    with open(inputfile, "rb") as file:
        byte = file.read(total)
        hash = hashlib.sha1(byte).hexdigest()
    filename = os.path.basename(inputfile)
    file_info = {'filename':filename,'sha1': hash, 'size': total,'chunk_size':chunk_size, 'chunks': chunk_info }
    if outputfile != '':
        filename = "{dirpath}\{name}".format(dirpath=dirpath, name=outputfile)
        save_info(file_info, filename)
    else:
        print(json.dumps(file_info))

def parse_options(argv, inputfile):
    try:
        opts, args = getopt.getopt(argv,"hi:o:s:",["ifile=","ofile=", "size="])
    except getopt.GetoptError:
        print(' -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(' -i <inputfile> -o <outputfile> -s <chunk size>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            os.mkdir("{inputfile}_out".format(inputfile=inputfile), 755)
            outputfile = arg
        elif opt in ("-s", "--size"):
            chunk_size = int(arg)
    return chunk_size, inputfile, outputfile

def main(argv):
    inputfile = ''
    outputfile = ''
    chunk_size = 1024 * 1024
    chunk_size, inputfile, outputfile = parse_options(argv, inputfile)
    file = open(inputfile, "rb")
    total = 0
    count = 0
    hash = ""
    byte = file.read(chunk_size)
    chunk_info = []
    byte, count, hash, total = slice(byte, chunk_info, chunk_size, count, file, inputfile)
    file.close()
    save_file_info(chunk_info, chunk_size, hash, inputfile, outputfile, total)


if __name__ == "__main__":
   main(sys.argv[1:])