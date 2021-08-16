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
This file is intended to generate a list with all the host IPs in the LAN.

It is very OS dependant, so for now it only works on Linux.
"""

import socket
import netifaces
import ipaddress

from urllib.request import urlopen

# Getting repo path
from pathlib import Path
REPO_PATH = str(Path(__file__).parent.parent.absolute()) + "/"

# IP List file path
IP_LIST_PATH = REPO_PATH + 'db/ip_list.txt'
AUTOREPLACE_TXT = '# AUTOREPLACE #'

# In windows we may not be able to find the netmask, we will use the default one.
DEFAULT_NETMASK = '255.255.255.0'

def is_internet_on() -> bool:
    """
    Returns wether this script has internet connection or not.
    """
    try:
        urlopen('https://www.google.com/', timeout=5)
        return True
    except: 
        return False

def get_network_info() -> tuple:
    """
    Returns the ip pattern and the netmask of the current computer. If unable to find, it returns the default values.
    """
    # Getting LAN IP adress
    # A big part of the code here has been extracted from the question of this man.
    # https://stackoverflow.com/questions/41625274/extracting-subnet-mask-from-my-computer-python
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    lan_ip = s.getsockname()[0]
    s.close()

    # Checking network interfaces for a convincing Gateway and Mask
    for i in netifaces.interfaces():
        try:

            pc_ip = netifaces.ifaddresses(i)[netifaces.AF_INET][0]['addr']
            mask = netifaces.ifaddresses(i)[netifaces.AF_INET][0]['netmask']
            gateway = netifaces.gateways()['default'][netifaces.AF_INET][0]

            if pc_ip == lan_ip:
                break
        except:
            pass

    else:
        # mask and gateway not found, using default values
        mask = DEFAULT_NETMASK
        gateway = str(lan_ip)

    # If invalid netmask we put the default netmask
    if mask == '255.255.255.255': mask = DEFAULT_NETMASK

    # Now we need to set to zero the host ports.
    splitted_ip = gateway.split('.')
    splitted_mask = mask.split('.')

    for i in range(4):
        if splitted_mask[i] == '0':
            splitted_ip[i] = '0'
        elif splitted_mask[i] != '255':
            num = bin(int(splitted_ip[i]))[2:]
            pat = bin(int(splitted_mask[i]))[2:]

            # Adding 0s if needed
            while len(num) < 8:
                num = '0' + num
            while len(pat) < 8:
                pat = '0' + pat

            for i in range(8):
                if pat[i] == '0':
                    num = num[:i] + '0' + num[i+1:]

            splitted_ip[i] = str(int(num, 2))


    correct_ip = '.'.join(splitted_ip)
    return correct_ip, mask


def generate_ip_list_file():
    """
    It auto-generates the ip_list.txt file
    """
    gip, mask = get_network_info()
    ips = ipaddress.IPv4Network(f"{gip}/{mask}")

    file_output = "\n".join([str(ip) for ip in ips])

    with open(IP_LIST_PATH, 'w') as f:
        f.write(file_output)

def need_to_generate_ip_file():
    """
    Returns wether the first line of the `IP_LIST_PATH`
    is `AUTOREPLACE_TXT`, and so, the file needs to be
    generated.
    """

    with open(IP_LIST_PATH, 'r') as f:
        return f.readline() == AUTOREPLACE_TXT + '\n'

# Debug
if __name__ == "__main__":
    if need_to_generate_ip_file(): generate_ip_list_file()