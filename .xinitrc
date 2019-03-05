#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

dbus-update-activation-environment --systemd DISPLAY
eval $(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh)
export SSH_AUTH_SOCK

loadkeys supplemental.kmap
xrdb -merge ~/.Xresources -cpp /usr/bin/cpp
xrandr --dpi 192
xrandr --output eDP1 --mode 2560x1440
synclient NaturalScrolling=1 &
feh --bg-scale /home/hty/Pictures/rog3.jpg &
conky -d -c /home/hty/.config/i3/.conkyrc &
compton &
python3 /home/hty/.config/i3/lemonbar_status.py &
sleep 1
exec i3
