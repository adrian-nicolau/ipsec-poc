#!/usr/bin/env python

from pytun import TunTapDevice, IFF_TAP
from binascii import hexlify

import struct


if __name__ == '__main__':
    tap = TunTapDevice(name='ipsec-tap', flags=IFF_TAP)
    tap.up()
    tap.persist(True)

    while True:
        try:
            buf = tap.read(tap.mtu)
            print 'old', hexlify(buf)
            # Valeri @ studentpub
            new_addr = struct.pack('4B', 192, 168, 10, 174)
            new_buf = buf[:34] + new_addr + buf[38:]
            print 'new', hexlify(new_buf)
            print
            tap.write(new_buf)
            # TODO encrypt buf
            # TODO send to wlan0
            # TODO enable routing
        except KeyboardInterrupt:
            tap.close()
