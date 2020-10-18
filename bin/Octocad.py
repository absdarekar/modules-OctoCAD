import sys;
import os;
OCTOCAD_FILE_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILE_PATH);
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.octocad.Gui import Gui;
from gui.octocad.HomeGui import HomeGui;
# from Design import Design;
# from CADmodel import CADmodel;
class Octocad():
    def openHome(self):
        self.obj_QMainWindow__openHome=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__openHome);
        self.obj_HomeGui=HomeGui();
        self.obj_HomeGui.setupUi(self.obj_QMainWindow__openHome,OCTOCAD_FILE_PATH);
        self.obj_QMainWindow__openHome.show();
        # self.obj_HomeGui.design.clicked.connect(self.openDesign);
        # self.obj_HomeGui.model.clicked.connect(self.openCADmodel);
    # def openDesign(self):
    #     self.obj_QMainWindow__openDesign=QtWidgets.QMainWindow();
    #     self.centering(self.obj_QMainWindow__openDesign);
    #     self.obj_Design=Design();
    #     self.obj_Design.setupUi(self.obj_QMainWindow__openDesign);
    #     self.obj_QMainWindow__openHome.close();
    #     self.obj_QMainWindow__openDesign.show();
    # def openCADmodel(self):
    #     self.obj_QMainWindow__openCADmodel=QtWidgets.QMainWindow();
    #     self.centering(self.obj_QMainWindow__openCADmodel);
    #     self.obj_CADmodel=CADmodel();
    #     self.obj_CADmodel.setupUi(self.obj_QMainWindow__openCADmodel);
    #     self.obj_QMainWindow__openHome.close();
    #     self.obj_QMainWindow__openCADmodel.show();
if __name__ == "__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv)
    obj_Octocad=Octocad();
    obj_Octocad.openHome();
    sys.exit(obj_QApplication.exec_())
