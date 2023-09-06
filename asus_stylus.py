#!/usr/bin/env python3

import importlib
import logging
import os
import re
import sys
from threading import Thread
from typing import Optional

from libevdev import EV_SYN, EV_MSC, Device, InputEvent

# Setup logging
# LOG=DEBUG sudo -E ./asus_stylus.py  # all messages
# LOG=ERROR sudo -E ./asus_stylus.py  # only error messages
logging.basicConfig()
log = logging.getLogger('Pen')
log.setLevel(os.environ.get('LOG', 'INFO'))

layout_name = 'SA201H'
if len(sys.argv) > 1:
    layout_name = sys.argv[1]

layout = importlib.import_module('stylus_layouts.'+ layout_name)

# Figure out device from devices file
stylus: Optional[list[str]] = []
device_id: Optional[list[str]] = []

tries = 5

# Look into the devices file
while tries > 0:

    stylus_detected = 0

    with open('/proc/bus/input/devices', 'r') as f:
        lines = f.readlines()
        for line in lines:

            # Look for the stylus
            if stylus_detected == 0 and "Stylus" in line:
                stylus_detected = 1
                log.debug('Detect stylus from %s', line.strip())

            if stylus_detected == 1:
                if "S: " in line:
                    # search device id
                    device_id.append(re.sub(r".*i2c-(\d+)/.*$", r'\1', line).replace("\n", ""))
                    log.debug('Set stylus device id %s from %s', device_id, line.strip())

                if "H: " in line:
                    stylus.append(line.split("event")[1]
                                      .split(" ")[0])
                    log.debug('Set stylus id %s from %s', stylus, line.strip())
                    stylus_detected = 0

            # # Stop looking if stylus have been found
            # if stylus_detected == 2:
            #     break

    print(f"{stylus = }")
    if len(stylus) > 0:
        stylus_detected = 2;

    if stylus_detected != 2:
        tries -= 1
        if tries == 0:
            if stylus_detected != 2:
                log.error("Can't find stylus (code: %s)", stylus_detected)
            for device_id_p in device_id:
                if stylus_detected == 2 and not device_id_p.isnumeric():
                    log.error("Can't find device id")
            sys.exit(1)
    else:
        break


# Start monitoring the stylus
fd_t = []
d_t = []
for pen in stylus:
    fd_t.append(open('/dev/input/event' + str(pen), 'rb'))
    for fd_t_p in fd_t:
        d_t.append(Device(fd_t_p))


# Create a new device
dev = []
for pen in stylus:
    dev.append(Device())

for device in dev:
    device.name = "Asus Stylus"
    for key_mapping in layout.keys:
        device.enable(key_mapping[2])
    device.enable(EV_SYN.SYN_REPORT)
    device.enable(EV_MSC.MSC_SCAN)

    udev = device.create_uinput_device()

def pressed_bound_key(e, key_mapping):
    key_events = []
    key_events.append(InputEvent(EV_MSC.MSC_SCAN, key_mapping[1]))
    for key in key_mapping[2:]:
        key_events.append(InputEvent(key, e.value))

    sync_event = [
        InputEvent(EV_SYN.SYN_REPORT, 0)
    ]    
    key_events = key_events + sync_event

    try:
        udev.send_events(key_events)
        if e.value:
            log.info("Caught key: ")
            log.info(key_mapping[0])
            log.info("Pressed key: ")
            log.info(key_mapping[2])
        else:
            log.info("Caught key: ")
            log.info(key_mapping[0])
            log.info("Unpressed key: ")
            log.info(key_mapping[2])
    except OSError as e:
        log.error("Cannot send event, %s", e)


def handle_stylus(d_t):
    while True:

        # If stylus sends something
        for e in d_t.events():
            log.debug(e)

            # Is this event binded to key?
            for key_mapping in layout.keys:
                if e.matches(key_mapping[0]):
                    pressed_bound_key(e, key_mapping)

for d_t_p in d_t:
    log.info(f"Started stylus {d_t_p}")
    Thread(target=handle_stylus, args=(d_t_p,)).start()
