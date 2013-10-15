#!/usr/bin/env python
# encoding: utf-8
"""
$FILE

Created by bunnyman on 2013/10/14.
Copyright (c) 2013 Bunni.biz. All rights reserved.
"""

import sys
import os


def main():
	pass


if __name__ == '__main__':
	main()



__author__ = 'bunnyman'


class SessionLogger(object):
    """
    Making this a class will allow us to extend this with "plugins" later
    """
    def __init__(self, logfile):
        self.file = logfile

    def log(self, message):
        """Write a message to the file."""
        self.file.write("{}\n".format(message))
        self.file.flush()

    def close(self):
        self.file.close()