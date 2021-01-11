import os;
import sys;
from PyQt5 import QtCore, QtGui, QtWidgets;
import FreeCAD;
import Draft;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from gui.Gui import Gui;
from gui.gear.spur.ModelGui import ModelGui;
from bin.gear.DesignData import DesignData;
from bin.gear.InvoluteProfile import InvoluteProfile;
class Model():
    def setupUi(self):
        self.obj_QDialog__ui=QtWidgets.QDialog();
        Gui.centering(self.obj_QDialog__ui);
        self.obj_ModelGui=ModelGui();
        self.obj_ModelGui.setupUi(self.obj_QDialog__ui);
        self.obj_QDialog__ui.show();
        self.obj_ModelGui.buttonBox.accepted.connect(self.getData);
    def generateModel(self):
        doc=FreeCAD.newDocument(self.fileName);
        profile, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.module,self.teeth,\
                                                        self.faceWidth,\
                                                        self.clearance,self.fillet);
        profileExtrude=Draft.extrude(profile,height);
    def getData(self):
        self.gear="Spur";
        self.profileType=self.obj_ModelGui.profile.currentText();
        profile=DesignData.evalProfile(self.profileType);
        self.pressureAngle=float(profile["pressureAngle"]);
        self.module=float(self.obj_ModelGui.module.text());
        self.teeth=float(self.obj_ModelGui.teeth.text());
        self.gearing=self.obj_ModelGui.gearing.currentText();
        self.faceWidth=float(self.obj_ModelGui.faceWidth.text());
        self.clearance=float(self.obj_ModelGui.clearance.text());
        self.fillet=float(self.obj_ModelGui.fillet.text());
        self.fileName=self.gear+" "+self.profileType+str(self.module)+"x"+\
                        str(self.teeth)+self.gearing+" "+str(self.faceWidth)+\
                        " "+str(self.clearance)+" "+str(self.fillet);
        self.generateModel();
if __name__=="__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Model=Model();
    obj_Model.setupUi();
