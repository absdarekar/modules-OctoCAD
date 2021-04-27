import os;
import math;
import pickle;
from gui.gear.helical.DesignGui import DesignGui;
from gui.gear.helical.ModelGui import ModelGui;
from gui.octocad.OutputGui import OutputGui;
from bin.Utility import Utility;
from bin.gear.DesignData import DesignData;
class Helical():
    def __init__(self,filesPath,appdataPath,homeWindow,moduleWindow):
        self.filesPath=filesPath;
        self.appdataPath=appdataPath;
        self.homeWindow=homeWindow;
        self.moduleWindow=moduleWindow;
        self.designDataPath=self.appdataPath+"/gear/helical/";
        os.makedirs(self.designDataPath,exist_ok=True);
        self.modelDataPath=self.designDataPath+"model";
        self.designDataPath+="design";
    def setupDesignUi(self):
        self.utilityDesign=Utility();
        self.designGui=DesignGui();
        self.utilityDesign.setupDialog(self.designGui,self.moduleWindow,self.findModule);
    def setupModelUi(self):
        self.utilityModel=Utility()
        self.modelGui=ModelGui();
        self.utilityModel.setupDialog(self.modelGui,self.moduleWindow,self.getModelData);
    def setupOutputUi(self):
        title="Design of helical gear";
        self.utilityDesign.setupOutputUi(title,self.designDataPath);
    def getDesignData(self):
        self.helixAngle=float(self.designGui.helixAngle.text());
        self.gearElasticity=float(self.designGui.gearElasticity.text());
        self.gearStrength=float(self.designGui.gearStrength.text());
        self.gearBendingStress=1/3*self.gearStrength;
        self.gearTeeth=float(self.designGui.gearTeeth.text());
        gearTeeth=self.gearTeeth;
        self.gearVirtualTeeth=gearTeeth/math.pow(math.cos(math.radians(self.helixAngle)),3);
        self.pinionElasticity=float(self.designGui.pinionElasticity.text());
        self.pinionRpm=float(self.designGui.pinionRpm.text());
        self.pinionStrength=float(self.designGui.pinionStrength.text());
        self.pinionBendingStress=1/3*self.pinionStrength;
        self.pinionTeeth=float(self.designGui.pinionTeeth.text());
        pinionTeeth=self.pinionTeeth;
        self.pinionVirtualTeeth=pinionTeeth/math.pow(math.cos(math.radians(self.helixAngle)),3);
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
    def getModelData(self):
        gear="Helical";
        profileType=self.modelGui.profile.currentText();
        profile=DesignData.evalProfile(profileType);
        pressureAngle=float(profile["pressureAngle"]);
        helixAngle=float(self.modelGui.helixAngle.text());
        helixHand=self.modelGui.helixHand.currentText();
        module=float(self.modelGui.module.text());
        teeth=float(self.modelGui.teeth.text());
        gearing=self.modelGui.gearing.currentText();
        faceWidth=float(self.modelGui.faceWidth.text());
        clearance=float(self.modelGui.clearance.text());
        fillet=float(self.modelGui.fillet.text());
        fileName=gear+" "+helixHand+" "+str(teeth)+" "+str(module*teeth)+" mm "\
                +str(module)+" mm";
        modelData=(gear,profileType,pressureAngle,helixAngle,helixHand,module,\
                    teeth,gearing,faceWidth,clearance,fillet,fileName);
        with open(self.modelDataPath,"wb") as model_f:
            pickle.dump(modelData,model_f);
        path=self.filesPath+"/bin/gear/helical/Model.py";
        name="helicalModel";
        Utility.runFreecad(path,name,self.homeWindow);
    def evalLoad(self,module):
        faceWidth=10*module;
        pitch=math.pi*module;
        pinionBendingLoad=self.pinionBendingStress*faceWidth*self.pinionLewisFactor*pitch;
        gearBendingLoad=self.gearBendingStress*faceWidth*self.gearLewisFactor*pitch;
        if(pinionBendingLoad<gearBendingLoad):
            bendingLoad=pinionBendingLoad;
        else:
            bendingLoad=gearBendingLoad;
        pitchVelocity=math.pi*self.pinionTeeth*module*self.pinionRpm/\
                        (60*1000*math.cos(math.radians(self.helixAngle)));
        tangentialLoad=self.power/pitchVelocity;
        moduleTransverse=module/math.cos(math.radians(self.helixAngle));
        gearError=DesignData.evalTolerance(moduleTransverse,self.gearTeeth,self.grade);
        pinionError=DesignData.evalTolerance(moduleTransverse,self.pinionTeeth,self.grade);
        error=gearError+pinionError;
        effectiveLoad=self.serviceFactor*tangentialLoad+((21*pitchVelocity*\
                        (self.deformationFactor*error*faceWidth*\
                        math.pow(math.cos(self.helixAngle),2)+tangentialLoad)*\
                        math.cos(math.radians(self.helixAngle)))/(21*pitchVelocity+\
                        math.sqrt(self.deformationFactor*error*faceWidth*\
                        math.pow(math.cos(self.helixAngle),2)+tangentialLoad)));
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
        self.contactStress=math.sqrt((self.wearLoad*\
                            math.pow(math.cos(math.radians(self.helixAngle)),3)/\
                            (10*self.pinionTeeth*(math.pow(DesignData.MODULES[i-1],2))*\
                            self.gearing))*(1.4/(math.sin(math.radians(self.pressureAngle))*\
                            math.cos(math.radians(self.pressureAngle))*\
                            ((1/self.pinionElasticity)+(1/self.gearElasticity)))));
        self.caseHardness=self.contactStress/2.65;
        self.createResult();
    def createResult(self):
        URL="https://github.com/absdarekar/OctoCAD/blob/"+\
            "master/doc/gear/helical/Technical-Summary.pdf";
        with open(self.designDataPath,"w") as design_f:
            with open(self.filesPath+"/LICENSE.md","r") as license_f:
                design_f.write("\n\n\nDESIGN OF HELICAL GEAR GENERATED USING OctoCAD©");
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
                design_f.write("Helix angle of gear pair is "+\
                                str(self.helixAngle)+" degree\n\n");
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
