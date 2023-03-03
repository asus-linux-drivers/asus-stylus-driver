# Asus stylus driver

[![License: GPLv2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fasus-linux-drivers%2Fasus-stylus-driver&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

If you find the project useful, do not forget to give project a [![GitHub stars](https://img.shields.io/github/stars/asus-linux-drivers/asus-stylus-driver.svg?style=flat-square)](https://github.com/asus-linux-drivers/asus-stylus-driver/stargazers) People already did!

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
git clone https://github.com/asus-linux-drivers/asus-stylus-driver
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

## Credits

Thank you very much [github.com/mohamed-badaoui](github.com/mohamed-badaoui) and all the contributors of [asus-touchpad-numpad-driver](https://github.com/mohamed-badaoui/asus-touchpad-numpad-driver) for your work.

## Developing

**During debugging rebember to disable service / uninstall already installed version of driver**

## Existing similar projects

I do not know any.

Why was this project created? As supplement driver with added support of configurable stylus buttons.
