#!/bin/bash

# Checking if the script is runned as root (via sudo or other)
if [[ $(id -u) != 0 ]]
then
	echo "Please run the installation script as root (using sudo for example)"
	exit 1
fi

if [[ $(sudo apt install 2>/dev/null) ]]; then
    echo 'apt is here' && sudo apt -y install libevdev2 python3-libevdev git
elif [[ $(sudo pacman -h 2>/dev/null) ]]; then
    echo 'pacman is here' && sudo pacman --noconfirm -S libevdev python-libevdev git
elif [[ $(sudo dnf install 2>/dev/null) ]]; then
    echo 'dnf is here' && sudo dnf -y install libevdev python-libevdev git
fi

if [[ -d stylus_layouts/__pycache__ ]] ; then
    rm -rf stylus_layouts/__pycache__
fi


echo
echo "Select key mapping layout:"
echo
echo "Default mapping is button closer to spike as middle click and second button as right click"
echo
PS3='Please enter your choice '
options=($(ls stylus_layouts) "Quit")
select opt in "${options[@]}"
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

echo "Add asus stylus service in /etc/systemd/system/"
cat asus_stylus.service | LAYOUT=$layout envsubst '$LAYOUT' > /etc/systemd/system/asus_stylus.service

mkdir -p /usr/share/asus_stylus-driver/stylus_layouts
mkdir -p /var/log/asus_stylus-driver
install asus_stylus.py /usr/share/asus_stylus-driver/
install -t /usr/share/asus_stylus-driver/stylus_layouts stylus_layouts/*.py

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

