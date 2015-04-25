#!/bin/bash

ip tuntap add mode tun dev ipsec-tun
ip link set dev ipsec-tun up
ip addr add 192.168.42.42 dev ipsec-tun
ip route add 192.168.10.174/32 dev ipsec-tun # Valeri @ studentpub
