#!/usr/bin/env python
# encoding: utf-8
"""


Created by bunnyman on 2013/10/09.
Copyright (c) 2013 Bunni.biz. All rights reserved.
"""

import unittest
import mm


class TestMM(unittest.TestCase):
    def setUp(self):
        self.testArgs = dict(name="test", server="tapestries.fur.com", port=2069)

    def test_setupdestroy(self):
        tester = mm.MuMe(self.testArgs)





if __name__ == '__main__':
    unittest.main()

__author__ = 'bunnyman'
