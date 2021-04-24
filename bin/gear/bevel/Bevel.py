import os;
import math;
import pickle;
import threading;
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.gear.bevel.DesignGui import DesignGui;
from gui.octocad.OutputGui import OutputGui;
from bin.Utility import Utility;
from bin.gear.DesignData import DesignData;
class Bevel():
    def __init__(self,octocadFilesPath,octocadAppdataPath,homeWindow,moduleWindow):
        self.octocadFilesPath=octocadFilesPath;
        self.octocadAppdataPath=octocadAppdataPath;
        self.homeWindow=homeWindow;
        self.moduleWindow=moduleWindow;
        self.octocadBevelDesignDataPath=self.octocadAppdataPath+"/gear/bevel/";
        os.makedirs(self.octocadBevelDesignDataPath,exist_ok=True);
        self.octocadBevelModelDataPath=self.octocadBevelDesignDataPath+"model";
        self.octocadBevelDesignDataPath+="design";
    def setupDesignUi(self):
        self.dialog=QtWidgets.QDialog();
        Utility.alignToCenter(self.dialog);
        self.designGui=DesignGui();
        self.designGui.setupUi(self.dialog);
        self.dialog.show();
        self.moduleWindow.close();
        self.designGui.buttonBox.accepted.connect(self.findModule);
    def setupOutputUi(self):
        self.outputWindow=QtWidgets.QMainWindow();
        Utility.alignToCenter(self.outputWindow);
        self.outputGui=OutputGui();
        self.outputGui.setupUi(self.outputWindow);
        self.outputWindow.setWindowTitle("Design of bevel gear");
        self.outputGui.plainTextEdit.setPlainText(open(self.octocadBevelDesignDataPath).read());
        self.outputWindow.show();
        close=self.outputGui.buttonBox.button(QtWidgets.QDialogButtonBox.Close);
        close.clicked.connect(self.outputWindow.close);
        save=self.outputGui.buttonBox.button(QtWidgets.QDialogButtonBox.Save);
        save.clicked.connect(self.save);
    def getDesignData(self):
        self.gearElasticity=float(self.designGui.gearElasticity.text());
        self.gearStrength=float(self.designGui.gearStrength.text());
        self.gearBendingStress=1/3*self.gearStrength;
        self.gearTeeth=float(self.designGui.gearTeeth.text());
        gearTeeth=self.gearTeeth;
        self.pinionElasticity=float(self.designGui.pinionElasticity.text());
        self.pinionRpm=float(self.designGui.pinionRpm.text());
        self.pinionStrength=float(self.designGui.pinionStrength.text());
        self.pinionBendingStress=1/3*self.pinionStrength;
        self.pinionTeeth=float(self.designGui.pinionTeeth.text());
        pinionTeeth=self.pinionTeeth;
        gearRatio=gearTeeth/pinionTeeth;
        self.gearPitchAngle=math.atan(gearRatio);
        self.pinionPitchAngle=math.pi/2-self.gearPitchAngle;
        self.gearVirtualTeeth=gearTeeth/math.cos(self.gearPitchAngle);
        self.pinionVirtualTeeth=pinionTeeth/math.cos(self.pinionPitchAngle);
        self.power=float(self.designGui.power.text());
        self.safetyFactorMin=float(self.designGui.safetyFactor.text());
        self.serviceFactor=float(self.designGui.serviceFactor.text());
        gearing=self.designGui.gearing.currentText();
        self.gearing, self.gearingType=DesignData.evalGearing(gearing,self.gearVirtualTeeth,self.pinionVirtualTeeth);
        self.grade=self.designGui.grade.currentText();
        profile=self.designGui.profile.currentText();
        profile=DesignData.evalProfile(profile);
        self.deformationFactor=eval(profile["deformationFactor"]);
        self.gearLewisFactor=eval(profile["lewisFactor"]["gear"]);
        self.pinionLewisFactor=eval(profile["lewisFactor"]["pinion"]);
        self.pressureAngle=float(profile["pressureAngle"]);
        self.profile=profile["profile"];
    def evalLoad(self,module):
        coneDistance=math.sqrt(((module*self.pinionTeeth/2)**2)+((module*self.gearTeeth/2)**2));
        self.faceWidth=min(10*module,coneDistance/3);
        pitch=math.pi*module;
        pinionBendingLoad=self.pinionBendingStress*self.faceWidth*self.pinionLewisFactor*pitch*(1-self.faceWidth/coneDistance);
        gearBendingLoad=self.gearBendingStress*self.faceWidth*self.gearLewisFactor*pitch*(1-self.faceWidth/coneDistance);
        if(pinionBendingLoad<gearBendingLoad):
            bendingLoad=pinionBendingLoad;
        else:
            bendingLoad=gearBendingLoad;
        pitchVelocity=math.pi*self.pinionTeeth*module*self.pinionRpm/(60*1000);
        tangentialLoad=self.power/pitchVelocity;
        error=DesignData.getTolerance(module,self.grade);
        effectiveLoad=self.serviceFactor*tangentialLoad+((21*pitchVelocity*\
                        (self.deformationFactor*error*self.faceWidth+tangentialLoad))/\
                        (21*pitchVelocity+math.sqrt(self.deformationFactor*error*\
                        self.faceWidth+tangentialLoad)));
        safetyFactor=bendingLoad/effectiveLoad;
        return pinionBendingLoad, gearBendingLoad, safetyFactor, effectiveLoad;
    def findModule(self):
        self.getDesignData();
        self.safetyFactor=0.0;
        i=0;
        while(self.safetyFactorMin>=self.safetyFactor):
            self.pinionBendingLoad, self.gearBendingLoad, self.safetyFactor, \
            self.effectiveLoad=self.evalLoad(DesignData.MODULES[i]);
            i+=1;
        self.module=DesignData.MODULES[i-1];
        self.wearLoad=self.effectiveLoad*self.safetyFactorMin;
        self.contactStress=math.sqrt((self.wearLoad/(DesignData.MODULES[i-1]*\
                            self.pinionTeeth*((3*self.faceWidth)/(4*\
                            math.cos(self.pinionPitchAngle)))*self.gearing))*\
                            (1.4/(math.sin(math.radians(self.pressureAngle))*\
                            math.cos(math.radians(self.pressureAngle))*\
                            ((1/self.pinionElasticity)+(1/self.gearElasticity)))));
        self.caseHardness=self.contactStress/2.65;
        self.createResult();
    def createResult(self):
        URL="https://github.com/absdarekar/OctoCAD/blob/"+\
            "master/doc/gear/bevel/Technical-Summary.pdf";
        with open(self.octocadBevelDesignDataPath,"w") as design_f:
            with open(self.octocadFilesPath+"/LICENSE.md","r") as license_f:
                design_f.write("\n\n\nDESIGN OF BEVEL GEAR GENERATED USING OctoCAD©");
                design_f.write("\n\n\nEND USER AGREEMENT\n\n\n");
                design_f.write(license_f.read());
                design_f.write("\n\n\nRESULTS\n\n\n");
                design_f.write("Ultimate tensile strength of pinion is "+\
                                str(self.pinionStrength)+" N.mm^-2\n\n");
                design_f.write("Ultimate tensile strength of gear is "+\
                                str(self.gearStrength)+" N.mm^-2\n\n");
                design_f.write("Modulus of elasticity of pinion is "+\
                                str(self.pinionElasticity)+" N.mm^-2\n\n");
                design_f.write("Modulus of elasticity of gear is "+\
                                str(self.gearElasticity)+" N.mm^-2\n\n");
                design_f.write("Grade of gear pair is "+str(self.grade)+"\n\n");
                design_f.write("Pressure angle of gear pair is "+\
                                str(self.pressureAngle)+" degree\n\n");
                design_f.write("Pitch angle of pinion is "+\
                                str(math.degrees(self.pinionPitchAngle))+" degree\n\n");
                design_f.write("Pitch angle of gear is "+\
                                str(math.degrees(self.gearPitchAngle))+" degree\n\n");
                design_f.write(self.profile+"\n\n");
                design_f.write(self.gearingType+"\n\n");
                design_f.write("Number of pinion teeth is "+str(self.pinionTeeth)+"\n\n");
                design_f.write("Number of gear teeth is "+str(self.gearTeeth)+"\n\n");
                design_f.write("Power transmitted by gear pair is "+\
                                str(+self.power)+" W\n\n");
                design_f.write("Speed of rotation of pinion is "+\
                                str(self.pinionRpm)+" rpm\n\n");
                design_f.write("Required factor of safety is "+\
                                str(self.safetyFactorMin)+"\n\n");
                design_f.write("Service factor is "+str(self.serviceFactor)+"\n\n");
                design_f.write("\n\n\nParameters for gear pair satisfying given design requirments:\n\n\n");
                design_f.write("Module is "+str(self.module)+" mm\n\n");
                design_f.write("Face width is "+str(self.faceWidth)+" mm\n\n");
                design_f.write("Available factor of safety  is "+\
                                str(self.safetyFactor)+"\n\n");
                design_f.write("Effective load on gear pair is "+\
                                str(self.effectiveLoad)+" N\n\n");
                design_f.write("Bending load capacity of pinion is "+\
                                str(self.pinionBendingLoad)+" N\n\n");
                design_f.write("Bending load capacity of gear is "+\
                                str(self.gearBendingLoad)+" N\n\n");
                design_f.write("Wear load capacity of gear pair is "+\
                                str(self.wearLoad)+" N\n\n");
                design_f.write("Required case hardness of the gear pair is "+\
                                str(self.caseHardness)+" BHN\n\n");
                design_f.write("\n\n\nFor technical summary refer "+URL);
        self.setupOutputUi();
    def save(self):
        Utility.saveFile(self.octocadBevelDesignDataPath);
