#!/bin/sh
nitrogen --restore &
guake & 
nm-applet &
compton --config .config/compton/compton.conf &
lxpolkit &
light -I &
Telegram &
#setxkbmap -layout 'us,ar' &
#setxkbmap -option 'grp:alt_shift_toggle'&


