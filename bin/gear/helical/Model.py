import os;
import pickle;
import math;
import FreeCAD;
import FreeCADGui;
import Draft;
import Part;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
OCTOCAD_APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from bin.gear.InvoluteProfile import InvoluteProfile;
class Model():
    def __init__(self,):
        with open(OCTOCAD_APPDATA_PATH+"/gear/helical/model","rb") as model_f:
            self.gear,self.profileType,self.pressureAngle,self.helixAngle,\
            self.helixHand,self.module,self.teeth,self.gearing,self.faceWidth,\
            self.clearance,self.fillet,self.fileName=\
            pickle.load(model_f);
        if(self.helixHand=="Left hand"):
            self.leftHand=True;
        else:
            self.leftHand=False;
        self.helixAngle=math.radians(self.helixAngle);
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
if __name__=="__main__":
    model=Model();
    model.generateModel();
