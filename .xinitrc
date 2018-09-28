#!/bin/sh
#
# ~/.xinitrc
#
# Executed by startx (run your window manager from here)

xrdb -merge ~/.Xresources
i3lock-next LOCKED Terminus 30
exec i
