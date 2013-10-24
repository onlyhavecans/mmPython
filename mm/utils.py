from datetime import datetime
import errno
import os
import shutil
import sys


def cleanup_files(name, nolog=False):
    if os.path.basename(os.getcwd()) == name:
        try:
            if os.path.exists("in"):
                os.unlink("in")
            if os.path.isfile("out"):
                if not nolog:
                    shutil.copyfile("out", get_timestamp())
                os.unlink("out")
        except OSError as e:
            print("unlinking {} caused error {}".format(e.filename, e.message))


def get_timestamp():
    """
    Single place to edit all the timestamsp
    """
    return datetime.now().strftime("%Y-%m-%dT%H%M%S")


def move_to_main_directory():
    muckdir = os.path.join(os.path.expanduser('~'), 'muck')
    try:
        os.makedirs(muckdir)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            print("Cannot make ~/muck. Failing")
            sys.exit(9)
    os.chdir(muckdir)