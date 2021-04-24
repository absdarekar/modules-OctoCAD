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
        pass;
        # with open(OCTOCAD_APPDATA_PATH+"/gear/spur/model","rb") as model_f:
        #     self.gear,self.profileType,self.pressureAngle,self.module,self.teeth,\
        #     self.gearing,self.faceWidth,self.clearance,self.fillet,self.fileName=\
        #     pickle.load(model_f);
    def generateModel(self):
        XAXIS=FreeCAD.Vector(1,0,0);
        INTERFERANCE=0.1;
        ORIGIN=FreeCAD.Vector(0,0,0);
        COPY=True;
        # doc=FreeCAD.newDocument(self.fileName);
        doc=FreeCAD.newDocument("Worm Gear"); #temporary file name for testing
        # tooth=InvoluteProfile.generateTooth(self.pressureAngle,self.module,\
        #                                     self.teeth,self.clearance,\
        #                                     self.fillet);
        ###
        #temporary variables for testing
        MODULE=4;
        TEETH=18;
        PRESSURE_ANGLE=20;
        CLEARANCE=0.5;
        FILLET=0.25;
        clearance=CLEARANCE*MODULE;
        ###
        tooth=InvoluteProfile.generateTooth(PRESSURE_ANGLE,MODULE,TEETH,CLEARANCE,FILLET);
        tooth=Draft.rotate(tooth,90,ORIGIN,XAXIS,not(COPY));
        pitch=math.pi*MODULE;
        helixRadius=MODULE*TEETH*math.cos(math.radians(PRESSURE_ANGLE))/2-clearance;
        helix=Part.makeHelix(pitch,MODULE*20,helixRadius);
        doc.addObject("Part::Feature","helix");
        doc.helix.Shape=helix;
        doc.addObject("Part::Sweep","threads");
        doc.threads.Sections=doc.findObjects("Part::Feature",tooth.Name);
        doc.threads.Spine=doc.helix;
        doc.threads.Solid=True;
        doc.threads.Frenet=True;
        worm=Part.makeCylinder(tooth.Shape.BoundBox.XMin+INTERFERANCE,MODULE*20);
        doc.addObject("Part::Feature","worm");
        doc.worm.Shape=worm;
        doc.addObject("Part::MultiFuse","wormGear");
        doc.wormGear.Shapes=[doc.threads,doc.worm,];
        FreeCADGui.ActiveDocument.getObject(tooth.Name).Visibility=False;
        FreeCADGui.ActiveDocument.getObject("helix").Visibility=False;
        FreeCADGui.ActiveDocument.getObject("threads").Visibility=False;
        FreeCADGui.ActiveDocument.getObject("worm").Visibility=False;
        doc.recompute();
if __name__=="__main__":
    model=Model();
    model.generateModel();
