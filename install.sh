#!/bin/bash

# Checking if the script is runned as root (via sudo or other)
if [[ $(id -u) != 0 ]]
then
	echo "Please run the installation script as root (using sudo for example)"
	exit 1
fi

if [[ $(sudo apt install 2>/dev/null) ]]; then
    echo 'apt is here' && sudo apt -y install libevdev2 python3-libevdev i2c-tools git
elif [[ $(sudo pacman -h 2>/dev/null) ]]; then
    echo 'pacman is here' && sudo pacman --noconfirm -S libevdev python-libevdev i2c-tools git
elif [[ $(sudo dnf install 2>/dev/null) ]]; then
    echo 'dnf is here' && sudo dnf -y install libevdev python-libevdev i2c-tools git
fi

modprobe i2c-dev

# Checking if the i2c-dev module is successfuly loaded
if [[ $? != 0 ]]
then
	echo "i2c-dev module cannot be loaded correctly. Make sur you have installed i2c-tools package"
	exit 1
fi

interfaces=$(for i in $(i2cdetect -l | grep DesignWare | sed -r "s/^(i2c\-[0-9]+).*/\1/"); do echo $i; done)
if [ -z "$interfaces" ]
then
    echo "No interface i2c found. Make sure you have installed libevdev packages"
    exit 1
fi

echo "Add asus stylus service in /etc/systemd/system/"
cat asus_stylus.service > /etc/systemd/system/asus_stylus.service

mkdir -p /usr/share/asus_stylus-driver/
mkdir -p /var/log/asus_stylus-driver
install asus_stylus.py /usr/share/asus_stylus-driver/

echo "i2c-dev" | tee /etc/modules-load.d/i2c-dev.conf >/dev/null

systemctl enable asus_stylus

if [[ $? != 0 ]]
then
	echo "Something gone wrong while enabling asus_stylus.service"
	exit 1
else
	echo "Asus stylus service enabled"
fi

systemctl restart asus_stylus
if [[ $? != 0 ]]
then
	echo "Something gone wrong while enabling asus_stylus_numpad.service"
	exit 1
else
	echo "Asus stylus service started"
fi

exit 0

