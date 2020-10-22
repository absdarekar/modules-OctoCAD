import sys;
import os;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.Gui import Gui;
from gui.octocad.HomeGui import HomeGui;
from gui.octocad.ModuleGui import ModuleGui;
class Octocad():
    def Ui(self):
        self.obj_QMainWindow__Ui=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__Ui);
        self.obj_HomeGui=HomeGui();
        self.obj_HomeGui.setupUi(self.obj_QMainWindow__Ui,OCTOCAD_FILES_PATH);
        self.obj_ModuleGui=ModuleGui();
        self.obj_QMainWindow__Ui.show();
        self.obj_HomeGui.design.clicked.connect(self.DesignUi);
        self.obj_HomeGui.model.clicked.connect(self.ModelUi);
    def DesignUi(self):
        self.obj_QMainWindow__DesignUi=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__DesignUi);
        self.obj_ModuleGui=ModuleGui();
        self.obj_ModuleGui.setupUi(self.obj_QMainWindow__DesignUi);
        self.obj_QMainWindow__DesignUi.setWindowTitle("Design");
        self.obj_QMainWindow__DesignUi.show();
        self.obj_ModuleGui.spurGear.clicked.connect(Octocad.spurDesign);
    def ModelUi(self):
        self.obj_QMainWindow__ModelUi=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__ModelUi);
        self.obj_ModuleGui=ModuleGui();
        self.obj_ModuleGui.setupUi(self.obj_QMainWindow__ModelUi);
        self.obj_QMainWindow__ModelUi.setWindowTitle("Model");
        self.obj_QMainWindow__ModelUi.show();
    def spurDesign():
        pass;
if __name__=="__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Octocad=Octocad();
    obj_Octocad.Ui();
    sys.exit(obj_QApplication.exec_());
