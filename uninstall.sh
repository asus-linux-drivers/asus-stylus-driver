#!/bin/bash

if [[ $(id -u) != 0 ]]
then
	echo "Please, run this script as root (using sudo for example)"
	exit 1
fi

systemctl stop asus-stylus
if [[ $? != 0 ]]
then
	echo "asus-stylus.service cannot be stopped correctly..."
	exit 1
fi

systemctl disable asus-stylus
if [[ $? != 0 ]]
then
	echo "asus-stylus.service cannot be disabled correctly..."
	exit 1
fi

rm -f /usr/lib/systemd/system/asus-stylus.service
if [[ $? != 0 ]]
then
	echo "/usr/lib/systemd/system/asus-stylus.service cannot be removed correctly..."
	exit 1
fi

rm -rf /etc/asus-stylus/
if [[ $? != 0 ]]
then
	echo "/etc/asus-stylus/ cannot be removed correctly..."
	exit 1
fi

rm -rf /usr/share/asus-stylus/
if [[ $? != 0 ]]
then
	echo "/usr/share/asus-stylus/ cannot be removed correctly..."
	exit 1
fi

rm -rf /var/log/asus-stylus
if [[ $? != 0 ]]
then
	echo "/var/log/asus-stylus cannot be removed correctly..."
	exit 1
fi

systemctl daemon-reload

if [[ $? != 0 ]]; then
    echo "Something went wrong when was called systemctl daemon reload"
    exit 1
else
    echo "Systemctl daemon realod called succesfully"
fi

echo "Asus stylus python driver uninstalled"
exit 0
