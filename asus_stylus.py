#!/usr/bin/env python3

import importlib
import logging
import os
import re
import sys
import signal
import multiprocessing
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
styluses: Optional[list[str]] = []
device_ids: Optional[list[str]] = []

tries = 5
styluses_name = []

# Look into the devices file
while tries > 0:

    stylus_detection_status = 0

    with open('/proc/bus/input/devices', 'r') as devices_list_file:
        lines = devices_list_file.readlines()
        for line in lines:

            # Look for the stylus
            if stylus_detection_status == 0 and "Stylus" in line:
                stylus_detection_status = 1
                name = line.strip().split('"')[1]
                styluses_name.append(f"{name} asus-stylus-driver")
                log.debug('Detect stylus from %s', line.strip())

            # Found stylus, now searching for ids
            if stylus_detection_status == 1:
                if "S: " in line:
                    # search device id
                    stylus_id = re.sub(r".*i2c-(\d+)/.*$", r'\1', line).replace("\n", "")
                    device_ids.append(stylus_id)
                    log.debug('Set stylus device id %s from %s', stylus_id, line.strip())

                if "H: " in line:
                    stylus_id = line.split("event")[1].split(" ")[0]
                    styluses.append(stylus_id)
                    log.debug('Set stylus id %s from %s', stylus_id, line.strip())
                    stylus_detection_status = 0

    # Stylus was found on at least one device
    if len(styluses) > 0:
        stylus_detection_status = 2;

    # Stylus was not detected?
    if stylus_detection_status != 2:
        tries -= 1
        if tries == 0:
            if stylus_detection_status != 2:
                log.error("Can't find stylus (code: %s)", stylus_detection_status)
            for device_id in device_ids:
                if stylus_detection_status == 2 and not device_id.isnumeric():
                    log.error("Can't find device id")
            sys.exit(1)
    else:
        break


# Start monitoring the stylus
stylus_devices = []
for stylus in styluses:
    fd = open('/dev/input/event' + str(stylus), 'rb')
    stylus_devices.append(Device(fd))


# Create a new device
class StylusInterface():
    def __init__(self, stylus, name):
        self.stylus = stylus
        self.stylus.name = name
        
        self.device = Device()
        self.device.name = name
        for key_mapping in layout.keys:
            self.device.enable(key_mapping[2])
        self.device.enable(EV_SYN.SYN_REPORT)
        self.device.enable(EV_MSC.MSC_SCAN)
        self.udev = self.device.create_uinput_device()


stylus_interfaces = []
for i in range(len(stylus_devices)):
    stylus_interfaces.append(StylusInterface(stylus_devices[i], styluses_name[i]))


def pressed_bound_key(event, key_mapping, stylus):
    key_events = []
    key_events.append(InputEvent(EV_MSC.MSC_SCAN, key_mapping[1]))
    for key in key_mapping[2:]:
        key_events.append(InputEvent(key, event.value))

    sync_event = [
        InputEvent(EV_SYN.SYN_REPORT, 0)
    ]
    key_events = key_events + sync_event

    try:
        stylus.udev.send_events(key_events)
        if event.value:
            log.info("Caught key: ")
            log.info(key_mapping[0])
            log.info("Pressed key: ")
            log.info(key_mapping[2])
        else:
            log.info("Caught key: ")
            log.info(key_mapping[0])
            log.info("Unpressed key: ")
            log.info(key_mapping[2])
    except OSError as event:
        log.error("Cannot send event, %s", event)


# Device process behavior
def handle_interface_events(interface):
    while True:
        # If stylus sends something
        for event in interface.stylus.events():
            log.debug(event)

            # Is this event binded to key?
            for key_mapping in layout.keys:
                if event.matches(key_mapping[0]):
                    pressed_bound_key(event, key_mapping, interface)

# Create and start processes, each device get its own process
processes = []
for stylus_interface in stylus_interfaces:
    log.info(f"Started stylus {stylus_interface.stylus.name}")
    process = multiprocessing.Process(target=handle_interface_events, args=(stylus_interface,), name=stylus_interface.stylus.name)
    process.start()
    processes.append(process)

# Clean before exiting
def sigint_handler(sig, frame):
    log.debug("Received SIGINT, stopping now...")
    for process in processes:
        process.kill()
        log.debug("Device %s closed.", process.name)
    log.debug("Threads dead, now exiting. Goodbye.")
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

signal.pause()
