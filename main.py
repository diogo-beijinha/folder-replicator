import argparse
import os
import shutil
import logging
import hashlib
import time


class SyncFolders:

    def __init__(self, logfile):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

        # Prevent adding multiple handlers
        if not self.logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s: %(levelname)s: %(message)s")

            # File
            file_handler = logging.FileHandler(logfile)
            file_handler.setFormatter(formatter)

            # Console
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def create_replicas(self, src, dest):
        if not os.path.exists(dest):
            os.makedirs(dest)

        for root, dirs, files in os.walk(src):
            rel_path = os.path.relpath(root, src)
            dest_root = os.path.join(dest, rel_path)

            # Create directories in destination
            for dir_name in dirs:
                dest_dir = os.path.join(dest_root, dir_name)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir)
                    self.logger.info(f"Created directory: {dest_dir}")

            # Copy files
            for filename in files:
                src_file = os.path.join(root, filename)
                dest_file = os.path.join(dest_root, filename)

                if not os.path.exists(dest_file) or get_file_md5(
                        src_file) != get_file_md5(dest_file):
                    shutil.copy2(src_file, dest_file)
                    self.logger.info(f"Copied/Updated file: {dest_file}")

        # Remove files/folders in replicas folder, that don't exist in source
        for root, dirs, files in os.walk(dest, topdown=False):
            rel_path = os.path.relpath(root, dest)
            src_root = os.path.join(src, rel_path)

            for filename in files:
                dest_file = os.path.join(root, filename)
                src_file = os.path.join(src_root, filename)
                if not os.path.exists(src_file):
                    os.remove(dest_file)
                    self.logger.warning(f"Deleted extra file: {dest_file}")

            for dir_name in dirs:
                dest_dir = os.path.join(root, dir_name)
                src_dir = os.path.join(src_root, dir_name)
                if not os.path.exists(src_dir):
                    shutil.rmtree(dest_dir)
                    self.logger.warning(f"Deleted extra directory: {dest_dir}")


def get_file_md5(filepath):
    md5 = hashlib.md5()
    with open(filepath, "rb") as f:
        chunk = f.read(4096)
        while chunk:
            md5.update(chunk)
            chunk = f.read(4096)
    return md5.hexdigest()


def parse_args():
    parser = argparse.ArgumentParser(
        description="Sync two folders periodically")
    parser.add_argument("--src", required=True, help="Source folder path")
    parser.add_argument("--dest",
                        required=True,
                        help="Destination folder path")
    parser.add_argument("--logfile", required=True, help="Log file path")
    parser.add_argument("--interval",
                        type=int,
                        default=10,
                        help="Sync interval in seconds")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    sync = SyncFolders(args.logfile)

    while True:
        sync.create_replicas(args.src, args.dest)
        sync.logger.info(
            f"Synchronization completed. Next sync in {args.interval} seconds..."
        )
        time.sleep(args.interval)
