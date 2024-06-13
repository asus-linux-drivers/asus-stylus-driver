#!/bin/bash

# Checking if the script is runned as root (via sudo or other)
if [[ $(id -u) != 0 ]]
then
	echo "Please run the installation script as root (using sudo for example)"
	exit 1
fi

if [[ $(apt install 2>/dev/null) ]]; then
    echo 'apt is here' && sudo apt -y install libevdev2 python3-libevdev
elif [[ $(pacman -h 2>/dev/null) ]]; then
    echo 'pacman is here' && sudo pacman -Sy --needed --noconfirm libevdev python-libevdev
elif [[ $(dnf help 2>/dev/null) ]]; then
    echo 'dnf is here' && sudo dnf -y install libevdev python-libevdev
fi

if [[ -d src/layouts/__pycache__ ]] ; then
    rm -rf src/layouts/__pycache__
fi


echo
echo "Select key mapping layout:"
echo
echo "SA201H mapping is for remapping button closer to spike as middle click and second button as right click"
echo
PS3='Please enter your choice '
options=($(ls src/layouts) "Quit")
select selected_opt in "${options[@]}"
do
    if [ "$selected_opt" = "Quit" ]
    then
        exit 0
    fi

    for option in $(ls src/layouts);
    do
        if [ "$option" = "$selected_opt" ] ; then
            layout=${selected_opt%.py}
            break
        fi
    done

    if [ -z "$layout" ] ; then
        echo "invalid option $REPLY"
    else
        break
    fi
done

echo "Add asus stylus service in /usr/lib/systemd/system/"
install -v -Dm644 -t /usr/lib/systemd/system src/asus-stylus.service

echo "Add asus stylus config in /etc/asus-stylus/"
install -v -dm755 /etc/asus-stylus
cat src/config.ini | LAYOUT=$layout envsubst '$LAYOUT' > /etc/asus-stylus/config.ini

echo "Add asus stylus in /usr/lib/asus-stylus/"
install -v -Dm644 -t /usr/lib/asus-stylus src/asus-stylus.py
install -v -Dm644 -t /usr/lib/asus-stylus/layouts src/layouts/*
install -v -dm755 /var/log/asus-stylus

echo "Add asus stylus binary in /usr/bin/"
install -v -Dm755 -t /usr/bin src/asus-stylus

systemctl daemon-reload

if [[ $? != 0 ]]; then
    echo "Something went wrong when was called systemctl daemon reload"
    exit 1
else
    echo "Systemctl daemon realod called succesfully"
fi

systemctl enable asus-stylus

if [[ $? != 0 ]]
then
	echo "Something gone wrong while enabling asus-stylus.service"
	exit 1
else
	echo "Asus stylus service enabled"
fi

systemctl restart asus-stylus
if [[ $? != 0 ]]
then
	echo "Something gone wrong while enabling asus-stylus.service"
	exit 1
else
	echo "Asus stylus service started"
fi

exit 0