#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

dbus-update-activation-environment --systemd DISPLAY
eval $(/usr/bin/gnome-keyring-daemon --start --components=pkcs11,secrets,ssh)
export SSH_AUTH_SOCK

xrdb -merge ~/.Xresources -cpp /usr/bin/cpp
i3lock-next 'UNLOCK TO CONTINUE' 'GohuFont Nerd Font' 40
compton &
exec i3
