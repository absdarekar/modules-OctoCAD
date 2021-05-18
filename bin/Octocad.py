#!/usr/bin/python3
import os;
import sys;
from PyQt5 import QtWidgets;
FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.OctoCAD');
os.makedirs(APPDATA_PATH,exist_ok=True);
sys.path.insert(1,FILES_PATH);
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
        self.homeGui.setupUi(self.homeWindow,FILES_PATH);
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
        self.spurDesign=Spur(FILES_PATH,APPDATA_PATH,self.homeWindow,self.designWindow);
        self.moduleGui.spurGear.clicked.connect(self.spurDesign.setupDesignUi);
        self.helicalDesign=Helical(FILES_PATH,APPDATA_PATH,self.homeWindow,self.designWindow);
        self.moduleGui.helicalGear.clicked.connect(self.helicalDesign.setupDesignUi);
        self.bevelDesign=Bevel(FILES_PATH,APPDATA_PATH,self.homeWindow,self.designWindow);
        self.moduleGui.bevelGear.clicked.connect(self.bevelDesign.setupDesignUi);
    def setupModelUi(self):
        self.modelWindow=QtWidgets.QMainWindow();
        Utility.alignToCenter(self.modelWindow);
        self.moduleGui=ModuleGui();
        self.moduleGui.setupUi(self.modelWindow);
        self.modelWindow.setWindowTitle("Model");
        self.modelWindow.show();
        self.spurModel=Spur(FILES_PATH,APPDATA_PATH,self.homeWindow,self.modelWindow);
        self.moduleGui.spurGear.clicked.connect(self.spurModel.setupModelUi);
        self.helicalModel=Helical(FILES_PATH,APPDATA_PATH,self.homeWindow,self.modelWindow);
        self.moduleGui.helicalGear.clicked.connect(self.helicalModel.setupModelUi);
        self.bevelModel=Bevel(FILES_PATH,APPDATA_PATH,self.homeWindow,self.modelWindow);
        self.moduleGui.bevelGear.clicked.connect(self.bevelModel.setupModelUi);
        # self.wormModel=Worm(FILES_PATH,APPDATA_PATH,self.homeWindow,self.modelWindow);
        # self.moduleGui.wormGear.clicked.connect(self.wormModel.setupModelUi);
if __name__=="__main__":
    qApplication=QtWidgets.QApplication(sys.argv);
    octocad=Octocad();
    sys.exit(qApplication.exec_());
