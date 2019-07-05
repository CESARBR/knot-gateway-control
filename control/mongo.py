#!/usr/bin/env python
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: BSD 3-Clause

from pymongo import MongoClient
from pymongo import errors

import logging

class Singleton(type):
    """
    Singleton class to guarantee that a single instance will be used for
    its inhereted classes
    """
    __instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls.__instances:
            cls.__instances[cls] = super(Singleton,
                                         cls).__call__(*args, **kwargs)
        return cls.__instances[cls]

class MongoConn(object):
    """
    MongoDB client used to manager databases
    """
    __metaclass__ = Singleton

    def __init__(self, host, port = None):
        self.host = host
        self.port = port

    def connect(self):
        self.client = MongoClient(self.host, self.port)

    def drop_db(self, database):
        self.client.drop_database(database)

    def drop_all_db(self):
        for db in self.client.list_database_names():
            self.drop_db(db)

    def close(self):
        self.client.close()
