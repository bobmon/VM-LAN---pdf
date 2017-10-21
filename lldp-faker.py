#!/usr/bin/env python3
# generate fake LLDP multicasts
# 2017-08-11 -bob,mon.

import scapy.layers.l2, scapy.sendrecv
import time

chassis = bytearray(7)
chassis[0:3] = (0x02,0x06,0x07)
chassis[3:] = str.encode('fakey', 'utf-8')

sysname = bytearray(7)
sysname[0:2] = (0x0a,0x05)
sysname[2:] = str.encode('Lies!', 'utf-8')

sysdesc = bytearray(12)
sysdesc[0:2] = (0x0c,0x0a)
sysdesc[2:] = str.encode('MS-DOS 1.0', 'utf-8')

# fake IP address 17.17.17.17
mgmt_addr = bytearray( (0x10,0x0c, 0x05,0x01, 0x11,0x11,0x11,0x11, 0x02, 0x00,0x00,0x00,0x0b, 0x00) )

# fake MAC address 00:01:02:ff:fe:fd
fake_MAC = '00:01:02:ff:fe:fd'
portID = bytearray( (0x04,0x07,0x03, 0x00,0x01,0x02,0xff,0xfe,0xfd) )

TTL = bytearray( (0x06,0x02, 0x00,0x78) )
end = bytearray( (0x00, 0x00) )
payload = bytes(chassis + portID + TTL + sysname + sysdesc + mgmt_addr + end) 

mac_lldp_multicast = '01:80:c2:00:00:0e'
eth = scapy.layers.l2.Ether(src=fake_MAC, dst=mac_lldp_multicast, type=0x88cc)
frame = eth / scapy.layers.l2.Raw(load=bytes(payload))	# no Padding() needed

while True:
    scapy.sendrecv.sendp(frame)
    time.sleep(30)
#--------
