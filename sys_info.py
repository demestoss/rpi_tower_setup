#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014-2022 Richard Hull and contributors
# See LICENSE.rst for details.
# PYTHON_ARGCOMPLETE_OK

"""
Display basic system information.

Needs psutil (+ dependencies) installed::

  $ sudo apt-get install python-dev
  $ sudo -H pip install psutil
"""

import os
import sys
import time
import socket
import subprocess as sp
from pathlib import Path
from datetime import datetime

if os.name != 'posix':
    sys.exit(f'{os.name} platform is not supported')

from demo_opts import get_device
from luma.core.render import canvas
from PIL import ImageFont

try:
    import psutil
except ImportError:
    print("The psutil library was not found. Run 'sudo -H pip install psutil' to install it.")
    sys.exit()


# TODO: custom font bitmaps for up/down arrows
# TODO: Load histogram


def bytes2human(n):
    """
    >>> bytes2human(10000)
    '9K'
    >>> bytes2human(100001221)
    '95M'
    """
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = int(float(n) / prefix[s])
            return '%s%s' % (value, s)
    return f"{n}B"


def cpu_usage():
    # load average, uptime
    uptime = datetime.now() - datetime.fromtimestamp(psutil.boot_time())
    av1, av2, av3 = os.getloadavg()
    return "Ld:%.1f %.1f %.1f Up: %s" \
        % (av1, av2, av3, str(uptime).split('.')[0])


def mem_usage():
    usage = psutil.virtual_memory()
    return "Mem: %s %.0f%%" \
        % (bytes2human(usage.used), 100 - usage.percent)


def disk_usage(dir):
    usage = psutil.disk_usage(dir)
    return "SD:  %s %.0f%%" \
        % (bytes2human(usage.used), usage.percent)


def network(iface):
    stat = psutil.net_io_counters(pernic=True)[iface]
    return "%s: Tx%s, Rx%s" % \
           (iface, bytes2human(stat.bytes_sent), bytes2human(stat.bytes_recv))

def ip_address(s):
    ip = s.getsockname()[0]
    return "IP:  %s" % (ip)

def get_temp():
    temp = sp.getoutput("vcgencmd measure_temp | egrep -o '[0-9]*\.[0-9]*'")
    return "Temp: %s" % (float(temp))


def stats(device, s):
    # use custom font
    font_path = str(Path(__file__).resolve().parent.joinpath('fonts', 'C&C Red Alert [INET].ttf'))
    font2 = ImageFont.truetype(font_path, 12)

    with canvas(device) as draw:
        draw.text((0, 0), cpu_usage(), font=font2, fill="white")
        if device.height >= 32:
            draw.text((0, 14), mem_usage(), font=font2, fill="white")

        if device.height >= 64:
            draw.text((0, 26), disk_usage('/'), font=font2, fill="white")
            draw.text((0, 38), get_temp(), font=font2, fill="white")
           # try:
           #     draw.text((0, 38), network('wlan0'), font=font2, fill="white")
           # except KeyError:
                # no wifi enabled/available
           #      pass
            draw.text((0, 50), ip_address(s), font=font2, fill="white")


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    try:
        while True:
            stats(device, s)
            time.sleep(5)

    except KeyboardInterrupt:
        pass
    s.close()


if __name__ == "__main__":
    try:
        device = get_device()
        main()
    except KeyboardInterrupt:
        pass
