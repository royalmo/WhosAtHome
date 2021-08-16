from subprocess import PIPE, STDOUT, run
from scapy.all import getmacbyip

# TODO : Add windows support

cmd = 'fping -f ips.txt -C 1 -q'
#TODO : Try this without the shell=True
output = run(cmd.split(), stdout=PIPE, stderr=STDOUT, shell=True).stdout.decode('utf-8')

import netifaces

netifaces.gateways()

for ans in output:
    if '-' not in ans:
        ip = ans.split()[0]
        mac = getmacbyip(ip)

        print(ip, mac)