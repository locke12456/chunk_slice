import sys
import getopt
import hashlib
import json

def main(argv):
    inputfile = ''
    jsonfile = ''
    try:
        opts, args = getopt.getopt(argv,"hf:v:",["file=","verify="])
    except getopt.GetoptError:
        print(' -f <file> -v <verify>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(' -f <file> -v <verify>')
            sys.exit()
        elif opt in ("-f", "--file"):
            inputfile = arg
        elif opt in ("-v", "--verify"):
            jsonfile = arg
    with open(jsonfile) as json_file:
        data = json.load(json_file)
        file = open(inputfile, "rb")
        max_size = data["chunk_size"]
        total = 0
        count = 0
        byte = file.read(max_size)
        chunk_info = []
        verify_info = data["chunks"]
        while byte:
            hash = hashlib.sha1(byte).hexdigest()
            #print("chunk: [" + str(count) +"] ("+ str(len(byte))+") " + hash[:10])
            size = len(byte)
            verify_data = verify_info[count]
            sha1 = hash[:10]
            if verify_data["id"] == count and verify_data["sha1"] == sha1:
                print("chunk [%d:%d] %s == %s success" % (verify_data["id"], count, verify_data["sha1"], sha1))
            else:
                print("chunk [%d:%d] %s != %s failed" % (verify_data["id"], count, verify_data["sha1"], sha1))
            total += size
            data = {'id':count, 'sha1':hash[:10], 'size':size}
            chunk_info.append(data)
            byte = file.read(max_size)
            count = count + 1

    #json_file.close()
    file.close()


if __name__ == "__main__":
   main(sys.argv[1:])
