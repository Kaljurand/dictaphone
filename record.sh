
dir_base=recordings

./dictaphone_ui.py --dir-base $dir_base -c 1 -r 16000 --playback --ui-in=kb --transcribe

find $dir_base | sort
