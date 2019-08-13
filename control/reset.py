#!/usr/bin/env python
#
# Copyright (c) 2019, CESAR. All rights reserved.
#
# SPDX-License-Identifier: BSD 3-Clause

import logging
import os
import json

from pkg_resources import resource_string
from mongo import MongoConn
from rabbitmq import RabbitMQConn
from connman import remove_wifi_services

RESET_SETTINGS_FILE = 'resetSettings.json'

def createReset():
    """
        A factory to create an instance of Reset
    """
    json_file = resource_string(__name__, RESET_SETTINGS_FILE)
    settings = json.loads(json_file)
    mongodb_settings = settings.get('mongodb')
    mongo_conn = MongoConn(mongodb_settings.get('host'),
                            mongodb_settings.get('port'))
    rabbitmq_conn = RabbitMQConn()

    return Reset(mongo_conn, rabbitmq_conn)

class Reset():
    """
    Performs reset functions on KNoT Gateway
    """
    def __init__(self, mongo_conn, rabbitmq_conn):
        self._rabbitmq_conn = rabbitmq_conn
        self._mongo_conn = mongo_conn

    def stop_process(self, process):
        logging.info('Stopping process: ' + process)
        stop = '/etc/knot/stop.sh '
        os.system(stop + process)

    def stop_processes(self):
        processes = ['knot-fog', 'knot-connector']
        for proc in processes:
            self.stop_process(proc)

    def factory_reset(self):
        # stop Daemons
        self.stop_processes()

        # clear RabbitMQ
        self._rabbitmq_conn.connect()
        self._rabbitmq_conn.remove_all_queues()
        self._rabbitmq_conn.close()

        # clear MongoDB
        self._mongo_conn.connect()
        self._mongo_conn.drop_all_db()
        self._mongo_conn.close()

        # clear ConnMan services
        remove_wifi_services()

        # reboot
        os.system('reboot')
