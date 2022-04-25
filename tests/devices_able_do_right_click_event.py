#!/usr/bin/env python3

import libevdev

number: int = 2
device: bool = False

while(not device):
    fd = open('/dev/input/event' + str(number), 'rb')
    d = libevdev.Device(fd)
    if not d.has(libevdev.EV_KEY.BTN_RIGHT): # or number == 6 or number == 24: # skip some devices via numbers
        number = number + 1
        continue
    else:
        device = True


for e in d.events():
    print(e)