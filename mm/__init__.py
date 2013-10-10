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
import argparse
from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
from mm.session import MuckSession, MuckFactory
from mm.utils import cleanup_files


class MuMe(object):
    def __init__(self, name, server, port, ssl=False, debug=False):
        self.name = name
        self.server = server
        self.port = port
        self.ssl = ssl
        self.debug = debug

    def enter_directory(self):
        try:
            os.makedirs(self.name)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
        os.chdir(self.name)

    def make_in(self):
        try:
            os.mkfifo("in")
        except OSError:
            print("FIFO already exists. Unlink or exit")
            print("if you run multiple copies in the same directory you're gonna have a bad time")
            if raw_input("Type YES to unlink and recreate: ") == "YES":
                os.unlink("in")
                self.make_in()
            else:
                sys.exitfunc()

    def run(self):
        self.enter_directory()
        self.make_in()
        outfile = open('out', 'w')

        from twisted.internet import reactor, ssl
        endpoint = None
        if self.ssl:
            endpoint = SSL4ClientEndpoint(reactor, self.server, self.port, ssl.ClientContextFactory())
        else:
            endpoint = TCP4ClientEndpoint(reactor, self.server, self.port)
        d = endpoint.connect(MuckFactory(outfile))

        print("Daemonize this shit yourself")
        reactor.run()

        outfile.close()
        sys.exit(0)


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
    atexit.register(cleanup_files, args.name, args.log, args.preserve)
    mm = MuMe(args.name, args.server, args.port, args.ssl, args.debug)
    mm.run()


if __name__ == '__main__':
    main()

__author__ = 'bunnyman'
