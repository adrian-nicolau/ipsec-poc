#!/usr/bin/env python

from pytun import TunTapDevice
from binascii import hexlify

if __name__ == '__main__':
    tun = TunTapDevice(name='ipsec-tun')
    tun.up()
    tun.persist(True)

    while True:
        try:
            buf = tun.read(tun.mtu)
            print hexlify(buf[4:])
            IPpayload = buf[4:]
            # TODO encrypt buf
            # TODO send to wlan0
            # TODO enable routing
        except KeyboardInterrupt:
            tun.close()
