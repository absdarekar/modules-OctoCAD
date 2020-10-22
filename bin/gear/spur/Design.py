import sys;
import os;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.Gui import Gui;
from gui.gear.spur.DesignGui import DesignGui;
class Design():
    def Ui(self):
        self.obj_QDialog__Ui=QtWidgets.QDialog();
        Gui.centering(self.obj_QDialog__Ui);
        self.obj_DesignGui=DesignGui();
        self.obj_DesignGui.setupUi(self.obj_QDialog__Ui);
        self.obj_QDialog__Ui.show();
if __name__=="__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Design=Design();
    obj_Design.Ui();
    sys.exit(obj_QApplication.exec_());
