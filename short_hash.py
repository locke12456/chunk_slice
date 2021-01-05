import sys
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

def main(argv):
    inputfile = ''
    outputfile = ''
    chunk_size = 1024 * 1024
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
            outputfile = arg
        elif opt in ("-s", "--size"):
            chunk_size = int(arg)
    file = open(inputfile, "rb")
    total = 0
    count = 0
    byte = file.read(chunk_size)
    chunk_info = []
    while byte:
        hash = hashlib.sha1(byte).hexdigest()
        size = len(byte)
        total += size
        data = {'id':count, 'sha1':hash[:10], 'size':size}
        chunk_info.append(data)
        byte = file.read(chunk_size)
        count = count + 1

    file_info = {'filename':inputfile, 'size': total,'chunk_size':chunk_size, 'chunks': chunk_info }
    if outputfile != '':
        save_info(file_info, outputfile)
    else:
        print(json.dumps(file_info))
    file.close()


if __name__ == "__main__":
   main(sys.argv[1:])