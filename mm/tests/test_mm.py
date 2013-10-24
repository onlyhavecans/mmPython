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

from twisted.internet.endpoints import TCP4ClientEndpoint, SSL4ClientEndpoint
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

    def test_standard_session(self):
        outfile = "test_out"
        from twisted.internet import reactor
        endpoint = TCP4ClientEndpoint(reactor, self.test_server, self.test_port)
        d = endpoint.connect(mm.MuckFactory(outfile))

        def test_protocol(p):
            tn = p.protocol
            reactor.callLater(2, tn.write, "WHO")
            reactor.callLater(2.5, tn.write, "QUIT")
            reactor.callLater(3, tn.close)
            reactor.callLater(3.5, reactor.stop)

        d.addCallback(test_protocol)
        reactor.run()
        self.assertTrue(os.path.exists(outfile))
        self.assertTrue(os.path.getsize(outfile) > 500)
        os.unlink(outfile)


if __name__ == '__main__':
    unittest.main()

