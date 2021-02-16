import os;
import sys;
import math;
from PyQt5 import QtCore, QtGui, QtWidgets;
import FreeCAD;
import FreeCADGui;
import Part;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from gui.gear.helical.ModelGui import ModelGui;
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
        pitch=math.pi*self.module*self.teeth/math.tan(self.helixAngle);
        pitchRadius=self.module*self.teeth/2;
        helix=Part.makeHelix(pitch,self.faceWidth*self.module,pitchRadius,0,self.leftHand,False);
        doc.addObject("Part::Feature","helix");
        doc.helix.Shape=helix;
        doc.addObject("Part::Sweep","helicalGear");
        profile, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.module,self.teeth,\
                                                        self.faceWidth,\
                                                        self.clearance,self.fillet);
        doc.helicalGear.Sections=doc.findObjects("Part::Feature",profile.Name);
        doc.helicalGear.Spine=doc.helix;
        doc.helicalGear.Solid=True;
        doc.helicalGear.Frenet=True;
        FreeCADGui.ActiveDocument.getObject(profile.Name).Visibility=False;
        FreeCADGui.ActiveDocument.getObject("helix").Visibility=False;
        doc.recompute();
    def getData(self):
        self.gear="Helical";
        self.profileType=self.modelGui.profile.currentText();
        profile=DesignData.evalProfile(self.profileType);
        self.pressureAngle=float(profile["pressureAngle"]);
        self.helixAngle=float(self.modelGui.helixAngle.text());
        self.helixHand=self.modelGui.helixHand.currentText();
        if(self.helixHand=="Left hand"):
            self.leftHand=True;
        else:
            self.leftHand=False;
        self.module=float(self.modelGui.module.text());
        self.teeth=float(self.modelGui.teeth.text());
        self.gearing=self.modelGui.gearing.currentText();
        self.faceWidth=float(self.modelGui.faceWidth.text());
        self.clearance=float(self.modelGui.clearance.text());
        self.fillet=float(self.modelGui.fillet.text());
        self.fileName=self.gear+" "+self.helixHand+" "+\
                        str(self.teeth)+" "+str(self.module*self.teeth)+" mm "\
                        +str(self.module)+" mm";
        self.helixAngle=math.radians(self.helixAngle);
        self.generateModel();
if __name__=="__main__":
    qApplication=QtWidgets.QApplication(sys.argv);
    model=Model();
    model.setupUi();
