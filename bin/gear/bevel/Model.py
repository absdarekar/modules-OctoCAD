import os;
import pickle;
import math;
import numpy;
import FreeCAD;
import Draft;
import Part;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
OCTOCAD_APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from bin.gear.InvoluteProfile import InvoluteProfile;
from bin.Status import Status;
class Model():
    def __init__(self):
        self.status=Status();
        self.status.updateStatus("Initiating data");
        with open(OCTOCAD_APPDATA_PATH+"/gear/bevel/model","rb") as model_f:
            self.gear,self.profileType,self.speedRatio,self.pressureAngle,\
            self.bottomModule,self.teeth,self.gearing,self.faceWidth,\
            self.clearance,self.fillet,self.fileName=pickle.load(model_f);
        self.status.updateStatus("Calculating pitch angles");
        self.pinionPitchAngle=math.atan(self.speedRatio);
        self.gearPitchAngle=math.atan(1/self.speedRatio);
        self.status.updateStatus("Calculating radii of frustrum");
        self.status.updateStatus("Calculating modules of apex");
        self.pinionTopModule=self.bottomModule-\
                            ((2*self.faceWidth*math.sin(self.pinionPitchAngle))/self.teeth);
        self.gearTopModule=self.bottomModule-\
                            ((2*self.faceWidth*math.sin(self.gearPitchAngle))/self.teeth);
        if(self.pinionTopModule<0.35 or self.gearTopModule<0.35):
            self.status.updateStatus("Failed to generate bevel gear model, decrease face width");
            raise Exception("Failed to generate bevel gear model, decrease face width");
        self.status.updateStatus("Calculating frustrum height");
        self.pinionHeight=math.sqrt((self.faceWidth**2-(self.bottomModule*self.teeth/\
                                        2-self.pinionTopModule*self.teeth/2)**2));
        self.gearHeight=math.sqrt((self.faceWidth**2-(self.bottomModule*self.teeth/\
                                        2-self.gearTopModule*self.teeth/2)**2));
    def generateModel(self):
        self.status.updateStatus("Defining coordinates");
        ORIGIN=FreeCAD.Vector(0,0,0);
        ZAXIS=FreeCAD.Vector(0,0,1);
        self.status.updateStatus("Creating .FCStd file");
        docPinion=FreeCAD.newDocument(self.fileName+" Pinion");
        self.status.updateStatus("Generating involute profie for base");
        profileBottom, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.bottomModule,\
                                                        self.teeth,self.faceWidth,\
                                                        self.clearance,self.fillet,\
                                                        self.status);
        self.status.updateStatus("Generating involute profie for apex of pinion");
        pinionProfileTop, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.pinionTopModule,\
                                                        self.teeth,self.faceWidth,\
                                                        self.clearance,self.fillet,\
                                                        self.status);
        self.status.updateStatus("Placing involute profie at apex of pinion");
        pinionProfileTop.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,self.pinionHeight),\
                                                    FreeCAD.Rotation(ZAXIS,0),ORIGIN);
        self.status.updateStatus("Lofting base and apex involute profiles");
        docPinion.addObject('Part::Loft','bevelPinion');
        docPinion.bevelPinion.Sections=[profileBottom,pinionProfileTop];
        docPinion.bevelPinion.Solid=True;
        docPinion.bevelPinion.Ruled=False;
        docPinion.bevelPinion.Closed=False;
        docPinion.recompute();
        self.status.updateStatus("Creating .FCStd file");
        docGear=FreeCAD.newDocument(self.fileName+" Gear");
        self.status.updateStatus("Generating involute profie for apex of gear");
        gearProfileTop, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.gearTopModule,\
                                                        self.teeth,self.faceWidth,\
                                                        self.clearance,self.fillet,\
                                                        self.status);
        self.status.updateStatus("Placing involute profie at apex of gear");
        gearProfileTop.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,self.gearHeight),\
                                                    FreeCAD.Rotation(ZAXIS,0),ORIGIN);
        self.status.updateStatus("Lofting base and apex involute profiles");
        docGear.addObject('Part::Loft','bevelGear');
        docGear.bevelGear.Sections=[profileBottom,gearProfileTop];
        docGear.bevelGear.Solid=True;
        docGear.bevelGear.Ruled=False;
        docGear.bevelGear.Closed=False;
        docGear.recompute();
        self.status.updateStatus("Done");
if __name__=="__main__":
    model=Model();
    model.generateModel();
