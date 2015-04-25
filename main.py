#!/usr/bin/env python

from pytun import TunTapDevice, IFF_TAP
from binascii import hexlify

import struct


def ip_checksum(ip_header, size):

    cksum = 0
    pointer = 0

    # The main loop adds up each set of 2 bytes. They are first converted to strings and then concatenated
    # together, converted to integers, and then added to the sum.
    while size > 1:
        cksum += int((ip_header[pointer] + ip_header[pointer + 1]), 16)
        size -= 2
        pointer += 2
    if size:  # This accounts for a situation where the header is odd
        cksum += ip_header[pointer]

    cksum = (cksum >> 16) + (cksum & 0xffff)
    cksum += (cksum >> 16)

    return (~cksum) & 0xFFFF


def shortToBytes(short):
    high = (short & 0xff00) >> 8
    low = (short & 0x00ff)
    return chr(high) + chr(low)

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
            ip_header = new_buf[18:38]
            checksum = ip_checksum([format(ord(c), "x")
                                    for c in ip_header], 20)

            print hex(checksum)
            final_buf = new_buf[:28] + shortToBytes(checksum) + new_buf[30:]
            print 'new', hexlify(final_buf)
            print
            tap.write(final_buf)
            # TODO encrypt buf
            # TODO send to wlan0
            # TODO enable routing
        except KeyboardInterrupt:
            tap.close()
