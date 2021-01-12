import FreeCAD;
import FreeCADGui;
import Part;
def generateModel(self):
    HELIX_ANGLE=math.radians(25);
    pitch=math.pi*MODULE*TEETH/math.tan(HELIX_ANGLE);
    pitchRadius=MODULE*TEETH/2;
    helix=Part.makeHelix(pitch,faceWidth,pitchRadius);
    helixPartFeature=doc.addObject("Part::Feature","Helix");
    helixPartFeature.Shape=helix;
    profileSweepFeature=doc.addObject("Part::Sweep","Helical Gear");
    profileSweepFeature.Sections=doc.findObjects("Part::Feature",profile.Name);
    profileSweepFeature.Spine=helixPartFeature;
    profileSweepFeature.Solid=True;
    profileSweepFeature.Frenet=True;
    FreeCADGui.ActiveDocument.getObject("Helix").Visibility=False;
    doc.recompute();
