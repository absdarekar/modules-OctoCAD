#!/usr/bin/env bash
# Script to install required softwares and libraries for development of OctoCAD
# Operating System: Ubuntu 20.04 LTS
# author: Atharv Darekar

# Enable Universe repository

echo "Enabling Universe repository"
sudo add-apt-repository universe

# Download package information from all configured sources

echo "Updating package information"
sudo apt-get update

# install Git

echo "Installing Git"
sudo apt-get install git-core git-gui git-doc -y

# install GNU Octave and octave-symbolic package

echo "Installing GNU Octave"
sudo apt install octave -y
echo "Installing octave-symbolic package"
sudo apt-get install octave-symbolic -y

# install PyQt5 developer and PyQt5 developer tools

echo "Installing PyQt5 developer"
sudo apt install pyqt5-dev -y
echo "Installing PyQt5 developer tools"
sudo apt install pyqt5-dev-tools -y

# install Qt 5 Designer

echo "Installing Qt 5 Designer"
sudo apt install qtcreator -y

# install pip3

echo "Installing pip3"
sudo apt install python3-pip -y

# install PyQt5 and pyqt5-tools

echo "Installing PyQt5"
pip3 install PyQt5
echo "Installing pyqt5-tools"
pip3 install pyqt5-tools

# install PySide2

echo "Installing PySide2"
pip3 install PySide2

# Cloning OctoCAD

echo "Cloning OctoCAD's official repository"
mkdir $HOME/OctoCAD
git clone https://github.com/absdarekar/OctoCAD.git $HOME/OctoCAD
chmod +x $HOME/OctoCAD/bin/Octocad.py

# make .desktop file of OctoCAD

echo "Creating desktop launcher"
OCTOCAD_DESKTOP_LAUNCHER_PATH="$HOME/.local/share/applications"
echo "[Desktop Entry]" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Version=0.0.0" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Type=Application" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Terminal=false" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Name[en_IN]=OctoCAD" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Exec=$HOME/OctoCAD/bin/Octocad.py" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Name=OctoCAD" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
echo "Icon=$HOME/OctoCAD/icon/logo.png" >> $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop
chmod -x $OCTOCAD_DESKTOP_LAUNCHER_PATH/OctoCAD.desktop

# download FreeCAD 0.18.4

echo "Downloading FreeCAD 0.18.4 executable"
mkdir $HOME/.local/bin
wget "https://github.com/FreeCAD/FreeCAD/releases/download/0.18.4/FreeCAD_0.18-16146-rev1-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage" -P $HOME/.local/bin
mv $HOME/.local/bin/FreeCAD_0.18-16146-rev1-Linux-Conda_Py3Qt5_glibc2.12-x86_64.AppImage $HOME/.local/bin/freecad
chmod +x $HOME/.local/bin/freecad

# make .desktop file of FreeCAD 0.18.4

echo "Creating desktop launcher"
FREECAD_DESKTOP_LAUNCHER_PATH="$HOME/.local/share/applications"
echo "[Desktop Entry]" >> $FREECAD_DESKTOP_LAUNCHER_PATH/FreeCAD.desktop
echo "Version=0.18.4" >> $FREECAD_DESKTOP_LAUNCHER_PATH/FreeCAD.desktop
echo "Type=Application" >> $FREECAD_DESKTOP_LAUNCHER_PATH/FreeCAD.desktop
echo "Terminal=false" >> $FREECAD_DESKTOP_LAUNCHER_PATH/FreeCAD.desktop
echo "Name[en_IN]=FreeCAD" >> $FREECAD_DESKTOP_LAUNCHER_PATH/FreeCAD.desktop
echo "Exec=$HOME/.local/bin/freecad" >> $FREECAD_DESKTOP_LAUNCHER_PATH/FreeCAD.desktop
echo "Name=FreeCAD" >> $FREECAD_DESKTOP_LAUNCHER_PATH/FreeCAD.desktop
echo "Icon=$HOME/OctoCAD/icon/freecad.png" >> $FREECAD_DESKTOP_LAUNCHER_PATH/FreeCAD.desktop
chmod -x $FREECAD_DESKTOP_LAUNCHER_PATH/FreeCAD.desktop

echo "Done"
echo "Please reboot the system"
