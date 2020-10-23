import sys;
import os;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.Gui import Gui;
from gui.gear.spur.DesignGui import DesignGui;
import math;
class Design():
    def ui(self):
        self.obj_QDialog__ui=QtWidgets.QDialog();
        Gui.centering(self.obj_QDialog__ui);
        self.obj_DesignGui=DesignGui();
        self.obj_DesignGui.setupUi(self.obj_QDialog__ui);
        self.obj_QDialog__ui.show();
        self.obj_DesignGui.buttonBox.accepted.connect(self.findModule);
    def getData(self):
        self.MODULES=[1,1.125,1.25,1.375,1.5,1.75,2,2.25,2.5,2.75,3,3.5,4,
                4.5,5,5.5,6,6.5,7,8,9,10,11,12,14,16,18,20,22,25,28,32,36,40,45,50];
        self.gearElasticity=float(self.obj_DesignGui.gearElasticity.text());
        self.gearStrength=float(self.obj_DesignGui.gearStrength.text());
        self.gearBendingStress=1/3*self.gearStrength;
        self.gearTeeth=float(self.obj_DesignGui.gearTeeth.text());
        self.pinionElasticity=float(self.obj_DesignGui.pinionElasticity.text());
        self.pinionRpm=float(self.obj_DesignGui.pinionRpm.text());
        self.pinionStrength=float(self.obj_DesignGui.pinionStrength.text());
        self.pinionBendingStress=1/3*self.pinionStrength;
        self.pinionTeeth=float(self.obj_DesignGui.pinionTeeth.text());
        self.power=float(self.obj_DesignGui.power.text());
        self.safetyFactorMin=float(self.obj_DesignGui.safetyFactor.text());
        self.serviceFactor=float(self.obj_DesignGui.serviceFactor.text());
        gearing=self.obj_DesignGui.gearing.currentText();
        self.gearing=self.evalGearing(gearing,self.gearTeeth,self.pinionTeeth);
        grade=self.obj_DesignGui.grade.currentText();
        self.getGrade(grade);
        profile=self.obj_DesignGui.profile.currentText();
        profile=self.evalProfile(profile);
        self.deformationFactor=eval(profile["deformationFactor"]);
        self.gearLewisFactor=eval(profile["lewisFactor"]["gear"]);
        self.pinionLewisFactor=eval(profile["lewisFactor"]["pinion"]);
        self.pressureAngle=float(profile["pressureAngle"]);
    def evalGearing(self,gearing,gearTeeth,pinionTeeth):
        if gearing=="Internal gearing":
            return ((2*gearTeeth/pinionTeeth)/(gearTeeth/pinionTeeth)-1);
        if gearing=="External gearing":
            return ((2*gearTeeth/pinionTeeth)/(gearTeeth/pinionTeeth)+1);
    def evalProfile(self,profile):
        if profile=="14.5 degree full depth involute tooth":
            return {
                    "lewisFactor":
                                    {
                                        "pinion":
                                                "0.124-(0.684/self.pinionTeeth)",
                                        "gear":
                                                "0.124-(0.684/self.gearTeeth)"
                                    },
                    "pressureAngle":
                                    "14.5",
                    "deformationFactor":
                                        "0.107/((1/self.pinionElasticity)+(1/self.gearElasticity))"
                    }
        if profile=="20 degree full depth involute tooth":
            return {
                    "lewisFactor":
                                    {
                                        "pinion":
                                                "0.154-(0.912/self.pinionTeeth)",
                                        "gear":
                                                "0.154-(0.912/self.gearTeeth)"
                                    },
                    "pressureAngle":
                                    "20",
                    "deformationFactor":
                                        "0.111/((1/self.pinionElasticity)+(1/self.gearElasticity))"
                    }
        if profile=="20 degree stub involute tooth":
            return {
                    "lewisFactor":
                                    {
                                        "pinion":
                                                "0.175-(0.95/self.pinionTeeth)",
                                        "gear":
                                                "0.175-(0.95/self.gearTeeth)"
                                    },
                    "pressureAngle":
                                    "20",
                    "deformationFactor":
                                        "0.115/((1/self.pinionElasticity)+(1/self.gearElasticity))"
                    }
    def getGrade(self,grade):
        if grade=="1":
            self.constant1=0.8;
            self.constant2=0.06;
        if grade=="2":
            self.constant1=1.25;
            self.constant2=0.10;
        if grade=="3":
            self.constant1=2.0;
            self.constant2=0.16;
        if grade=="4":
            self.constant1=3.2;
            self.constant2=0.25;
        if grade=="5":
            self.constant1=5.0;
            self.constant2=0.4;
        if grade=="6":
            self.constant1=8.0;
            self.constant2=0.63;
        if grade=="7":
            self.constant1=11.0;
            self.constant2=0.9;
        if grade=="8":
            self.constant1=16.0;
            self.constant2=1.25;
        if grade=="9":
            self.constant1=22.0;
            self.constant2=1.80;
        if grade=="10":
            self.constant1=32.0;
            self.constant2=2.5;
        if grade=="11":
            self.constant1=45.0;
            self.constant2=3.55;
        if grade=="12":
            self.constant1=63.0;
            self.constant2=5.0;
    def evalTolerance(self,module,teeth):
        phi=module+0.25*math.sqrt(module*teeth);
        error=self.constant1+self.constant2*phi;
        return (error/1000);
    def evalLoad(self,module):
        faceWidth=10*module;
        pitch=math.pi*module;
        pinionBendingLoad=self.pinionBendingStress*faceWidth*self.pinionLewisFactor*pitch;
        gearBendingLoad=self.gearBendingStress*faceWidth*self.gearLewisFactor*pitch;
        if(pinionBendingLoad<gearBendingLoad):
            bendingLoad=pinionBendingLoad;
        else:
            bendingLoad=gearBendingLoad;
        pitchVelocity=math.pi*self.pinionTeeth*module*self.pinionRpm/(60*1000);
        tangentialLoad=self.power/pitchVelocity;
        gearError=self.evalTolerance(module,self.gearTeeth);
        pinionError=self.evalTolerance(module,self.pinionTeeth);
        error=gearError+pinionError;
        sF=self.serviceFactor;
        tL=tangentialLoad;
        pV=pitchVelocity;
        dF=self.deformationFactor;
        e=error;
        fW=faceWidth;
        effectiveLoad=sF*tL+((21*pV*(dF*e*fW+tL))/(21*pV+math.sqrt(dF*e*fW+tL)));
        safetyFactor=bendingLoad/effectiveLoad;
        return pinionBendingLoad, gearBendingLoad, safetyFactor, effectiveLoad;
    def findModule(self):
        self.getData();
        safetyFactor=0.0;
        i=0;
        while(self.safetyFactorMin>=safetyFactor):
            pinionBendingLoad, gearBendingLoad, safetyFactor, effectiveLoad=self.evalLoad(self.MODULES[i]);
            i+=1;
        wearLoad=effectiveLoad*self.safetyFactorMin;
        Fw=wearLoad;
        zp=self.pinionTeeth;
        m=self.MODULES[i-1];
        Q=self.gearing;
        pA=self.pressureAngle;
        Ep=self.pinionElasticity;
        Eg=self.gearElasticity;
        sinpA=math.sin(math.radians(pA));
        cospA=math.cos(math.radians(pA));
        contactStress=math.sqrt((Fw/(10*zp*(math.pow(m,2))*Q))*(1.4/(sinpA*cospA*((1/Ep)+(1/Eg)))));
        caseHardness=contactStress/2.65;
        print(m)
        print(safetyFactor)
        print(self.safetyFactorMin)
        print(gearBendingLoad)
        print(pinionBendingLoad)
        print(effectiveLoad)
        print(wearLoad)
        print(contactStress)
        print(caseHardness)
