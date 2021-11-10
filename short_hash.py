import sys, os
import getopt
import utils

def parse_options(argv, inputfile):
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
            os.mkdir("{inputfile}_out".format(inputfile=inputfile), 755)
            outputfile = arg
        elif opt in ("-s", "--size"):
            chunk_size = int(arg, 10)
    return chunk_size, inputfile, outputfile

def main(argv):
    inputfile = ''
    outputfile = ''
    chunk_size, inputfile, outputfile = parse_options(argv, inputfile)
    utils.SliceFile(chunk_size, inputfile, outputfile)


if __name__ == "__main__":
   main(sys.argv[1:])