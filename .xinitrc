#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

dbus-update-activation-environment --systemd DISPLAY
eval $(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh)
export SSH_AUTH_SOCK

xrdb -merge ~/.Xresources -cpp /usr/bin/cpp
xrandr --dpi 192
synclient NaturalScrolling=1 &
feh --bg-scale /home/hty/Pictures/circle.jpg &
compton &
conky -d -c /home/hty/.config/i3/.conkyrc &
python3 /home/hty/.config/i3/lemonbar_status.py &
exec i3
