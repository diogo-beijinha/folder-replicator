import argparse
import os
import shutil
import logging

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


sourceFiles = os.listdir(args.source)
replicaFiles = os.listdir(args.replica)
# print(replicaFiles)

logs = open(args.log, "a")

# iterate through files
for filename in os.listdir(args.source):
    file_path = os.path.join(args.source, filename)
    if os.path.isfile(file_path):
        # FILE IS IN REPLICAS
        if filename in replicaFiles:
            logging.info(f"Source file {filename} found in replicas folder!\n")
        # FILE IS NOT IN REPLICAS
        else:
            shutil.copy(file_path, os.path.join(args.replica, filename))
            logging.info(f"Source file {filename} created in replicas folder!\n")

for filename in os.listdir(args.replica):
    file_path = os.path.join(args.replica, filename)
    if os.path.isfile(file_path):
        # FILE IS IN REPLICAS
        if filename not in sourceFiles:
            os.remove(file_path)
            print(f"{filename} not in source")
            logging.warning(f"File {filename} does not exist in Source folder! Deleting from replicas..\n")


# name != name SKIP >> DONE <<
# source not in replica == create file in replica OVER >> DONE <<
# replica not in source == delete replica file OVER >> DONE <<

# name == name => check hash => hash is the same OVER
# name == name => check hash => hash is not the same ==> delete replica file ==> create source file in replica OVER