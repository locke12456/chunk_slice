import os
import sys
import getopt
import hashlib
import json

def verify_chunk(count, verify_data, verify_failed, verify_info, writer):
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

def main(argv):
    inputfile = ''
    jsonfile = ''
    remove = False
    try:
        opts, args = getopt.getopt(argv,"hv:r:",["verify=", "remove="])
    except getopt.GetoptError:
        print('-v <verify>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('-v <verify>')
            sys.exit()
        elif opt in ("-v", "--verify"):
            jsonfile = arg
        elif opt in ("-r", "--remove"):
            remove = True
    with open(jsonfile) as json_file:
        data = json.load(json_file)
        filename = "{name}".format(name=data["filename"])
        total = 0
        count = 0
        verify_failed = 0
        chunk_info = []
        verify_info = data["chunks"]
        with open(filename, "wb") as writer:
            for count in range(0, len(verify_info)):
                verify_data = verify_info[count]
                if os.path.exists(verify_info[count]["sha1"]):
                    total, verify_failed = verify_chunk(count, verify_data, verify_failed, verify_info, writer)
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
            if remove == True:
                for count in range(0, len(verify_info)):
                    os.remove(verify_info[count]["sha1"])
            #json_file.close()
    


if __name__ == "__main__":
   main(sys.argv[1:])
