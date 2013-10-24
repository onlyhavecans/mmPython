#!/usr/bin/env python
# encoding: utf-8
"""
$FILE

Created by bunnyman on 2013/10/24.
Copyright (c) 2013 Bunni.biz. All rights reserved.
"""
import errno
import sys
import os
from twisted.internet.endpoints import SSL4ClientEndpoint, TCP4ClientEndpoint
from twisted.python import log
from mm import MuckFactory


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
            else:
                print("Cannot make connection directory {}".format(self.name))
                sys.exit(9)
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
        if self.debug:
            log.startLogging(sys.stdout)
        from twisted.internet import reactor, ssl
        endpoint = None
        if self.ssl:
            endpoint = SSL4ClientEndpoint(reactor, self.server, self.port, ssl.ClientContextFactory())
        else:
            endpoint = TCP4ClientEndpoint(reactor, self.server, self.port)
        deferred = endpoint.connect(MuckFactory("out", "in"))
        reactor.run()
        sys.exit(0)