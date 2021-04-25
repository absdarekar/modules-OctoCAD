import os;
import math;
import numpy;
import FreeCAD;
import Draft;
import Part;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
OCTOCAD_APPDATA_PATH=os.path.join(os.path.expanduser('~'),'.OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from bin.gear.InvoluteProfile import InvoluteProfile;
class Model():
    def __init__(self):
        self.pressureAngle=20
        self.bottomModule=4
        self.teeth=18
        self.gearing=""
        self.faceWidth=20;
        self.clearance=0.5;
        self.fillet=0.25;
        self.gearRatio=1.25;
        self.pinionPitchAngle=math.atan(self.gearRatio);
        self.gearPitchAngle=math.atan(1/self.gearRatio);
        self.pinionTopModule=self.bottomModule-\
                            ((2*self.faceWidth*math.sin(self.pinionPitchAngle))/self.teeth);
        self.gearTopModule=self.bottomModule-\
                            ((2*self.faceWidth*math.sin(self.gearPitchAngle))/self.teeth);
        self.pinionHeight=math.sqrt((self.faceWidth**2-(self.bottomModule*self.teeth/\
                                        2-self.pinionTopModule*self.teeth/2)**2));
        self.gearHeight=math.sqrt((self.faceWidth**2-(self.bottomModule*self.teeth/\
                                        2-self.gearTopModule*self.teeth/2)**2));
        self.fileName="Bevel"
    def generateModel(self):
        ORIGIN=FreeCAD.Vector(0,0,0);
        ZAXIS=FreeCAD.Vector(0,0,1);
        docPinion=FreeCAD.newDocument(self.fileName+" Pinion");
        profileBottom, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.bottomModule,\
                                                        self.teeth,self.faceWidth,\
                                                        self.clearance,self.fillet);
        pinionProfileTop, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.pinionTopModule,\
                                                        self.teeth,self.faceWidth,\
                                                        self.clearance,self.fillet);
        pinionProfileTop.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,self.pinionHeight),\
                                                    FreeCAD.Rotation(ZAXIS,0),ORIGIN);
        docPinion.addObject('Part::Loft','bevelPinion');
        docPinion.bevelPinion.Sections=[profileBottom,pinionProfileTop];
        docPinion.bevelPinion.Solid=True;
        docPinion.bevelPinion.Ruled=False;
        docPinion.bevelPinion.Closed=False;
        docPinion.recompute();
        docGear=FreeCAD.newDocument(self.fileName+" Gear");
        gearProfileTop, height=InvoluteProfile.generateProfile(self.pressureAngle,\
                                                        self.gearTopModule,\
                                                        self.teeth,self.faceWidth,\
                                                        self.clearance,self.fillet);
        gearProfileTop.Placement=FreeCAD.Placement(FreeCAD.Vector(0,0,self.gearHeight),\
                                                    FreeCAD.Rotation(ZAXIS,0),ORIGIN);
        docGear.addObject('Part::Loft','bevelGear');
        docGear.bevelGear.Sections=[profileBottom,gearProfileTop];
        docGear.bevelGear.Solid=True;
        docGear.bevelGear.Ruled=False;
        docGear.bevelGear.Closed=False;
        docGear.recompute();
if __name__=="__main__":
    model=Model();
    model.generateModel();
