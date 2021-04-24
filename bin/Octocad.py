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
from bin.gear.bevel.Bevel import Bevel;
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
        self.spurDesign=Spur(OCTOCAD_FILES_PATH,OCTOCAD_APPDATA_PATH,self.homeWindow,self.designWindow);
        self.moduleGui.spurGear.clicked.connect(self.spurDesign.setupDesignUi);
        self.helicalDesign=Helical(OCTOCAD_FILES_PATH,OCTOCAD_APPDATA_PATH,self.homeWindow,self.designWindow);
        self.moduleGui.helicalGear.clicked.connect(self.helicalDesign.setupDesignUi);
        self.bevelDesign=Bevel(OCTOCAD_FILES_PATH,OCTOCAD_APPDATA_PATH,self.homeWindow,self.designWindow);
        self.moduleGui.bevelGear.clicked.connect(self.bevelDesign.setupDesignUi);
    def setupModelUi(self):
        self.modelWindow=QtWidgets.QMainWindow();
        Utility.alignToCenter(self.modelWindow);
        self.moduleGui=ModuleGui();
        self.moduleGui.setupUi(self.modelWindow);
        self.modelWindow.setWindowTitle("Model");
        self.modelWindow.show();
        self.spurModel=Spur(OCTOCAD_FILES_PATH,OCTOCAD_APPDATA_PATH,self.homeWindow,self.modelWindow);
        self.moduleGui.spurGear.clicked.connect(self.spurModel.setupModelUi);
        self.helicalModel=Helical(OCTOCAD_FILES_PATH,OCTOCAD_APPDATA_PATH,self.homeWindow,self.modelWindow);
        self.moduleGui.helicalGear.clicked.connect(self.helicalModel.setupModelUi);
        # self.moduleGui.wormGear.clicked.connect(self.modelWorm);
if __name__=="__main__":
    qApplication=QtWidgets.QApplication(sys.argv);
    octocad=Octocad();
    sys.exit(qApplication.exec_());
