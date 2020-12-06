import os;
import sys;
from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtWidgets import QFileDialog;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
OCTOCAD_APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.OctoCAD');
os.makedirs(OCTOCAD_APPDATA_PATH,exist_ok=True);
sys.path.insert(1,OCTOCAD_FILES_PATH);
from gui.Gui import Gui;
from gui.octocad.HomeGui import HomeGui;
from gui.octocad.ModuleGui import ModuleGui;
class Octocad():
    def setupUi(self):
        self.obj_QMainWindow__ui=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__ui);
        self.obj_HomeGui=HomeGui();
        self.obj_HomeGui.setupUi(self.obj_QMainWindow__ui,OCTOCAD_FILES_PATH);
        self.obj_ModuleGui=ModuleGui();
        self.obj_QMainWindow__ui.show();
        self.obj_HomeGui.design.clicked.connect(self.setupDesignUi);
        self.obj_HomeGui.model.clicked.connect(self.setupModelUi);
    def setupDesignUi(self):
        self.obj_QMainWindow__setupDesignUi=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__setupDesignUi);
        self.obj_ModuleGui=ModuleGui();
        self.obj_ModuleGui.setupUi(self.obj_QMainWindow__setupDesignUi);
        self.obj_QMainWindow__setupDesignUi.setWindowTitle("Design");
        self.obj_QMainWindow__setupDesignUi.show();
        self.obj_ModuleGui.spurGear.clicked.connect(self.designSpur);
    def setupModelUi(self):
        self.obj_QMainWindow__setupModelUi=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__setupModelUi);
        self.obj_ModuleGui=ModuleGui();
        self.obj_ModuleGui.setupUi(self.obj_QMainWindow__setupModelUi);
        self.obj_QMainWindow__setupModelUi.setWindowTitle("Model");
        self.obj_QMainWindow__setupModelUi.show();
    def designSpur(self):
        from bin.gear.spur.Design import Design;
        os.makedirs(OCTOCAD_APPDATA_PATH+"/gear/spur",exist_ok=True);
        self.obj_Design__designSpur=Design();
        self.obj_Design__designSpur.setupUi();
if __name__=="__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Octocad=Octocad();
    obj_Octocad.setupUi();
    sys.exit(obj_QApplication.exec_());
def saveFile(path):
    file, fileFilter=QFileDialog.getSaveFileName(caption='',directory=os.path.expanduser('~'));
    with open(file,"w") as file_f:
        with open(path,"r") as appData_f:
            data=appData_f.read();
            file_f.write(data);
