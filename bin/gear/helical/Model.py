import os;
import sys;
import math;
from PyQt5 import QtCore, QtGui, QtWidgets;
import FreeCAD;
import FreeCADGui;
import Part;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from gui.Gui import Gui;
from gui.gear.helical.ModelGui import ModelGui;
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
        pitch=math.pi*self.module*self.teeth/math.tan(self.helixAngle);
        pitchRadius=self.module*self.teeth/2;
        helix=Part.makeHelix(pitch,self.faceWidth*self.module,pitchRadius);
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
        self.profileType=self.obj_ModelGui.profile.currentText();
        profile=DesignData.evalProfile(self.profileType);
        self.pressureAngle=float(profile["pressureAngle"]);
        self.helixAngle=float(self.obj_ModelGui.helixAngle.text());
        self.module=float(self.obj_ModelGui.module.text());
        self.teeth=float(self.obj_ModelGui.teeth.text());
        self.gearing=self.obj_ModelGui.gearing.currentText();
        self.faceWidth=float(self.obj_ModelGui.faceWidth.text());
        self.clearance=float(self.obj_ModelGui.clearance.text());
        self.fillet=float(self.obj_ModelGui.fillet.text());
        self.fileName=self.gear+" "+str(self.helixAngle)+" "+\
                        self.profileType+" "+str(self.module)+"x"+str(self.teeth)+\
                        " "+self.gearing+" "+str(self.faceWidth)+" "+\
                        str(self.clearance)+" "+str(self.fillet);
        self.helixAngle=math.radians(self.helixAngle);
        self.generateModel();
if __name__=="__main__":
    obj_QApplication=QtWidgets.QApplication(sys.argv);
    obj_Model=Model();
    obj_Model.setupUi();
