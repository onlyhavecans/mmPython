#!/usr/bin/env python
# encoding: utf-8
"""


Created by bunnyman on 2013/10/08.
Copyright (c) 2013 Bunni.biz. All rights reserved.
"""

from __future__ import print_function
import atexit
import sys
import os
import errno
from datetime import datetime
import twisted
import argparse


class MuMe(object):
    def __init__(self, args):
        self.name = args.name
        self.server = args.server
        self.port = args.port
        self.ssl = args.ssl
        self.debug = args.debug

    def run(self):
        try:
            os.makedirs(self.name)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass

        os.chdir(self.name)
        self._make_in()
        print("Daemonize this shit yourself")

        sys.exit(0)

    def _make_in(self):
        try:
            os.mkfifo("in")
        except OSError:
            print("FIFO already exists. Unlink or exit")
            print("if you run multiple copies in the same directory you're gonna have a bad time")
            if raw_input("Type YES to unlink and recreate: ") == "YES":
                os.unlink("in")
                self._make_in()
            else:
                sys.exitfunc()


def parse_arguments():
    parser = argparse.ArgumentParser(description="A FIFO and filesystem based MU* client")
    parser.add_argument("name", help="connection name")
    parser.add_argument("server", help="Server to connect to")
    parser.add_argument("port", help="Port to connect on", type=int)
    parser.add_argument("--ssl", help="use ssl", action="store_true")
    parser.add_argument("--log", help="save log after disconnect", action="store_true")
    parser.add_argument("--debug", action="store_true")
    parser.add_argument("--preserve", help="Preserve directory on disconnect", action="store_true")
    return parser.parse_args()


def cleanup(name, preserve, log):
    if os.path.basename(os.curdir) == name:
        try:
            if os.path.exists("in"):
                os.unlink("in")
            if not preserve:
                if os.path.exists("out"):
                    os.unlink("out")
        except OSError as e:
            print("unlinking {} caused error {}".format(e.filename, e.message))


def main():
    args = parse_arguments()
    atexit.register(cleanup, args.name, args.preserve, args.log)
    mm = MuMe(args)
    mm.run()


if __name__ == '__main__':
    main()

__author__ = 'bunnyman'
