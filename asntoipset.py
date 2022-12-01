#!/usr/bin/env python3
""" Convert a list of records from iptoasn.com to a firewalld ipset XML file.

Download a database in tab-delimited format from https://iptoasn.com/,
uncompress, filter with grep, and feed to this script to generate a
file to place in /etc/firewalld/ipsets for use in firewall rules.

Example:

wget -q -O - https://iptoasn.com/data/ip2asn-v4.tsv.gz | \
    gunzip | grep -v "DIGITALOCEAN" | ./asntoipset.py > /etc/firewalld/ipsets/DigitalOcean.xml

To match country codes to block all but addresses in the US, try the
following as your filter. (Include None to include non-routable blocks
such as your LAN or you might lock yourself out of your server.)

grep -v -P "\t(US|None)\t"

Requires the netaddr package to extract CIDR lists from a range of IP addresses.
Requires ElementTree from Python > 3.7 that includes the indent method.
"""

import sys

if (len(sys.argv) == 1):
    fobj = sys.stdin
else:
    fobj = open(sys.argv[-1], 'r') # command-line argument

import csv

reader = csv.DictReader(fobj, ["range_start", "range_end", "AS_number", "country_code", "AS_description"], delimiter="\t")
records = []
for row in reader:
    records.append(dict(row))

from netaddr import IPRange

networks = []
for record in records:
    range = IPRange(record["range_start"], record["range_end"])
    networks.extend(range.cidrs());

import xml.etree.ElementTree as ET

ipset = ET.Element("ipset", type="hash:net")
ET.SubElement(ipset, "option", name="maxelem", value=str(len(networks)))
ET.SubElement(ipset, "option", name="family", value="inet")
for network in networks:
    ET.SubElement(ipset, "entry").text = str(network)

tree = ET.ElementTree(ipset)
ET.indent(tree)
# standard streams are "text" and utf-8 is binary, so switch stdout
# to binary output mode with detach method
sys.stdout = sys.stdout.detach()
tree.write(sys.stdout, encoding="utf-8", xml_declaration=True)
