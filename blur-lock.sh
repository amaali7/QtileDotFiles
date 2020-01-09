#!/usr/bin/env bash
TMPBG=$(mktemp screen-XXX.png -p /tmp)
LOCK=$HOME/.config/qtile/lock.png
RES=$(xrandr | grep '*' | sed -E "s/[^0-9]*([0-9]+)x([0-9]+).*/\1*\2/")

ffmpeg -f x11grab -video_size "$RES" -y -i "$DISPLAY" -i "$LOCK" -filter_complex "boxblur=5:1,overlay=(main_w-overlay_w)/2:(main_h-overlay_h)/2" -vframes 1 "$TMPBG" -loglevel quiet

revert() {
  xset dpms 0 0 0
}
trap revert HUP INT TERM
xset +dpms dpms 5 5 5
i3lock -n -i "$TMPBG"
revert
rm "$TMPBG"

