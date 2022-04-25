#!/usr/bin/env python3

import logging
import os
import re
import sys
from fcntl import F_SETFL, fcntl
from time import sleep
from typing import Optional

from libevdev import EV_KEY, EV_SYN, EV_MSC, Device, InputEvent

# Setup logging
# LOG=DEBUG sudo -E ./asus-stylus-numpad-driver  # all messages
# LOG=ERROR sudo -E ./asus-stylus-numpad-driver  # only error messages
logging.basicConfig()
log = logging.getLogger('Pen')
log.setLevel(os.environ.get('LOG', 'INFO'))


# Figure out device from devices file
stylus: Optional[str] = None
device_id: Optional[str] = None

tries = 5

# Look into the devices file
while tries > 0:

    #keyboard_detected = 0
    stylus_detected = 0

    with open('/proc/bus/input/devices', 'r') as f:
        lines = f.readlines()
        for line in lines:

            # Look for the stylus
            if stylus_detected == 0 and ("Name=\"ELAN" in line) and "Stylus" in line:
                stylus_detected = 1
                log.debug('Detect stylus from %s', line.strip())

            if stylus_detected == 1:
                if "S: " in line:
                    # search device id
                    device_id=re.sub(r".*i2c-(\d+)/.*$", r'\1', line).replace("\n", "")
                    log.debug('Set stylus device id %s from %s', device_id, line.strip())

                if "H: " in line:
                    stylus = line.split("event")[1]
                    stylus = stylus.split(" ")[0]
                    stylus_detected = 2
                    log.debug('Set stylus id %s from %s', stylus, line.strip())

            # Stop looking if stylus have been found
            if stylus_detected == 2:
                break

    if stylus_detected != 2:
        tries -= 1
        if tries == 0:
            if stylus_detected != 2:
                log.error("Can't find stylus (code: %s)", stylus_detected)
            if stylus_detected == 2 and not device_id.isnumeric():
                log.error("Can't find device id")
            sys.exit(1)
    else:
        break


# Start monitoring the stylus

fd_t = open('/dev/input/event' + str(stylus), 'rb')
fcntl(fd_t, F_SETFL, os.O_NONBLOCK)
d_t = Device(fd_t)


# Create a new device to send right clickss

dev = Device()
dev.name = "Asus Stylus"
dev.enable(EV_KEY.BTN_RIGHT)
dev.enable(EV_KEY.BTN_MIDDLE)
dev.enable(EV_SYN.SYN_REPORT)
dev.enable(EV_MSC.MSC_SCAN)

udev = dev.create_uinput_device()

while True:

    # If stylus sends something
    for e in d_t.events():


        # Pen's distance tracker:
        #
        # 1 is send when was entered ZONE closer to laptop screen where is stylus active
        # 0 is send when was entered ZONE where is stylus disabled
        if (
            e.matches(EV_KEY.BTN_TOOL_PEN)
        ):
            log.debug(e)

        # Pen's first button (closer to spike) - mapped as middle click:
        #
        # 0 then immediately 1
        elif (
            e.matches(EV_KEY.BTN_TOOL_RUBBER)
        ):

            if e.value == 1:
                events = [
                    InputEvent(EV_MSC.MSC_SCAN, 589827),
                    InputEvent(EV_KEY.BTN_MIDDLE, e.value),
                    InputEvent(EV_SYN.SYN_REPORT, 0),
                ]
            else:
                events = [
                    InputEvent(EV_MSC.MSC_SCAN, 589827),
                    InputEvent(EV_KEY.BTN_MIDDLE, e.value),
                    InputEvent(EV_SYN.SYN_REPORT, 0),
                ]

            try:
                udev.send_events(events)
            except OSError as err:
                log.warning("Cannot send event, %s", err)

            log.debug(e)

        # Pen's second button - mapped as right click:
        #
        # 0 then immediately 1
        elif (
            e.matches(EV_KEY.BTN_STYLUS)
        ):

            if e.value == 1:
                events = [
                    InputEvent(EV_MSC.MSC_SCAN, 589826),
                    InputEvent(EV_KEY.BTN_RIGHT, e.value),
                    InputEvent(EV_SYN.SYN_REPORT, 0),
                ]
            else:
                events = [
                    InputEvent(EV_MSC.MSC_SCAN, 589826),
                    InputEvent(EV_KEY.BTN_RIGHT, e.value),
                    InputEvent(EV_SYN.SYN_REPORT, 0),
                ]

            try:
                udev.send_events(events)
            except OSError as err:
                log.warning("Cannot send event, %s", err)
        else:
            log.debug(e)

    sleep(0.1)
