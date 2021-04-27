import math;
import numpy;
import FreeCAD;
import Draft;
import Part;
class InvoluteProfile():
    def calculateRange(radiusRatio):
        PRECISION=0.0000001;
        xMean=0;
        xUpper=1;
        xLower=0;
        if((InvoluteProfile.evalInv(radiusRatio,xUpper)*InvoluteProfile.evalInv(radiusRatio,xLower))<0):
            xMean=(xUpper+xLower)/2;
            while(abs(InvoluteProfile.evalInv(radiusRatio,xMean))>=PRECISION):
                xMean=(xUpper+xLower)/2;
                if ((InvoluteProfile.evalInv(radiusRatio,xLower)*\
                    InvoluteProfile.evalInv(radiusRatio,xMean))<=0):
                    xUpper=xMean;
                else:
                    xLower=xMean;
        return xMean;
    def evalInv(radiusRatio,x):
        return eval("radiusRatio-math.cos(x)-x*math.sin(x)");
    def generateHob(baseRadius,addendumRadius,dedendumRadius,angularSeperation,\
                    clearance,filletRadius,sign,status):
        CLOSED=True;
        OPEN=False;
        FACE=True;
        WIRE_FRAME=False;
        PLACEMENT=None
        DELETE=True;
        status.updateStatus("Setting precision to 0.001 mm");
        PRECISION=0.001;
        status.updateStatus("Calculating range for involute function");
        ratioAddendum=addendumRadius/baseRadius;
        ratioDedendum=dedendumRadius/baseRadius;
        t=numpy.arange(InvoluteProfile.calculateRange(ratioDedendum),\
                        InvoluteProfile.calculateRange(ratioAddendum),PRECISION);
        status.updateStatus("Defining involute curves");
        xInvLeft=baseRadius*(numpy.cos(-t-angularSeperation)-t*numpy.sin(-t-angularSeperation));
        yInvLeft=baseRadius*(numpy.sin(-t-angularSeperation)+t*numpy.cos(-t-angularSeperation));
        xInvRight=baseRadius*(numpy.cos(t+angularSeperation)+t*numpy.sin(t+angularSeperation));
        yInvRight=baseRadius*(numpy.sin(t+angularSeperation)-t*numpy.cos(t+angularSeperation));
        InvLeftVector=[];
        InvRightVector=[];
        status.updateStatus("Defining vectors for involute curves");
        for i in range(len(t)):
            InvLeftVector.append(FreeCAD.Vector(xInvLeft[i],yInvLeft[i],0));
            InvRightVector.append(FreeCAD.Vector(xInvRight[i],yInvRight[i],0));
        status.updateStatus("Drafting involute curves");
        InvLeft=Draft.makeBSpline(Part.makePolygon(InvLeftVector),OPEN,WIRE_FRAME);
        InvRight=Draft.makeBSpline(Part.makePolygon(InvRightVector),OPEN,WIRE_FRAME);
        status.updateStatus("Defining clearance lines");
        clearanceLeftX=FreeCAD.Vector(xInvLeft[0]-clearance+filletRadius,yInvLeft[0],0);
        clearanceRightX=FreeCAD.Vector(xInvRight[0]-clearance+filletRadius,yInvRight[0],0);
        status.updateStatus("Drafting clearance lines");
        lineLeft=Draft.makeLine(InvLeftVector[0],clearanceLeftX);
        lineRight=Draft.makeLine(InvRightVector[0],clearanceRightX);
        status.updateStatus("Defining root line");
        clearanceLeftY=FreeCAD.Vector(xInvLeft[0]-clearance,yInvLeft[0]+filletRadius,0);
        clearanceRightY=FreeCAD.Vector(xInvRight[0]-clearance,yInvRight[0]-filletRadius,0);
        status.updateStatus("Drafting root line");
        lineClearance=Draft.makeLine(clearanceLeftY,clearanceRightY);
        status.updateStatus("Defining fillet curves");
        filletLeftCenter=FreeCAD.Placement();
        filletRightCenter=FreeCAD.Placement();
        filletLeftCenter.move(FreeCAD.Vector(xInvLeft[0]-clearance+filletRadius,\
                                yInvLeft[0]+filletRadius,0));
        filletRightCenter.move(FreeCAD.Vector(xInvRight[0]-clearance+filletRadius,\
                                yInvRight[0]-filletRadius,0));
        startangle=180;
        endangle=270;
        status.updateStatus("Drafting fillet curves");
        filletLeft=Draft.makeCircle(filletRadius,filletLeftCenter,WIRE_FRAME,startangle,endangle);
        startangle=90;
        endangle=180;
        filletRight=Draft.makeCircle(filletRadius,filletRightCenter,WIRE_FRAME,startangle,endangle);
        radius=math.sqrt(xInvLeft[len(xInvLeft)-1]**2+yInvLeft[len(xInvLeft)-1]**2);
        status.updateStatus("Defining addendum arc");
        arcAngle=sign*(math.atan(yInvLeft[len(xInvLeft)-1]/xInvLeft[len(xInvLeft)-1])*180/math.pi);
        startangle=arcAngle;
        endangle=-arcAngle;
        status.updateStatus("Drafting addendum arc");
        arc=Draft.makeCircle(radius,PLACEMENT,WIRE_FRAME,startangle,endangle);
        status.updateStatus("Generating hob geometry");
        hobWire, deletedFeatures=Draft.upgrade([arc,lineRight,lineLeft,lineClearance,\
                                                InvRight,InvLeft,filletRight,filletLeft],DELETE);
        status.updateStatus("Generating hob face");
        hobFace, deletedFeatures=Draft.upgrade(hobWire,DELETE);
        return hobFace[0];
    def generateTooth(pressureAngle,module,teeth,clearance,fillet):
        SIGN=-1;
        pressureAngle=math.radians(pressureAngle);
        baseRadius=module*teeth*math.cos(pressureAngle)/2;
        addendumRadius=(module*teeth+2*module)/2;
        dedendumRadius=(module*teeth-2.5*module)/2;
        angularSeperation=SIGN*(math.pi/(2*teeth)+(math.tan(pressureAngle)-pressureAngle));
        clearance=clearance*module;
        filletRadius=fillet*module;
        toothFace=InvoluteProfile.generateHob(baseRadius,addendumRadius,\
                                            dedendumRadius,angularSeperation,\
                                            clearance,filletRadius,SIGN);
        return toothFace;
    def generateProfile(pressureAngle,module,teeth,faceWidth,clearance,fillet,status):
        status.updateStatus("Defining coordinates");
        ORIGIN=FreeCAD.Vector(0,0,0);
        ZAXIS=FreeCAD.Vector(0,0,1);
        COPY=True;
        SIGN=+1;
        status.updateStatus("Calculating parameters for involute proflie");
        pressureAngle=math.radians(pressureAngle);
        baseRadius=module*teeth*math.cos(pressureAngle)/2;
        addendumRadius=(module*teeth+2*module)/2;
        dedendumRadius=(module*teeth-2.5*module)/2;
        angularSeperation=SIGN*(math.pi/(2*teeth)-(math.tan(pressureAngle)-pressureAngle));
        faceWidth=faceWidth*module;
        clearance=clearance*module;
        filletRadius=fillet*module;
        status.updateStatus("Drafting addendum circle");
        addendumCirle=Draft.makeCircle(addendumRadius);
        status.updateStatus("Generating hob");
        hobFace=InvoluteProfile.generateHob(baseRadius,addendumRadius,\
                                            dedendumRadius,angularSeperation,\
                                            clearance,filletRadius,SIGN,status);
        status.updateStatus("Generated hob");
        hobFaces=[]
        hobFaces.append(hobFace);
        angle=360/teeth;
        status.updateStatus("Defining hob cuts for addendum cirle");
        while(angle<360):
            hobFaces.append(Draft.rotate(hobFaces[0],angle,ORIGIN,ZAXIS,COPY));
            angle+=360/teeth;
        profile=addendumCirle;
        for i in range(len(hobFaces)):
            status.updateStatus("Cutting tooth "+str(i+1));
            profile=Draft.cut(profile,hobFaces[i]);
        height=FreeCAD.Vector(0,0,faceWidth);
        return profile, height;
