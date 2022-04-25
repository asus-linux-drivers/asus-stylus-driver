# Asus stylus driver

Tested only with **ASUS-PEN-SA201H**.

## TODO:

- [x] (First button as middle click)
- [x] (Second button as right click)

<br/>

This python driver has been tested and works fine for these asus versions at the moment:
- ASUS PEN SA201H (delivered with ASUS Zenbook 14 Flip OLED UP5401EA-OLED024T Pine Grey)

Install required packages

- Debian / Ubuntu / Linux Mint / Pop!_OS / Zorin OS:
```
sudo apt install libevdev2 python3-libevdev i2c-tools git
```

- Arch Linux / Manjaro:
```
sudo pacman -S libevdev python-libevdev i2c-tools git
```

- Fedora:
```
sudo dnf install libevdev python-libevdev i2c-tools git
```


Then enable i2c
```
sudo modprobe i2c-dev
sudo i2cdetect -l
```

Now you can get the latest ASUS Stylus Driver for Linux from Git and install it using the following commands.
```
git clone https://github.com/ldrahnik/asus-stylus-driver
cd asus-stylus-driver
sudo ./install.sh
```

To uninstall, just run:
```
sudo ./uninstall.sh
```

**Troubleshooting**

To activate logger, do in a console:
```
LOG=DEBUG sudo -E ./asus_stylus.py
```

For some operating systems with boot failure (Pop!OS, Mint, ElementaryOS, SolusOS), before installing, please uncomment in the asus_touchpad.service file, this following property and adjust its value:
```
# ExecStartPre=/bin/sleep 2
```

Thank you very much [github.com/mohamed-badaoui](github.com/mohamed-badaoui) and all the contributors of [asus-touchpad-numpad-driver](https://github.com/mohamed-badaoui/asus-touchpad-numpad-driver) for inspiration.
