import FreeCAD;
import Draft;
import Part;
import math;
import numpy;


doc=FreeCAD.newDocument("Spur Gear");


def calculateRange(radiusRatio):
    PRECISION=0.0000001;
    xMean=0;
    xUpper=1;
    xLower=0;
    if((evalInv(radiusRatio,xUpper)*evalInv(radiusRatio,xLower))<0):
        xMean=(xUpper+xLower)/2;
        while(abs(evalInv(radiusRatio,xMean))>=PRECISION):
            xMean=(xUpper+xLower)/2;
            if ((evalInv(radiusRatio,xLower)*evalInv(radiusRatio,xMean))<=0):
                xUpper=xMean;
            else:
                xLower=xMean;
    return xMean;


def evalInv(radiusRatio,x):
    return eval("radiusRatio-math.cos(x)-x*math.sin(x)");


MODULE=4;
TEETH=18;
PRECISION=0.001;
PRESSURE_ANGLE=20*math.pi/180;
ORIGIN=FreeCAD.Vector(0,0,0);
ZAXIS=FreeCAD.Vector(0,0,1);
COPY=True;
CLOSED=True;
OPEN=False;
FACE=True;
WIRE_FRAME=False;
PLACEMENT=None
DELETE=True;


faceWidth=10*MODULE;
baseRadius=MODULE*TEETH*math.cos(PRESSURE_ANGLE)/2;
addendumRadius=(MODULE*TEETH+2*MODULE)/2;
dedendumRadius=(MODULE*TEETH-2.5*MODULE)/2;
clearance=0.25*MODULE; # 20 degree full depth involute profile
filletRadius=0.15*MODULE # should not exceed clearance
angularSeperation=math.pi/(2*TEETH);
ratioAddendum=addendumRadius/baseRadius;
ratioDedendum=dedendumRadius/baseRadius;
height=FreeCAD.Vector(0,0,faceWidth);
angle=360/TEETH;


t=numpy.arange(calculateRange(ratioDedendum),calculateRange(ratioAddendum),PRECISION);
xInvLeft=baseRadius*(numpy.cos(-t-angularSeperation)-t*numpy.sin(-t-angularSeperation));
yInvLeft=baseRadius*(numpy.sin(-t-angularSeperation)+t*numpy.cos(-t-angularSeperation));
xInvRight=baseRadius*(numpy.cos(t+angularSeperation)+t*numpy.sin(t+angularSeperation));
yInvRight=baseRadius*(numpy.sin(t+angularSeperation)-t*numpy.cos(t+angularSeperation));


InvLeftVector=[];
InvRightVector=[];
for i in range(len(t)):
    InvLeftVector.append(FreeCAD.Vector(xInvLeft[i],yInvLeft[i],0));
    InvRightVector.append(FreeCAD.Vector(xInvRight[i],yInvRight[i],0));


addendumCirle=Draft.makeCircle(addendumRadius);
InvLeft=Draft.makeBSpline(Part.makePolygon(InvLeftVector),OPEN,WIRE_FRAME);
InvRight=Draft.makeBSpline(Part.makePolygon(InvRightVector),OPEN,WIRE_FRAME);
clearanceLeftX=FreeCAD.Vector(xInvLeft[0]-clearance+filletRadius,yInvLeft[0],0);
clearanceRightX=FreeCAD.Vector(xInvRight[0]-clearance+filletRadius,yInvRight[0],0);
lineLeft=Draft.makeLine(InvLeftVector[0],clearanceLeftX);
lineRight=Draft.makeLine(InvRightVector[0],clearanceRightX);
clearanceLeftY=FreeCAD.Vector(xInvLeft[0]-clearance,yInvLeft[0]+filletRadius,0);
clearanceRightY=FreeCAD.Vector(xInvRight[0]-clearance,yInvRight[0]-filletRadius,0);
lineClearance=Draft.makeLine(clearanceLeftY,clearanceRightY);
filletLeftCenter=FreeCAD.Placement();
filletRightCenter=FreeCAD.Placement();
filletLeftCenter.move(FreeCAD.Vector(xInvLeft[0]-clearance+filletRadius,\
                        yInvLeft[0]+filletRadius,0));
filletRightCenter.move(FreeCAD.Vector(xInvRight[0]-clearance+filletRadius,\
                        yInvRight[0]-filletRadius,0));
filletLeft=Draft.makeCircle(filletRadius,filletLeftCenter,False,180,270);
filletRight=Draft.makeCircle(filletRadius,filletRightCenter,False,90,180);
radius=math.sqrt(xInvLeft[len(xInvLeft)-1]**2+yInvLeft[len(xInvLeft)-1]**2);
arcAngle=math.atan(yInvLeft[len(xInvLeft)-1]/xInvLeft[len(xInvLeft)-1])*180/math.pi;
startangle=arcAngle;
endangle=-arcAngle;
arc=Draft.makeCircle(radius,PLACEMENT,WIRE_FRAME,startangle,endangle);
cutWire, deletedFeatures=Draft.upgrade([arc,lineRight,lineLeft,lineClearance,\
                                        InvRight,InvLeft,filletRight,filletLeft],DELETE);
cutFace, deletedFeatures=Draft.upgrade(cutWire,DELETE);
cutFaces=[]
cutFaces.append(cutFace[0]);
while(angle<360):
    cutFaces.append(Draft.rotate(cutFaces[0],angle,ORIGIN,ZAXIS,COPY));
    angle+=360/TEETH;
profile=addendumCirle;
for i in range(len(cutFaces)):
    profile=Draft.cut(profile,cutFaces[i]);
profileExtrude=Draft.extrude(profile,height);
