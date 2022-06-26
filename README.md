# Asus stylus driver

**Tested only on laptop Asus ZenBook UP5401EA** with type of Asus Pen **ASUS-PEN-SA201H** and system Elementary OS 6.1 Loki.

## TODO:

- [x] (Button closer to the spike by default as middle click)
- [x] (More distant button by default as right click)
- [x] (Configurable key mappings support for buttons)
- [ ] (Do not display battery low 1%, https://gitlab.gnome.org/GNOME/gnome-power-manager/-/issues/23)


<br/>

Install required packages

- Debian / Ubuntu / Linux Mint / Pop!_OS / Zorin OS:
```
sudo apt install libevdev2 python3-libevdev git
```

- Arch Linux / Manjaro:
```
sudo pacman -S libevdev python-libevdev git
```

- Fedora:
```
sudo dnf install libevdev python-libevdev git
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

## Credits

Thank you very much [github.com/mohamed-badaoui](github.com/mohamed-badaoui) and all the contributors of [asus-touchpad-numpad-driver](https://github.com/mohamed-badaoui/asus-touchpad-numpad-driver) for your work.

## Developing

**During debugging rebember to disable service / uninstall already installed version of driver**

## Existing similar projects

I do not know any.

Why was this project created? As supplement driver with added support of configurable stylus buttons.
