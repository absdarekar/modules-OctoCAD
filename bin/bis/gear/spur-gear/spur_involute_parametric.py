#program: Generates gear profile in FreeCAD
#author: Atharv Darekar
import FreeCAD;
import Part;
import Draft;
import sys;
sys.path.append("/home/ubuntu/.OctoCAD/spur-gear");
from vectors import *;
class SpurGearInvoluteProfile():
    def draw(self):
        doc=FreeCAD.newDocument("SpurGearInvoluteProfile");
        FreeCAD_profile_involute_dedendum=[];
        FreeCAD_profile_addendum=[];
        for i in range(len(profile_involute_dedendum)):
            if profile_involute_dedendum[i]!=[]:
                FreeCAD_profile_involute_dedendum.append(FreeCAD.Vector(profile_involute_dedendum[i]));
            if profile_involute_dedendum[i]==[]:
                try:
                    profile_curves=Draft.makeBSpline(Part.makePolygon(FreeCAD_profile_involute_dedendum),closed=False,face=True);
                    FreeCAD_profile_involute_dedendum=[];
                except:
                    print();
        for i in range(len(profile_addendum)-1):
            FreeCAD_profile_addendum.append(FreeCAD.Vector(profile_addendum[i]));
        profile_curves=Draft.makeLine(FreeCAD_profile_addendum[0],FreeCAD_profile_addendum[len(FreeCAD_profile_addendum)-1]);
        i=0;
        while (i<=((len(FreeCAD_profile_addendum)/2)-2)):
            profile_curves=Draft.makeLine(FreeCAD_profile_addendum[2*i+1],FreeCAD_profile_addendum[2*i+2]);
            i=i+1;
obj_SpurGearInvoluteProfile=SpurGearInvoluteProfile();
obj_SpurGearInvoluteProfile.draw();
