from libevdev import EV_KEY

keys = [ 
    [
        EV_KEY.BTN_TOOL_RUBBER, # listen
        589827, # MSC_SCAN code of BTN_MIDDLE
        EV_KEY.BTN_MIDDLE # pressed & unpressed key
    ],
    [
        EV_KEY.BTN_STYLUS, # listen
        589826, # MSC_SCAN code of BTN_RIGHT
        EV_KEY.BTN_RIGHT # pressed & unpressed key
    ]
]