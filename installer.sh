#!/bin/sh

# Shell script to install OctoCAD and FreeCAD

# Enables Universe repository and updates the system

echo "Get update"
sudo add-apt-repository universe && sudo apt-get update

# installs pip3

echo "Installing pip3"
sudo apt install python3-pip -y

# installs PyQt5

echo "Installing PyQt5"
pip3 install PyQt5

# installs FreeCAD

echo "Installing FreeCAD"
sudo add-apt-repository ppa:freecad-maintainers/freecad-stable -y && sudo apt-get update
sudo apt install freecad -y

# download OctoCAD

echo "Get OctoCAD"
wget https://github.com/absdarekar/OctoCAD/archive/master.zip
echo "Unpacking OctoCAD"
unzip master.zip -d $HOME
mv $HOME/OctoCAD-master/ $HOME/OctoCAD/
rm master.zip

# make .desktop file of OctoCAD

echo "Setting up OctoCAD"
OCTOCAD_DESKTOP_LAUNCHER_PATH="$HOME/.local/share/applications"
echo "[Desktop Entry]" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Version=1.0" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Type=Application" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Terminal=false" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Name[en_IN]=OctoCAD" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Exec=python3 $HOME/OctoCAD/bin/Octocad.py" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Name=OctoCAD" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Icon=$HOME/OctoCAD/icon/logo.png" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop

chmod 777 $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop

echo "Done"
