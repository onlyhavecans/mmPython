from datetime import datetime
import os
import shutil

__author__ = 'bitm'


def cleanup_files(name, log=True, preserve=False):
    if os.path.basename(os.getcwd()) == name:
        try:
            if os.path.exists("in"):
                os.unlink("in")
            if os.path.isfile("out"):
                if log:
                    shutil.copyfile("out", datetime.now().strftime("%Y-%m-%dT%H%M%S"))
                if not preserve:
                    os.unlink("out")
        except OSError as e:
            print("unlinking {} caused error {}".format(e.filename, e.message))