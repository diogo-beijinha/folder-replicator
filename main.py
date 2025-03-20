import argparse
import os
import shutil
import logging
import hashlib
import time

class SyncFolders:
    def __init__(self, log_file):
        logging.basicConfig(filename=log_file, format="%(asctime)s: %(levelname)s: %(message)s", level=logging.INFO)

    def create_replicas(self, source_path, replica_path):
        # Ensure replica folder exists
        if not os.path.exists(replica_path):
            os.makedirs(replica_path)

        # Sync files and folders
        for root, dirs, files in os.walk(source_path):
            rel_path = os.path.relpath(root, source_path)
            replica_root = os.path.join(replica_path, rel_path)

            # Create missing directories in replica
            for dir_name in dirs:
                replica_dir = os.path.join(replica_root, dir_name)
                if not os.path.exists(replica_dir):
                    os.makedirs(replica_dir)
                    logging.info(f"Created directory: {replica_dir}")

            # Copy or update files
            for filename in files:
                source_file = os.path.join(root, filename)
                replica_file = os.path.join(replica_root, filename)

                if not os.path.exists(replica_file) or get_file_md5(source_file) != get_file_md5(replica_file):
                    shutil.copy2(source_file, replica_file)
                    logging.info(f"Copied/Updated file: {replica_file}")

        # Remove extra files and folders from replica
        for root, dirs, files in os.walk(replica_path, topdown=False):  # Traverse bottom-up to delete empty dirs
            rel_path = os.path.relpath(root, replica_path)
            source_root = os.path.join(source_path, rel_path)

            # Remove extra files
            for filename in files:
                replica_file = os.path.join(root, filename)
                source_file = os.path.join(source_root, filename)
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    logging.warning(f"Deleted extra file: {replica_file}")

            # Remove extra directories
            for dir_name in dirs:
                replica_dir = os.path.join(root, dir_name)
                source_dir = os.path.join(source_root, dir_name)
                if not os.path.exists(source_dir):
                    shutil.rmtree(replica_dir)
                    logging.warning(f"Deleted extra directory: {replica_dir}")

def get_file_md5(filepath):
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        chunk = f.read(4096)
        while chunk:
            md5.update(chunk)
            chunk = f.read(4096)
    return md5.hexdigest()

def parse_args():
    parser = argparse.ArgumentParser(description="Sync two folders periodically with subdirectory support")
    parser.add_argument("source", help="Source folder path")
    parser.add_argument("replica", help="Replica folder path")
    parser.add_argument("--interval", type=int, default=10, help="Sync interval in seconds")
    parser.add_argument("--log", help="Log file path")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    sync = SyncFolders(args.log)

    while True:
        sync.create_replicas(args.source, args.replica)
        logging.info(f"Synchronization completed. Next sync in {args.interval} seconds...")
        time.sleep(args.interval)
