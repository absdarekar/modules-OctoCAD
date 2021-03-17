#!/bin/sh

# Shell script to install OctoCAD and FreeCAD

# Download package information from all configured sources

echo "Update package information"
sudo apt-get update

# install PyQt5 developer and PyQt5 developer tools

echo "Installing PyQt5 developer"
sudo apt install pyqt5-dev
echo "Installing PyQt5 developer tools"
sudo apt install pyqt5-dev-tools

# installs FreeCAD

echo "Installing FreeCAD"
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
