# Asus stylus driver

[![License: GPLv2](https://img.shields.io/badge/License-GPL_v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
![Maintainer](https://img.shields.io/badge/maintainer-ldrahnik-blue)
[![GitHub Release](https://img.shields.io/github/release/asus-linux-drivers/asus-stylus-driver.svg?style=flat)](https://github.com/asus-linux-drivers/asus-stylus-driver/releases)
[![GitHub commits](https://img.shields.io/github/commits-since/asus-linux-drivers/asus-stylus-driver/v1.1.1.svg)](https://GitHub.com/asus-linux-drivers/asus-stylus-driver/commit/)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20about-anything-1abc9c.svg)](https://github.com/asus-linux-drivers/asus-stylus-driver/issues/new/choose)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fasus-linux-drivers%2Fasus-stylus-driver&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

Supplement driver which adds support bind not bound buttons by the origin driver for X11/Wayland and allows rebind button events.

If you find the project useful, do not forget to give project a [![GitHub stars](https://img.shields.io/github/stars/asus-linux-drivers/asus-stylus-driver.svg?style=flat-square)](https://github.com/asus-linux-drivers/asus-stylus-driver/stargazers) People already did!

## Changelog

[CHANGELOG.md](CHANGELOG.md)

## Features

- Laptops with dual screens are supported (credits [@Safenein](https://github.com/Safenein))

## TODO:

- [ ] (Do not display battery low 1%, https://gitlab.gnome.org/GNOME/gnome-power-manager/-/issues/23)

## Setup

### Requirements

- Python 3
- libevdev

### Distro package

- Arch Linux (AUR):
	- [stable package](https://aur.archlinux.org/packages/asus-stylus-driver)
	- [git package](https://aur.archlinux.org/packages/asus-stylus-driver-git)

### Manual

> [!IMPORTANT]
> Install script is intended for Debian, Arch and Fedora based distros.

```
git clone https://github.com/asus-linux-drivers/asus-stylus-driver
cd asus-stylus-driver
sudo ./install.sh
```

To uninstall, just run:
```
sudo ./uninstall.sh
```

## Troubleshooting

To activate logger, do in a console:
```
sudo LOG=DEBUG asus-stylus
```

## Credits

Thank you very much [github.com/mohamed-badaoui](github.com/mohamed-badaoui) and all the contributors of [asus-touchpad-numpad-driver](https://github.com/mohamed-badaoui/asus-touchpad-numpad-driver) for your work.

## Developing

**During debugging remember to disable service / uninstall the already installed version of this driver**

## Existing similar projects

I do not know any.

**Why was this project created?** As a supplement driver which adds support bind not bound buttons by the origin driver for X11/Wayland and to allows rebind button events on X11 (Wayland does not allow exclusive input device grabbing so key events would be sent 2 times).
