#!/bin/bash

ip tuntap add mode tap dev ipsec-tap
ip link set dev ipsec-tap up
ip addr add 192.168.53.53 dev ipsec-tap
ip route add 192.168.10.174/32 dev ipsec-tap # Valeri @ studentpub
