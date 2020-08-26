#!/usr/bin/env python

import argparse
import sys
import socket
import random
import struct,threading

from scapy.layers.inet import _IPOption_HDR, IPOption, IP, UDP, Ether,TCP
from scapy.all import *
from time import sleep

TYPE_MYTUNNEL = 0x1212
TYPE_IPV4 = 0x0800


def get_if():
    ifs = get_if_list()
    iface = None
    for i in get_if_list():
        if "eth0" in i:
            iface = i
            break
    if not iface:
        print("Cannot find eth0 interface")
        exit(1)
    return iface


class SwitchTrace(Packet):
    fields_desc = [BitField("swid", 0, 16),
                   IntField("qlenth", 0),
                   BitField("packetdt", 0, 48)
                   ]

    def extract_padding(self, p):
        return "", p


class IPOption_MRI(IPOption):
    name = "MRI"
    option = 31
    fields_desc = [_IPOption_HDR,
                   FieldLenField("length", None, fmt="B",
                                 length_of="swtraces",
                                 adjust=lambda pkt, l: l * 2 + 4),
                   ShortField("count", 0),
                   PacketListField("swtraces",
                                   [],
                                   SwitchTrace,
                                   count_from=lambda pkt: (pkt.count * 1))]


def main():

    iface = get_if()

    pkt = Ether(src="08:00:00:00:01:01", dst="ff:ff:ff:ff:ff:ff") / IP(
        dst="10.0.2.2", options=IPOption_MRI(count=0,
                                       swtraces=[])) / TCP(
        dport=1234, sport=random.randint(49152,65535)) / "111111111111111111111111111111111111111111111111111111111111111111111111111111" \
                                  "111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111"

    pkt2 = Ether(src="08:00:00:00:01:01", dst="ff:ff:ff:ff:ff:ff") / IP(
        dst="10.0.2.2", options=IPOption_MRI(count=0,
                                       swtraces=[])) / TCP(
        dport=1234, sport=random.randint(49152,65535)) / "2222"
    #t=float(sys.argv[1])
    list_delta=[0.05,0.058,0.065,0.074,0.087,0.1,0.13]
    pkt.show2()
    try:
        for l in list_delta:
            sendp(pkt2)
            for i in range(500):
                sendp(pkt, iface=iface)
                sleep(l)
            sleep(10)
        sendp(pkt2)


    except KeyboardInterrupt:
        raise


if __name__ == '__main__':
    main()
