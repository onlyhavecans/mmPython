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
import mm
from mm.utils import cleanup_files


class TestMM(unittest.TestCase):
    def setUp(self):
        self.test_name = "test-connection"
        self.test_server = "tapestries.fur.com"
        self.test_port = 2069

    def tearDown(self):
        if os.path.basename(os.getcwd()) == self.test_name:
            os.chdir("..")
        shutil.rmtree(self.test_name)

    def test_setupdestroy_files(self):
        tester = mm.MuMe(self.test_name, self.test_server, self.test_port)
        tester.enter_directory()
        self.assertEqual(os.path.basename(os.getcwd()), self.test_name)
        tester.make_in()
        self.assertTrue(os.path.exists("in"))
        with open("out", 'w') as outfile:
            outfile.write("testing stufffffff")
        cleanup_files(self.test_name, True, True)
        self.assertTrue(os.path.isfile(datetime.now().strftime("%Y-%m-%dT%H%M%S")))
        self.assertTrue(os.path.isfile("out"))
        cleanup_files(self.test_name, False, False)
        self.assertFalse(os.path.exists("in"))
        self.assertFalse(os.path.isfile("out"))


if __name__ == '__main__':
    unittest.main()

__author__ = 'bunnyman'
