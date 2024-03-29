import os
import sys, time
import getopt
import utils, short_hash
import json
def sender_config(file, dir_path):
    config = None
    with open(file) as json_file:
        config = json.load(json_file)
        config["broadcast"]["dir_path"] = dir_path
    if config != None:
        with open(file, 'w') as outfile:
            json.dump(config, outfile)
def main(argv):
    dir = ''
    try:
        opts, args = getopt.getopt(argv,"hd:",["dir="])
    except getopt.GetoptError:
        print('-d <dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('-d <dir>')
            sys.exit()
        elif opt in ("-d", "--dir"):
            dir = arg
    files = utils.ListDir(dir)
    while True :
        for file in files.GetNewFiles():
            print(file["path"])
            print(file["update_time"])
            inputfile = file["path"]
            filename = os.path.basename(file["path"])
            if filename == "sender":
                continue
            outputfile = "{jsonname}.json".format(jsonname=os.path.splitext(filename)[0])
            chunk_size = 1024 * 1024
            file = open(inputfile, "rb")
            total = 0
            count = 0
            hash = ""
            byte = file.read(chunk_size)
            chunk_info = []
            byte, count, hash, total = short_hash.slice(byte, chunk_info, chunk_size, count, file, inputfile)
            file.close()
            dir = short_hash.save_file_info(chunk_info, chunk_size, hash, inputfile, outputfile, total)
            config = "sender.json"
            sender_config(config, dir)
            utils.ExecProgram(files.fileserver, ["sender.json"])
        time.sleep(1)
        files.Update()


if __name__ == "__main__":
   main(sys.argv[1:])
