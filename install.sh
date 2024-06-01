#!/bin/bash

# Checking if the script is runned as root (via sudo or other)
if [[ $(id -u) != 0 ]]
then
	echo "Please run the installation script as root (using sudo for example)"
	exit 1
fi

if [[ $(apt install 2>/dev/null) ]]; then
    echo 'apt is here' && sudo apt -y install libevdev2 python3-libevdev git
elif [[ $(pacman -h 2>/dev/null) ]]; then
    echo 'pacman is here' && sudo pacman --noconfirm -S libevdev python-libevdev git
elif [[ $(dnf help 2>/dev/null) ]]; then
    echo 'dnf is here' && sudo dnf -y install libevdev python-libevdev git
fi

if [[ -d stylus_layouts/__pycache__ ]] ; then
    rm -rf stylus_layouts/__pycache__
fi


echo
echo "Select key mapping layout:"
echo
echo "SA201H mapping is for remapping button closer to spike as middle click and second button as right click"
echo
PS3='Please enter your choice '
options=($(ls stylus_layouts) "Quit")
select selected_opt in "${options[@]}"
do
    if [ "$selected_opt" = "Quit" ]
    then
        exit 0
    fi

    for option in $(ls stylus_layouts);
    do
        if [ "$option" = "$selected_opt" ] ; then
            model=${selected_opt::-3}
            break
        fi
    done

    if [ -z "$model" ] ; then
        echo "invalid option $REPLY"
    else
        break
    fi
done

echo "Add asus stylus service in /usr/lib/systemd/system/"
install -Dm644 -t /usr/lib/systemd/system src/asus-stylus.service

echo "Add asus stylus config in /etc/asus-stylus/"
cat src/asus-stylus.ini | LAYOUT=$layout envsubst '$LAYOUT' > /etc/asus-stylus/asus-stylus.ini

echo "Add asus stylus in /usr/share/asus-stylus/"
install -Dm644 -t /usr/share/asus-stylus src/asus-stylus.py
install -Dm644 -t /usr/share/asus-stylus/layouts src/layouts/*
install -dm755 /var/log/asus-stylus

systemctl daemon-reload

if [[ $? != 0 ]]; then
    echo "Something went wrong when was called systemctl daemon reload"
    exit 1
else
    echo "Systemctl daemon realod called succesfully"
fi

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

