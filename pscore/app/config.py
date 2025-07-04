# -*- coding: utf-8 -*-
"""
eated on Thr Mar 8 17:28:15 2018
@author: Amey Bhadkamkar
"""

import os


# default config
class Config():

    def __init__(self):
        # self.logger = logger
        # global logger
        global UI_port_no
        global UI_ip_address

    def configuration(self):
        UI_ip_address = 'localhost'
        PScore_ip_address = 'localhost'
        machine_id = '5ab488d4e5840e2c1abe3c3b'
        UI_port_no = '3000'

        return (UI_ip_address, UI_port_no, machine_id, PScore_ip_address)
