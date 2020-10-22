import sys;
import os;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.Gui import Gui;
from gui.octocad.HomeGui import HomeGui;
from gui.octocad.ModuleGui import ModuleGui;
class Octocad():
    def ui(self):
        self.obj_QMainWindow__ui=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__ui);
        self.obj_HomeGui=HomeGui();
        self.obj_HomeGui.setupUi(self.obj_QMainWindow__ui,OCTOCAD_FILES_PATH);
        self.obj_ModuleGui=ModuleGui();
        self.obj_QMainWindow__ui.show();
        self.obj_HomeGui.design.clicked.connect(self.designUi);
        self.obj_HomeGui.model.clicked.connect(self.modelUi);
    def designUi(self):
        self.obj_QMainWindow__designUi=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__designUi);
        self.obj_ModuleGui=ModuleGui();
        self.obj_ModuleGui.setupUi(self.obj_QMainWindow__designUi);
        self.obj_QMainWindow__designUi.setWindowTitle("Design");
        self.obj_QMainWindow__designUi.show();
        self.obj_ModuleGui.spurGear.clicked.connect(Octocad.spurDesign);
    def modelUi(self):
        self.obj_QMainWindow__modelUi=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__modelUi);
        self.obj_ModuleGui=ModuleGui();
        self.obj_ModuleGui.setupUi(self.obj_QMainWindow__modelUi);
        self.obj_QMainWindow__modelUi.setWindowTitle("Model");
        self.obj_QMainWindow__modelUi.show();
    def spurDesign():
        pass;
if __name__=="__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Octocad=Octocad();
    obj_Octocad.ui();
    sys.exit(obj_QApplication.exec_());
