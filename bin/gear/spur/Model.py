import os;
import pickle;
import FreeCAD;
import Draft;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
OCTOCAD_APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from bin.gear.InvoluteProfile import InvoluteProfile;
class Model():
    def __init__(self,):
        with open(OCTOCAD_APPDATA_PATH+"/gear/spur/model","rb") as model_f:
            self.gear,self.profileType,self.pressureAngle,self.module,self.teeth,\
            self.gearing,self.faceWidth,self.clearance,self.fillet,self.fileName=\
            pickle.load(model_f);
    def generateModel(self):
        doc=FreeCAD.newDocument(self.fileName);
        profile, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.module,self.teeth,\
                                                        self.faceWidth,\
                                                        self.clearance,self.fillet);
        profileExtrude=Draft.extrude(profile,height);
        FreeCADGui.ActiveDocument.getObject(profile.Name).Visibility=False;
        doc.recompute();
if __name__=="__main__":
    model=Model();
    model.generateModel();
