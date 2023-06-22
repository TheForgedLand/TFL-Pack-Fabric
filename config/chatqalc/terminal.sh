#!/bin/sh

if [ $(command -v gnome-terminal) ]; then
	if gnome-terminal --wait --version; then
		detected_term="gnome-terminal --wait -- ";
	else
		detected_term="gnome-terminal --disable-factory -- ";
	fi
elif [ $(command -v xfce4-terminal) ]; then
	detected_term="xfce4-terminal --disable-server -e ";
else
	for t in x-terminal-emulator konsole alacritty qterminal xterm urxvt rxvt kitty sakura terminology termite tilix; do
		if [ $(command -v $t) ]; then
			detected_term="$t -e ";
			break
		fi
	done
fi
$detected_term ./config/chatqalc/update.sh;
exec /home/aiko/.local/share/PrismLauncher/instances/TEMPLATE/.minecraft/config/chatqalc/qalculate-4.5.1/qalculate
