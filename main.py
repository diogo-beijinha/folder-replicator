import argparse
import os
import shutil
import logging
import hashlib

class SyncFolders:

    def parse_args(self):
        pass

    def create_replicas(self, source, replica):
        pass

def get_file_md5(filepath):
    md5 = hashlib.md5()

    # handle content in binary form
    f = open(filepath, "rb")

    while chunk := f.read(4096):
        md5.update(chunk)
    
    return md5.hexdigest()


# parse args
parser = argparse.ArgumentParser(description="Sync two folders")

# Arguments list
parser.add_argument("source", help="Source folder path")
parser.add_argument("replica", help="Replica folder path")
# parser.add_argument("--interval", type=int, default=10, help="Sync interval in seconds")
parser.add_argument("--log", help="Log file path")

args = parser.parse_args()

logging.basicConfig(filename=args.log, 
                    format='%(asctime)s: %(levelname)s: %(message)s', 
                    level=logging.INFO)


# print(f"Interval: {args.interval}")

# create replicas
sourceFiles = os.listdir(args.source)
replicaFiles = os.listdir(args.replica)
# print(replicaFiles)

logs = open(args.log, "a")

# iterate through files for removal
for filename in os.listdir(args.replica):
    file_path = os.path.join(args.replica, filename)
    if os.path.isfile(file_path):
        # DELETE FILE FROM REPLICAS IF NOT IN SOURCE
        if filename not in sourceFiles or filename in sourceFiles and get_file_md5(file_path) != get_file_md5(os.path.join(args.source, filename)):
            print(f"{filename} not in source")
            logging.warning(f"File {filename} does not exist in Source folder! Deleting from replicas..\n")
            os.remove(file_path)

# iterate through files for creation
for filename in os.listdir(args.source):
    file_path = os.path.join(args.source, filename)
    if os.path.isfile(file_path):
        # FILE IS IN REPLICAS
        if filename in replicaFiles and get_file_md5(file_path) == get_file_md5(os.path.join(args.replica, filename)):
            logging.info(f"Source file {filename} found in replicas folder!\n")
        # FILE IS NOT IN REPLICAS
        else:
            shutil.copy(file_path, os.path.join(args.replica, filename))
            logging.info(f"Source file {filename} created in replicas folder!\n")

