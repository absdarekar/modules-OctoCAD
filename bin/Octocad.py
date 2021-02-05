import os;
import sys;
from PyQt5 import QtCore, QtGui, QtWidgets;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
OCTOCAD_APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.OctoCAD');
os.makedirs(OCTOCAD_APPDATA_PATH,exist_ok=True);
sys.path.insert(1,OCTOCAD_FILES_PATH);
from gui.octocad.HomeGui import HomeGui;
from gui.octocad.ModuleGui import ModuleGui;
from bin.Utility import Utility;
class Octocad():
    def setupUi(self):
        self.homeWindow=QtWidgets.QMainWindow();
        Utility.alignToCenter(self.homeWindow);
        self.homeGui=HomeGui();
        self.homeGui.setupUi(self.homeWindow,OCTOCAD_FILES_PATH);
        self.homeWindow.show();
        self.homeGui.design.clicked.connect(self.setupDesignUi);
        self.homeGui.model.clicked.connect(self.setupModelUi);
    def setupDesignUi(self):
        self.designWindow=QtWidgets.QMainWindow();
        Utility.alignToCenter(self.designWindow);
        self.moduleGui=ModuleGui();
        self.moduleGui.setupUi(self.designWindow);
        self.designWindow.setWindowTitle("Design");
        self.designWindow.show();
        self.moduleGui.spurGear.clicked.connect(self.designSpur);
        self.moduleGui.helicalGear.clicked.connect(self.designHelical);
    def setupModelUi(self):
        self.modelWindow=QtWidgets.QMainWindow();
        Utility.alignToCenter(self.modelWindow);
        self.moduleGui=ModuleGui();
        self.moduleGui.setupUi(self.modelWindow);
        self.modelWindow.setWindowTitle("Model");
        self.modelWindow.show();
        self.moduleGui.spurGear.clicked.connect(self.modelSpur);
        self.moduleGui.helicalGear.clicked.connect(self.modelHelical);
        self.moduleGui.wormGear.clicked.connect(self.modelWorm);
    def designSpur(self):
        from bin.gear.spur.Design import Design;
        os.makedirs(OCTOCAD_APPDATA_PATH+"/gear/spur",exist_ok=True);
        self.design=Design();
        self.design.setupUi();
    def designHelical(self):
        from bin.gear.helical.Design import Design;
        os.makedirs(OCTOCAD_APPDATA_PATH+"/gear/helical",exist_ok=True);
        self.design=Design();
        self.design.setupUi();
    def modelSpur(self):
        FILE_PATH=OCTOCAD_FILES_PATH+"/bin/gear/spur/Model.py";
        THREAD_NAME="modelSpur";
        Utility.createThread(FILE_PATH,THREAD_NAME,self.modelWindow,self.homeWindow);
    def modelHelical(self):
        FILE_PATH=OCTOCAD_FILES_PATH+"/bin/gear/helical/Model.py";
        THREAD_NAME="modelHelical";
        Utility.createThread(FILE_PATH,THREAD_NAME,self.modelWindow,self.homeWindow);
    def modelWorm(self):
        FILE_PATH=OCTOCAD_FILES_PATH+"/bin/gear/worm/Model.py";
        THREAD_NAME="modelWorm";
        Utility.createThread(FILE_PATH,THREAD_NAME,self.modelWindow,self.homeWindow);
if __name__=="__main__":
    qApplication=QtWidgets.QApplication(sys.argv);
    octocad=Octocad();
    octocad.setupUi();
    sys.exit(qApplication.exec_());
