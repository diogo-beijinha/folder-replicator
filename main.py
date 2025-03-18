import argparse
import os
import shutil
import logging
import hashlib

class SyncFolders:
    def __init__(self, log_file):
        logging.basicConfig(filename=log_file, format='%(asctime)s: %(levelname)s: %(message)s', level=logging.INFO)

    def create_replicas(self, source_path, replica_path):
        
        sourceFiles = os.listdir(source_path)
        replicaFiles = os.listdir(replica_path)
        
        logs = open(args.log, "a")

        # iterate through files for removal
        for filename in os.listdir(replica_path):
            file_path = os.path.join(replica_path, filename)
            if os.path.isfile(file_path):
                # DELETE FILE FROM REPLICAS IF NOT IN SOURCE
                if filename not in sourceFiles or filename in sourceFiles and get_file_md5(file_path) != get_file_md5(os.path.join(source_path, filename)):
                    logging.warning(f"File {filename} does not exist in Source folder! Deleting from replicas..\n")
                    os.remove(file_path)

        # iterate through files for creation
        for filename in os.listdir(source_path):
            file_path = os.path.join(source_path, filename)
            if os.path.isfile(file_path):
                # FILE IS IN REPLICAS
                if filename in replicaFiles and get_file_md5(file_path) == get_file_md5(os.path.join(replica_path, filename)):
                    logging.info(f"Source file {filename} found in replicas folder!\n")
                # FILE IS NOT IN REPLICAS
                else:
                    shutil.copy2(file_path, os.path.join(replica_path, filename))
                    logging.info(f"Source file {filename} created in replicas folder!\n")

def get_file_md5(filepath):
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        chunk = f.read(4096)
        while chunk:
            md5.update(chunk)
            chunk = f.read(4096)
    return md5.hexdigest()

def parse_args():
    parser = argparse.ArgumentParser(description="Sync two folders")
    # Arguments list
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    # parser.add_argument("--interval", type=int, default=10, help="Sync interval in seconds")
    parser.add_argument("--log", help="Log file path")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    sync = SyncFolders(args.log)
    sync.create_replicas(args.source, args.replica)
