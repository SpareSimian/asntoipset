# asntoipset

Convert a list of records from iptoasn.com to a firewalld ipset XML file.

Download a database in tab-delimited format from https://iptoasn.com/,
uncompress, filter with grep, and feed to this script to generate a
file to place in /etc/firewalld/ipsets for use in firewall rules.

Example:
```
wget -q -O - https://iptoasn.com/data/ip2asn-v4.tsv.gz | \
    gunzip | grep -v "DIGITALOCEAN" | ./asntoipset.py > /etc/firewalld/ipsets/DigitalOcean.xml
```

To match country codes to block all but addresses in the US, try the
following as your filter. (Include None to include non-routable blocks
such as your LAN or you might lock yourself out of your server.)
```
grep -v -P "\t(US|None)\t"
```

Requires the netaddr package to extract CIDR lists from a range of IP addresses.
Requires ElementTree from Python > 3.7 that includes the indent method.
