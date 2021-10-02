import glob
import os


def create_dirs(*args):
    for directory in args:
        if not os.path.exists(directory):
            os.makedirs(directory)


def delete_directory_files(path):
    files = glob.glob(path + '/*')
    for f in files:
        os.remove(f)
