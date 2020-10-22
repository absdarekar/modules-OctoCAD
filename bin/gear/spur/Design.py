import sys;
import os;
OCTOCAD_FILES_PATH=os.path.join(os.path.expanduser('~'),'OctoCAD');
sys.path.insert(1,OCTOCAD_FILES_PATH);
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.Gui import Gui;
from gui.gear.spur.DesignGui import DesignGui;
import math;
class Design():
    MODULES=[1,1.125,1.25,1.375,1.5,1.75,2,2.25,2.5,2.75,3,3.5,4,
            4.5,5,5.5,6,6.5,7,8,9,10,11,12,14,16,18,20,22,25,28,32,36,40,45,50];
    def ui(self):
        self.obj_QDialog__ui=QtWidgets.QDialog();
        Gui.centering(self.obj_QDialog__ui);
        self.obj_DesignGui=DesignGui();
        self.obj_DesignGui.setupUi(self.obj_QDialog__ui);
        self.obj_QDialog__ui.show();
    def getData(self):
        gearElasticity=float(self.obj_DesignGui.gearElasticity.text());
        gearStrength=float(self.obj_DesignGui.gearStrength.text());
        gearBendingStressMax=1/3*gearStrength;
        gearTeeth=float(self.obj_DesignGui.gearTeeth.text());
        gearing=self.obj_DesignGui.gearing.currentText();
        gearing=self.evalGearing(gearing);
        grade=self.obj_DesignGui.grade.currentText();
        self.getGrade(grade);
        pinionElasticity=float(self.obj_DesignGui.pinionElasticity.text());
        pinionRpm=float(self.obj_DesignGui.pinionRpm.text());
        pinionStrength=float(self.obj_DesignGui.pinionStrength.text());
        pinionBendingStressMax=1/3*pinionStrength;
        pinionTeeth=float(self.obj_DesignGui.pinionTeeth.text());
        power=float(self.obj_DesignGui.power.text());
        profile=self.obj_DesignGui.profile.currentText();
        profile=self.evalProfile(profile);
        deformationFactor=eval(profile["deformationFactor"]);
        gearLewisFactor=eval(profile["lewisFactor"]["gear"]);
        pinionLewisFactor=eval(profile["lewisFactor"]["pinion"]);
        pressureAngle=float(profile["pressureAngle"]);
        safetyFactorMin=float(self.obj_DesignGui.safetyFactor.text());
        serviceFactor=float(self.obj_DesignGui.serviceFactor.text());
    def evalGearing(self,gearing):
        if gearing=="Internal gearing":
            return (2*gearTeeth/pinionTeeth))/(gearTeeth/pinionTeeth)-1);
        if gearing=="External gearing":
            return (2*gearTeeth/pinionTeeth))/(gearTeeth/pinionTeeth)+1);
    def evalProfile(self,profile):
        if profile=="14.5 degree full depth involute tooth":
            return {
                    "lewisFactor":
                                    {
                                        "pinion":
                                                "0.124-(0.684/pinionTeeth)",
                                        "gear":
                                                "0.124-(0.684/gearTeeth)"
                                    },
                    "pressureAngle":
                                    "14.5",
                    "deformationFactor":
                                        "0.107/((1/pinionElasticity)+(1/gearElasticity))"
                    }
        if profile=="20 degree full depth involute tooth":
            return {
                    "lewisFactor":
                                    {
                                        "pinion":
                                                "0.154-(0.912/pinionTeeth)",
                                        "gear":
                                                "0.154-(0.912/gearTeeth)"
                                    },
                    "pressureAngle":
                                    "20",
                    "deformationFactor":
                                        "0.111/((1/pinionElasticity)+(1/gearElasticity))"
                    }
        if profile=="20 degree stub involute tooth":
            return {
                    "lewisFactor":
                                    {
                                        "pinion":
                                                "0.175-(0.95/pinionTeeth)",
                                        "gear":
                                                "0.175-(0.95/gearTeeth)"
                                    },
                    "pressureAngle":
                                    "20",
                    "deformationFactor":
                                        "0.115/((1/pinionElasticity)+(1/gearElasticity))"
                    }
    def getGrade(self,grade):
        if grade=="1":
            constant1=0.8;
            constant2=0.06;
        if grade=="2":
            constant1=1.25;
            constant2=0.10;
        if grade=="3":
            constant1=2.0;
            constant2=0.16;
        if grade=="4":
            constant1=3.2;
            constant2=0.25;
        if grade=="5"
            constant1=5.0;
            constant2=0.4;
        if grade=="6":
            constant1=8.0;
            constant2=0.63;
        if grade=="7":
            constant1=11.0;
            constant2=0.9;
        if grade=="8":
            constant1=16.0;
            constant2=1.25;
        if grade=="9":
            constant1=22.0;
            constant2=1.80;
        if grade=="10":
            constant1=32.0;
            constant2=2.5;
        if grade=="11":
            constant1=45.0;
            constant2=3.55;
        if grade=="12":
            constant1=63.0;
            constant2=5.0;
    def evalTolerance(self,module,teeth,constant1,constant2):
        phi=module+0.25*math.sqrt(module*teeth);
        error=constant1+constant2*phi;
        return (error/1000);
    def evalLoad(self,module):
        self.getData();
        faceWidth=10*module;
        pitch=Math.pi*module;
        pinionBendingLoad=pinionBendingStressMax*faceWidth*pinionLewisFactor*pitch;
        gearBendingLoad=gearBendingStressMax*faceWidth*gearLewisFactor*pitch;
        if(pinionBendingLoad<gearBendingLoad):
            bendingLoad=pinionBendingLoad;
        else:
            bendingLoad=gearBendingLoad;
        pitchVelocity=Math.pi*pinionTeeth*module*pinionRpm/(60*1000);
        tangentialLoad=power/pitchVelocity;
        gearError=self.evalTolerance(module,gearTeeth,constant1,constant2);
        pinionError=self.evalTolerance(module,pinionTeeth,constant1,constant2);
        error=gearError+pinionError;
        sF=serviceFactor;
        tL=tangentialLoad;
        pV=pitchVelocity;
        dF=deformationFactor;
        e=error;
        fW=faceWidth;
        effectiveLoad=sF*tL+((21*pV*(dF*e*fW+tL))/(21*pV+Math.sqrt(dF*e*fW+tL)));
        safetyFactor=bendingLoad/effectiveLoad;
        return pinionBendingLoad, gearBendingLoad, safetyFactor, effectiveLoad;
    def findModule(self):
        self.getData();
        safetyFactor=0.0;
        i=0;
        while(safetyFactorMin>=safetyFactor):
            pinionBendingLoad, gearBendingLoad, safetyFactor, effectiveLoad=self.evalLoad(MODULES[i]);
            i++;
        wearLoad=effectiveLoad*safetyFactorMin;
        wL=wearLoad;
        pT=pinionTeeth;
        m=MODULES(i-1);
        g=gearing;
        pA=pressureAngle;
        pE=pinionElasticity;
        gE=gearElasticity;
        sinpA=Math.sin(Math.radians(pA));
        cospA=Math.cos(Math.radians(pA));
        contactStress=Math.sqrt((wL/(10*pT*(m^2)*g))*(1.4/sinpA*cospA*((1/pE)+(1/gE)))));
        caseHardness=contactStress/2.65;
