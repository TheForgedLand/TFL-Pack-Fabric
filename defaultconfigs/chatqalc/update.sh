#!/bin/sh

echo "Updating Qalculate!...";
sleep 1;
new_version=4.6.1;
if cd "./config/chatqalc"; then
	if curl -L -o qalculate-${new_version}-x86_64.tar.xz https://github.com/Qalculate/qalculate-gtk/releases/download/v${new_version}/qalculate-${new_version}-x86_64.tar.xz; then
		echo "Extracting files...";
		if tar -xJf qalculate-${new_version}-x86_64.tar.xz; then
			cd  qalculate-${new_version};
			if cp -f qalculate-gtk "/home/aiko/.local/share/PrismLauncher/instances/TEMPLATE/.minecraft/config/chatqalc/qalculate-4.5.1/qalculate"; then
				cp -f qalc "/home/aiko/.local/share/PrismLauncher/instances/TEMPLATE/.minecraft/config/chatqalc/qalculate-4.5.1/";
				cd ..;
			rm -r qalculate-${new_version};
			rm qalculate-${new_version}-x86_64.tar.xz;
				exit 0;
			fi
			cd ..;
		rm -r qalculate-${new_version};
		fi
		rm qalculate-${new_version}-x86_64.tar.xz;
	fi
fi
echo "Update failed";
echo "Press Enter to continue";
read _;
exit 1
