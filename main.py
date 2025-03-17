import argparse
import os
import shutil

parser = argparse.ArgumentParser(description="Sync two folders")

# Arguments list
parser.add_argument("source", help="Source folder path")
parser.add_argument("replica", help="Replica folder path")
# parser.add_argument("--interval", type=int, default=10, help="Sync interval in seconds")
parser.add_argument("--log", help="Log file path")

args = parser.parse_args()


# print(f"Interval: {args.interval}")


replicaFiles = os.listdir(args.replica)
print(replicaFiles)

logs = open(args.log, "a")

# iterate through files
for filename in os.listdir(args.source):
    file_path = os.path.join(args.source, filename)
    if os.path.isfile(file_path):
        if filename in replicaFiles:
            logs.writelines(f"Source file {filename} found in replicas folder!\n")
            # print(f"Source file {filename} found in replicas folder!")
        else:
            shutil.copy(file_path, os.path.join(args.replica, filename))
            logs.writelines(f"Source file {filename} created in replicas folder!")