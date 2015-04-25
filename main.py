#!/usr/bin/python

from pytun import TunTapDevice

if __name__ == '__main__':
	tun = TunTapDevice(name='ipsec-tun')
	tun.up()

	while True:
		buf = tun.read(tun.mtu)
		print buf
