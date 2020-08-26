#!/usr/bin/env python
import sys, os
import struct

from scapy.layers.inet import _IPOption_HDR, IPOption, IP, UDP,TCP
from scapy.all import *
TYPE_MYTUNNEL = 0x1212
TYPE_IPV4 = 0x0800


def get_if():
    ifs = get_if_list()
    iface = None
    for i in get_if_list():
        if "eth0" in i:
            iface = i
            break;
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


def handle_pkt(pkt):
    path = "/home/hcc/PycharmProjects/fattree/%s.csv" % (''.join(sys.argv[1]))
    if IP in pkt:
        print("got a packet")
        with open(path, "a+") as f:
            seq=[str(pkt.options[0].swtraces[0].swid)," ",str(pkt.options[0].swtraces[0].qlenth)," ",str(pkt.options[0].swtraces[0].packetdt)," ",
                 str(pkt.options[0].swtraces[1].swid)," ",str(pkt.options[0].swtraces[1].qlenth)," ",str(pkt.options[0].swtraces[1].packetdt)," ",
                 str(pkt.options[0].swtraces[2].swid)," ",str(pkt.options[0].swtraces[2].qlenth)," ",str(pkt.options[0].swtraces[2].packetdt)," ",
                 str(pkt.load,'utf-8')[0],"\n"]
            f.writelines(seq)
    pkt.show2()
    sys.stdout.flush()



def main():
    iface = 'eth0'
    sniff(filter="tcp",iface=iface,
          prn=lambda x: handle_pkt(x))
    

if __name__ == '__main__':
    main()
