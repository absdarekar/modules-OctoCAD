import math;
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.Gui import Gui;
from gui.gear.helical.DesignGui import DesignGui;
from gui.octocad.OutputGui import OutputGui;
from bin.Octocad import OCTOCAD_APPDATA_PATH, OCTOCAD_FILES_PATH, saveFile;
from bin.gear.DesignData import DesignData;
OCTOCAD_HELICAL_DESIGN_DATA_PATH=OCTOCAD_APPDATA_PATH+"/gear/helical/design";
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
        self.obj_QMainWindow__setupResultUi.setWindowTitle("Design of helical gear");
        self.obj_OutputGui.plainTextEdit.setPlainText(open(OCTOCAD_HELICAL_DESIGN_DATA_PATH).read());
        self.obj_QMainWindow__setupResultUi.show();
        close=self.obj_OutputGui.buttonBox.button(QtWidgets.QDialogButtonBox.Close);
        close.clicked.connect(self.obj_QMainWindow__setupResultUi.close);
        save=self.obj_OutputGui.buttonBox.button(QtWidgets.QDialogButtonBox.Save);
        save.clicked.connect(self.save);
    def getData(self):
        self.helixAngle=float(self.obj_DesignGui.helixAngle.text());
        self.gearElasticity=float(self.obj_DesignGui.gearElasticity.text());
        self.gearStrength=float(self.obj_DesignGui.gearStrength.text());
        self.gearBendingStress=1/3*self.gearStrength;
        self.gearTeeth=float(self.obj_DesignGui.gearTeeth.text());
        gearTeeth=self.gearTeeth;
        self.gearVirtualTeeth=gearTeeth/math.pow(math.cos(math.radians(self.helixAngle)),3);
        self.pinionElasticity=float(self.obj_DesignGui.pinionElasticity.text());
        self.pinionRpm=float(self.obj_DesignGui.pinionRpm.text());
        self.pinionStrength=float(self.obj_DesignGui.pinionStrength.text());
        self.pinionBendingStress=1/3*self.pinionStrength;
        self.pinionTeeth=float(self.obj_DesignGui.pinionTeeth.text());
        pinionTeeth=self.pinionTeeth;
        self.pinionVirtualTeeth=pinionTeeth/math.pow(math.cos(math.radians(self.helixAngle)),3);
        self.power=float(self.obj_DesignGui.power.text());
        self.safetyFactorMin=float(self.obj_DesignGui.safetyFactor.text());
        self.serviceFactor=float(self.obj_DesignGui.serviceFactor.text());
        gearing=self.obj_DesignGui.gearing.currentText();
        self.gearing, self.gearingType=DesignData.evalGearing(gearing,self.gearVirtualTeeth,self.pinionVirtualTeeth);
        self.grade=self.obj_DesignGui.grade.currentText();
        profile=self.obj_DesignGui.profile.currentText();
        profile=DesignData.evalProfile(profile);
        self.deformationFactor=eval(profile["deformationFactor"]);
        self.gearLewisFactor=eval(profile["lewisFactor"]["gear"]);
        self.pinionLewisFactor=eval(profile["lewisFactor"]["pinion"]);
        self.pressureAngle=float(profile["pressureAngle"]);
        self.profile=profile["profile"];
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
        self.getData();
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
        with open(OCTOCAD_HELICAL_DESIGN_DATA_PATH,"w+") as design_f:
            with open(OCTOCAD_FILES_PATH+"/LICENSE.md","r") as license_f:
                design_f.write(license_f.read());
                design_f.write("\n\n\nDesign of helical gear for given design data:\n\n\n");
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
        self.setupResultUi();
    def save(self):
        saveFile(OCTOCAD_HELICAL_DESIGN_DATA_PATH);
