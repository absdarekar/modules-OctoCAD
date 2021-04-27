import os;
import pickle;
import FreeCAD;
import FreeCADGui;
import Draft;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
OCTOCAD_APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from bin.gear.InvoluteProfile import InvoluteProfile;
from bin.Status import Status;
class Model():
    def __init__(self,):
        self.status=Status();
        self.status.updateStatus("Initiating data");
        with open(OCTOCAD_APPDATA_PATH+"/gear/spur/model","rb") as model_f:
            self.gear,self.profileType,self.pressureAngle,self.module,self.teeth,\
            self.gearing,self.faceWidth,self.clearance,self.fillet,self.fileName=\
            pickle.load(model_f);
    def generateModel(self):
        self.status.updateStatus("Creating .FCStd file");
        doc=FreeCAD.newDocument(self.fileName);
        self.status.updateStatus("Generating involute profie");
        profile, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.module,self.teeth,\
                                                        self.faceWidth,\
                                                        self.clearance,self.fillet,\
                                                        self.status);
        self.status.updateStatus("Extruding involute profile");
        profileExtrude=Draft.extrude(profile,height);
        FreeCADGui.ActiveDocument.getObject(profile.Name).Visibility=False;
        doc.recompute();
        self.status.updateStatus("Done");
if __name__=="__main__":
    model=Model();
    model.generateModel();
