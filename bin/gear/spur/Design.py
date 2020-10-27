import math;
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.Gui import Gui;
from gui.gear.spur.DesignGui import DesignGui;
from gui.octocad.OutputGui import OutputGui;
from bin.Octocad import OCTOCAD_APPDATA_PATH, OCTOCAD_FILES_PATH, saveFile;
OCTOCAD_SPUR_DESIGN_DATA_PATH=OCTOCAD_APPDATA_PATH+"/gear/spur/design";
class Design():
    def setupUi(self):
        self.obj_QDialog__ui=QtWidgets.QDialog();
        Gui.centering(self.obj_QDialog__ui);
        self.obj_DesignGui=DesignGui();
        self.obj_DesignGui.setupUi(self.obj_QDialog__ui);
        self.obj_QDialog__ui.show();
        self.obj_DesignGui.buttonBox.accepted.connect(self.findModule);
    def setupResultUi(self):
        self.obj_QMainWindow__setupResultUi=QtWidgets.QMainWindow();
        Gui.centering(self.obj_QMainWindow__setupResultUi);
        self.obj_OutputGui=OutputGui();
        self.obj_OutputGui.setupUi(self.obj_QMainWindow__setupResultUi);
        self.obj_QMainWindow__setupResultUi.setWindowTitle("Design of spur gear");
        self.obj_OutputGui.plainTextEdit.setPlainText(open(OCTOCAD_SPUR_DESIGN_DATA_PATH).read());
        self.obj_QMainWindow__setupResultUi.show();
        close=self.obj_OutputGui.buttonBox.button(QtWidgets.QDialogButtonBox.Close);
        close.clicked.connect(self.obj_QMainWindow__setupResultUi.close);
        save=self.obj_OutputGui.buttonBox.button(QtWidgets.QDialogButtonBox.Save);
        save.clicked.connect(self.save);
    def getData(self):
        self.MODULES=[1,1.125,1.25,1.375,1.5,1.75,2,2.25,2.5,2.75,3,3.5,4,4.5,5,
                    5.5,6,6.5,7,8,9,10,11,12,14,16,18,20,22,25,28,32,36,40,45,50];
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
        self.gearing, self.gearingType=self.evalGearing(gearing,self.gearTeeth,self.pinionTeeth);
        self.grade=self.obj_DesignGui.grade.currentText();
        self.getGrade(self.grade);
        profile=self.obj_DesignGui.profile.currentText();
        profile=self.evalProfile(profile);
        self.deformationFactor=eval(profile["deformationFactor"]);
        self.gearLewisFactor=eval(profile["lewisFactor"]["gear"]);
        self.pinionLewisFactor=eval(profile["lewisFactor"]["pinion"]);
        self.pressureAngle=float(profile["pressureAngle"]);
        self.profile=profile["profile"];
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
    def evalGearing(self,gearing,gearTeeth,pinionTeeth):
        if gearing=="Internal gearing":
            return ((2*gearTeeth/pinionTeeth)/((gearTeeth/pinionTeeth)-1)), "Internal gearing";
        if gearing=="External gearing":
            return ((2*gearTeeth/pinionTeeth)/((gearTeeth/pinionTeeth)+1)), "External gearing";
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
                                        "0.107/((1/self.pinionElasticity)+(1/self.gearElasticity))",
                    "profile":
                              "Full depth involute tooth"
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
                                        "0.111/((1/self.pinionElasticity)+(1/self.gearElasticity))",
                    "profile":
                              "Full depth involute tooth"
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
                                        "0.115/((1/self.pinionElasticity)+(1/self.gearElasticity))",
                    "profile":
                              "Stub involute tooth"
                    }
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
        self.safetyFactor=0.0;
        i=0;
        while(self.safetyFactorMin>=self.safetyFactor):
            self.pinionBendingLoad, self.gearBendingLoad, self.safetyFactor, self.effectiveLoad=self.evalLoad(self.MODULES[i]);
            i+=1;
        self.module=self.MODULES[i-1];
        self.wearLoad=self.effectiveLoad*self.safetyFactorMin;
        wL=self.wearLoad;
        pT=self.pinionTeeth;
        m=self.MODULES[i-1];
        g=self.gearing;
        pA=self.pressureAngle;
        pE=self.pinionElasticity;
        gE=self.gearElasticity;
        sinpA=math.sin(math.radians(pA));
        cospA=math.cos(math.radians(pA));
        self.contactStress=math.sqrt((wL/(10*pT*(math.pow(m,2))*g))*(1.4/(sinpA*cospA*((1/pE)+(1/gE)))));
        self.caseHardness=self.contactStress/2.65;
        self.createResult();
    def createResult(self):
        with open(OCTOCAD_SPUR_DESIGN_DATA_PATH,"w+") as design_f:
            with open(OCTOCAD_FILES_PATH+"/LICENSE.md","r") as license_f:
                design_f.write(license_f.read());
                design_f.write("\n\n\nDesign of spur gear for given design data:\n\n\n");
                design_f.write("Ultimate tensile strength of pinion is "+str(self.pinionStrength)+" N.mm^-2\n\n");
                design_f.write("Ultimate tensile strength of gear is "+str(self.gearStrength)+" N.mm^-2\n\n");
                design_f.write("Modulus of elasticity of pinion is "+str(self.pinionElasticity)+" N.mm^-2\n\n");
                design_f.write("Modulus of elasticity of gear is "+str(self.gearElasticity)+" N.mm^-2\n\n");
                design_f.write("Grade of gear pair is "+str(self.grade)+"\n\n");
                design_f.write("Pressure angle of gear pair is "+str(self.pressureAngle)+" degree\n\n");
                design_f.write(self.profile+"\n\n");
                design_f.write(self.gearingType+"\n\n");
                design_f.write("Number of pinion teeth is "+str(self.pinionTeeth)+"\n\n");
                design_f.write("Number of gear teeth is "+str(self.gearTeeth)+"\n\n");
                design_f.write("Power transmitted by gear pair is "+str(+self.power)+" W\n\n");
                design_f.write("Speed of rotation of pinion is "+str(self.pinionRpm)+" rpm\n\n");
                design_f.write("Required factor of safety is "+str(self.safetyFactorMin)+"\n\n");
                design_f.write("Service factor is "+str(self.serviceFactor)+"\n\n");
                design_f.write("\n\n\nParameters for gear pair satisfying given design requirments:\n\n\n");
                design_f.write("Module is "+str(self.module)+" mm\n\n");
                design_f.write("Available factor of safety  is "+str(self.safetyFactor)+"\n\n");
                design_f.write("Effective load on gear pair is "+str(self.effectiveLoad)+" N\n\n");
                design_f.write("Bending load capacity of pinion is "+str(self.pinionBendingLoad)+" N\n\n");
                design_f.write("Bending load capacity of gear is "+str(self.gearBendingLoad)+" N\n\n");
                design_f.write("Wear load capacity of gear pair is "+str(self.wearLoad)+" N\n\n");
                design_f.write("Required case hardness of the gear pair is "+str(self.caseHardness)+" BHN\n\n");
                design_f.write("\n\n\nFor technical summary refer https://github.com/absdarekar/OctoCAD/blob/master/doc/gear/spur/Technical-Summary.pdf");
        self.setupResultUi();
    def save(self):
        saveFile(OCTOCAD_SPUR_DESIGN_DATA_PATH);
