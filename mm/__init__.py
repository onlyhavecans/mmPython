#!/usr/bin/env python
# encoding: utf-8
"""


Created by bunnyman on 2013/10/08.
Copyright (c) 2013 Bunni.biz. All rights reserved.
"""

from __future__ import print_function
import atexit
import argparse
from mm import fifo
from mm.mume import MuMe
from mm.session import MuckSession, MuckFactory
import mm.utils


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


def main():
    args = parse_arguments()
    atexit.register(utils.cleanup_files, args.name, args.log, args.preserve)
    utils.move_to_main_directory()
    mm = MuMe(args.name, args.server, args.port, args.ssl, args.debug)
    mm.run()


if __name__ == '__main__':
    main()

