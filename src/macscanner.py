#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#################################################################################
# MIT License

# Copyright (c) 2021 Eric Roy

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#################################################################################

"""
This module scans for mac addresses.
"""

from subprocess import PIPE, STDOUT, run
from scapy.all import getmacbyip
import ipmaker
from ipmaker import IP_LIST_PATH

# TODO : Add windows support

SCAN_COMMAND = f'fping -f {IP_LIST_PATH} -C 1 -q'

if ipmaker.need_to_generate_ip_file(): ipmaker.generate_ip_list_file()

output = run(SCAN_COMMAND.split(), stdout=PIPE, stderr=STDOUT).stdout.decode('utf-8')
maclist = []

for ans in output.split('\n'):
    if '-' not in ans and ans != "":
        ip = ans.split()[0]
        mac = getmacbyip(ip)

        print(ip, mac)