#!/usr/bin/env python
# encoding: utf-8
"""


Created by bunnyman on 2013/10/09.
Copyright (c) 2013 Bunni.biz. All rights reserved.
"""
from datetime import datetime
import os
import shutil
import unittest
import sys
from twisted.internet.endpoints import TCP4ClientEndpoint
import mm


class TestMM(unittest.TestCase):
    def setUp(self):
        self.test_name = "test-connection"
        self.test_server = "tapestries.fur.com"
        self.test_port = 2069

    def tearDown(self):
        if os.path.basename(os.getcwd()) == self.test_name:
            os.chdir("..")
        try:
            shutil.rmtree(self.test_name)
        except OSError:
            pass

    def test_setupdestroy_files(self):
        tester = mm.MuMe(self.test_name, self.test_server, self.test_port)
        tester.enter_directory()
        self.assertEqual(os.path.basename(os.getcwd()), self.test_name)
        tester.make_in()
        self.assertTrue(os.path.exists("in"))
        with open("out", 'w') as outfile:
            outfile.write("testing stufffffff")
        mm.cleanup_files(self.test_name, True, True)
        self.assertTrue(os.path.isfile(datetime.now().strftime("%Y-%m-%dT%H%M%S")))
        self.assertTrue(os.path.isfile("out"))
        mm.cleanup_files(self.test_name, False, False)
        self.assertFalse(os.path.exists("in"))
        self.assertFalse(os.path.isfile("out"))

    def test__standard_session(self):
        outfile = sys.stdout
        from twisted.internet import reactor
        endpoint = TCP4ClientEndpoint(reactor, self.test_server, self.test_port)
        muck_factory = mm.MuckFactory(outfile)
        muck_factory.protocol = mm.MuckSession
        d = endpoint.connect(muck_factory)

        def test_protocol(p):
            reactor.callLater(3, p.write, "WHO")
            reactor.callLater(5, p.close)

        d.addCallback(test_protocol)
        reactor.run()


if __name__ == '__main__':
    unittest.main()

__author__ = 'bunnyman'
