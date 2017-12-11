import errno
import os
import shutil


def make_dir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def remove_dir(path):
    try:
        shutil.rmtree(path)
    except:
        pass


def read_dir(path, ext):
    files = [f for f in os.listdir(path) if f.endswith(ext)]
    return files