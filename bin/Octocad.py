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
from bin.gear.spur.Spur import Spur;
from bin.gear.helical.Helical import Helical;
class Octocad():
    def __init__(self):
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
        self.spur=Spur(OCTOCAD_FILES_PATH,OCTOCAD_APPDATA_PATH,self.homeWindow,self.designWindow);
        self.moduleGui.spurGear.clicked.connect(self.spur.setupDesignUi);
        self.helical=Helical(OCTOCAD_FILES_PATH,OCTOCAD_APPDATA_PATH,self.homeWindow,self.designWindow);
        self.moduleGui.helicalGear.clicked.connect(self.helical.setupDesignUi);
        # self.moduleGui.bevelGear.clicked.connect(self.designBevel);
    def setupModelUi(self):
        self.modelWindow=QtWidgets.QMainWindow();
        Utility.alignToCenter(self.modelWindow);
        self.moduleGui=ModuleGui();
        self.moduleGui.setupUi(self.modelWindow);
        self.modelWindow.setWindowTitle("Model");
        self.modelWindow.show();
        self.spur=Spur(OCTOCAD_FILES_PATH,OCTOCAD_APPDATA_PATH,self.homeWindow,self.modelWindow);
        self.moduleGui.spurGear.clicked.connect(self.spur.setupModelUi);
        self.helical=Helical(OCTOCAD_FILES_PATH,OCTOCAD_APPDATA_PATH,self.homeWindow,self.modelWindow);
        self.moduleGui.helicalGear.clicked.connect(self.helical.setupModelUi);
        # self.moduleGui.wormGear.clicked.connect(self.modelWorm);
if __name__=="__main__":
    qApplication=QtWidgets.QApplication(sys.argv);
    octocad=Octocad();
    sys.exit(qApplication.exec_());
