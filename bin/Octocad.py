import os;
import sys;
from PyQt5 import QtCore, QtGui, QtWidgets;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
OCTOCAD_APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.OctoCAD');
os.makedirs(OCTOCAD_APPDATA_PATH,exist_ok=True);
sys.path.insert(1,OCTOCAD_FILES_PATH);
from gui.Gui import Gui;
from gui.octocad.HomeGui import HomeGui;
from gui.octocad.ModuleGui import ModuleGui;
from bin.Utility import Utility;
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
        self.obj_ModuleGui.helicalGear.clicked.connect(self.designHelical);
    def setupModelUi(self):
        self.obj_QMainWindow__setupModelUi=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__setupModelUi);
        self.obj_ModuleGui=ModuleGui();
        self.obj_ModuleGui.setupUi(self.obj_QMainWindow__setupModelUi);
        self.obj_QMainWindow__setupModelUi.setWindowTitle("Model");
        self.obj_QMainWindow__setupModelUi.show();
        self.obj_ModuleGui.spurGear.clicked.connect(self.modelSpur);
        self.obj_ModuleGui.helicalGear.clicked.connect(self.modelHelical);
        self.obj_ModuleGui.wormGear.clicked.connect(self.modelWorm);
    def designSpur(self):
        from bin.gear.spur.Design import Design;
        os.makedirs(OCTOCAD_APPDATA_PATH+"/gear/spur",exist_ok=True);
        self.obj_Design__designSpur=Design();
        self.obj_Design__designSpur.setupUi();
    def designHelical(self):
        from bin.gear.helical.Design import Design;
        os.makedirs(OCTOCAD_APPDATA_PATH+"/gear/helical",exist_ok=True);
        self.obj_Design__designSpur=Design();
        self.obj_Design__designSpur.setupUi();
    def modelSpur(self):
        FILE_PATH=OCTOCAD_FILES_PATH+"/bin/gear/spur/Model.py";
        THREAD_NAME="modelSpur";
        modelUi=self.obj_QMainWindow__setupModelUi;
        octocadUi=self.obj_QMainWindow__ui;
        Utility.createThread(FILE_PATH,THREAD_NAME,modelUi,octocadUi);
    def modelHelical(self):
        FILE_PATH=OCTOCAD_FILES_PATH+"/bin/gear/helical/Model.py";
        THREAD_NAME="modelHelical";
        modelUi=self.obj_QMainWindow__setupModelUi;
        octocadUi=self.obj_QMainWindow__ui;
        Utility.createThread(FILE_PATH,THREAD_NAME,modelUi,octocadUi);
    def modelWorm(self):
        FILE_PATH=OCTOCAD_FILES_PATH+"/bin/gear/worm/Model.py";
        THREAD_NAME="modelWorm";
        modelUi=self.obj_QMainWindow__setupModelUi;
        octocadUi=self.obj_QMainWindow__ui;
        Utility.createThread(FILE_PATH,THREAD_NAME,modelUi,octocadUi);
if __name__=="__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Octocad=Octocad();
    obj_Octocad.setupUi();
    sys.exit(obj_QApplication.exec_());
