#!/bin/bash

ip tuntap add mode tap dev ipsec-tap
ip link set dev ipsec-tap up
ip addr add 192.168.42.42 dev ipsec-tap
ip route add 42.42.42.42/32 dev ipsec-tap
# Add arp static entry for 42.42.42.42 with the destination MAC for the IP address in main.py.
