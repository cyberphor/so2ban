#!/usr/bin/python

from scapy.all import *

ether = Ether()
ether.src = '00:0a:0b:0c:0d:11'
ether.dst = '00:0a:0b:0c:0d:22'
ip = IP()
ip.src = '192.168.1.69'
ip.dst = '8.8.8.8'
udp = UDP()
udp.sport = 4321
udp.dport = 53
dns = DNS()
dns.rd = 1
dns.qd = DNSQR()
dns.qd.qname = input('[+] Test Bro with this IOC: ')
packet = ether/ip/udp/dns
packet.show()

for i in range(1,10):
    wrpcap('traffic.pcap', packet, append=True)
