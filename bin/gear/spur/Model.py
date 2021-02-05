import os;
import sys;
from PyQt5 import QtCore, QtGui, QtWidgets;
import FreeCAD;
import Draft;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from gui.gear.spur.ModelGui import ModelGui;
from bin.Utility import Utility;
from bin.gear.DesignData import DesignData;
from bin.gear.InvoluteProfile import InvoluteProfile;
class Model():
    def setupUi(self):
        self.dialog=QtWidgets.QDialog();
        Utility.alignToCenter(self.dialog);
        self.modelGui=ModelGui();
        self.modelGui.setupUi(self.dialog);
        self.dialog.show();
        self.modelGui.buttonBox.accepted.connect(self.getData);
    def generateModel(self):
        doc=FreeCAD.newDocument(self.fileName);
        profile, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.module,self.teeth,\
                                                        self.faceWidth,\
                                                        self.clearance,self.fillet);
        profileExtrude=Draft.extrude(profile,height);
        FreeCADGui.ActiveDocument.getObject(profile.Name).Visibility=False;
        doc.recompute();
    def getData(self):
        self.gear="Spur";
        self.profileType=self.modelGui.profile.currentText();
        profile=DesignData.evalProfile(self.profileType);
        self.pressureAngle=float(profile["pressureAngle"]);
        self.module=float(self.modelGui.module.text());
        self.teeth=float(self.modelGui.teeth.text());
        self.gearing=self.modelGui.gearing.currentText();
        self.faceWidth=float(self.modelGui.faceWidth.text());
        self.clearance=float(self.modelGui.clearance.text());
        self.fillet=float(self.modelGui.fillet.text());
        self.fileName=self.gear+" "+self.profileType+" "+str(self.module)+"x"+\
                        str(self.teeth)+" "+self.gearing+" "+str(self.faceWidth)+\
                        " "+str(self.clearance)+" "+str(self.fillet);
        self.generateModel();
if __name__=="__main__":
    qApplication=QtWidgets.QApplication(sys.argv);
    model=Model();
    model.setupUi();
