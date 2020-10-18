#program: Graphical User Interface for the spur gear design module
#author: Atharv Darekar
from PySide2.QtWidgets import (QApplication, QDesktopWidget, QComboBox, QDialog, QMessageBox, QDialogButtonBox,
                               QFormLayout, QGroupBox, QLabel, QDoubleSpinBox, QSpinBox, QVBoxLayout);
from PySide2.QtGui import QIcon, QFont, QDoubleValidator;
import sys;
import os;
class Design(QDialog):
    def __init__(self):
        super(spur_design, self).__init__();
        self.createForm();
        self.buttonBox=QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel);
        self.buttonBox.accepted.connect(self.submit);
        self.buttonBox.rejected.connect(self.reject);
        mainLayout=QVBoxLayout();
        mainLayout.addWidget(self.formGroupBox);
        mainLayout.addWidget(self.buttonBox);
        self.setLayout(mainLayout);
        self.setWindowTitle("OctoCAD\N{COPYRIGHT SIGN}");
        self.setGeometry(0,0,600,400);
        self.setIcon();
        self.centering();
        self.show();
    def setIcon(self):
        icon=QIcon("/home/ubuntu/OctoCAD/icons/logo_transparent_enlarged.png");
        self.setWindowIcon(icon);
    def centering(self):
        window=self.frameGeometry();
        center=QDesktopWidget().availableGeometry().center();
        window.moveCenter(center);
        self.move(window.topLeft());
    def createForm(self):
        self.formGroupBox=QGroupBox("Design Configuration");
        self.layout=QFormLayout();
        self.Sutp=QDoubleSpinBox();
        self.Sutp.setRange(1,10000);
        self.layout.addRow(QLabel("Enter ultimate tensile strength of pinion N.mm^-2"),self.Sutp);
        self.Sutg=QDoubleSpinBox();
        self.Sutg.setRange(1,10000);
        self.layout.addRow(QLabel("Enter ultimate tensile strength of gear N.mm^-2"),self.Sutg);
        self.Ep=QDoubleSpinBox();
        self.Ep.setRange(1,10000000);
        self.layout.addRow(QLabel("Enter modulus of elasticity of pinion N.mm^-2"),self.Ep);
        self.Eg=QDoubleSpinBox();
        self.Eg.setRange(1,10000000);
        self.layout.addRow(QLabel("Enter modulus of elasticity of gear N.mm^-2"),self.Eg);
        self.grade=QComboBox();
        self.grade.addItem("1");
        self.grade.addItem("2");
        self.grade.addItem("3");
        self.grade.addItem("4");
        self.grade.addItem("5");
        self.grade.addItem("6");
        self.grade.addItem("7");
        self.grade.addItem("8");
        self.grade.addItem("9");
        self.grade.addItem("10");
        self.grade.addItem("11");
        self.grade.addItem("12");
        self.layout.addRow(QLabel("Select grade of gear pair"),self.grade);
        self.y=QComboBox();
        self.y.addItem("14.5 degree full depth involute tooth");
        self.y.addItem("20 degree full depth involute tooth");
        self.y.addItem("20 degree stub involute tooth");
        self.layout.addRow(QLabel("Select type of gear pair"),self.y);
        self.zp=QSpinBox();
        self.zp.setRange(14,300);
        self.layout.addRow(QLabel("Enter number of pinion teeth"),self.zp);
        self.zg=QSpinBox();
        self.zg.setRange(14,300);
        self.layout.addRow(QLabel("Enter number of gear teeth"),self.zg);
        self.P=QDoubleSpinBox();
        self.P.setRange(1,1000000);
        self.layout.addRow(QLabel("Enter power transmitted by gear pair W"),self.P);
        self.Np=QDoubleSpinBox();
        self.Np.setRange(1,10000);
        self.layout.addRow(QLabel("Enter speed of pinion rpm"),self.Np);
        self.Q=QComboBox();
        self.Q.addItem("Internal gearing");
        self.Q.addItem("External gearing");
        self.layout.addRow(QLabel("Enter type of gearing"),self.Q);
        self.FOSr=QDoubleSpinBox();
        self.FOSr.setRange(1,10);
        self.layout.addRow(QLabel("Enter factor of safety"),self.FOSr);
        self.cs=QDoubleSpinBox();
        self.layout.addRow(QLabel("Enter service factor"),self.cs);
        self.cs.setRange(1,10);
        self.formGroupBox.setLayout(self.layout);
    def submit(self):
        os.makedirs("/home/ubuntu/.OctoCAD/spur-gear", exist_ok=True);
        with open("/home/ubuntu/.OctoCAD/spur-gear/user_input_design.txt","w") as user_input_design_f:
            user_input_design_f.write("# name: Eg\n# type: scalar\n");
            user_input_design_f.write(self.Eg.text()+"\n\n\n");
            user_input_design_f.write("# name: Ep\n# type: scalar\n");
            user_input_design_f.write(self.Ep.text()+"\n\n\n");
            user_input_design_f.write("# name: FOSr\n# type: scalar\n");
            user_input_design_f.write(self.FOSr.text()+"\n\n\n");
            user_input_design_f.write("# name: Np\n# type: scalar\n");
            user_input_design_f.write(self.Np.text()+"\n\n\n");
            user_input_design_f.write("# name: P\n# type: scalar\n");
            user_input_design_f.write(self.P.text()+"\n\n\n");
            user_input_design_f.write("# name: Q\n# type: scalar\n");
            if self.Q.currentText()=="Internal gearing":
                user_input_design_f.write("1"+"\n\n\n");
            if self.Q.currentText()=="External gearing":
                user_input_design_f.write("2"+"\n\n\n");
            user_input_design_f.write("# name: Sutg\n# type: scalar\n");
            user_input_design_f.write(self.Sutg.text()+"\n\n\n");
            user_input_design_f.write("# name: Sutp\n# type: scalar\n");
            user_input_design_f.write(self.Sutp.text()+"\n\n\n");
            user_input_design_f.write("# name: cs\n# type: scalar\n");
            user_input_design_f.write(self.cs.text()+"\n\n\n");
            user_input_design_f.write("# name: grade\n# type: scalar\n");
            user_input_design_f.write(self.grade.currentText()+"\n\n\n");
            user_input_design_f.write("# name: y\n# type: scalar\n");
            if self.y.currentText()=="14.5 degree full depth involute tooth":
                user_input_design_f.write("1"+"\n\n\n");
            if self.y.currentText()=="20 degree full depth involute tooth":
                user_input_design_f.write("2"+"\n\n\n");
            if self.y.currentText()=="20 degree stub involute tooth":
                user_input_design_f.write("3"+"\n\n\n");
            user_input_design_f.write("# name: zg\n# type: scalar\n");
            user_input_design_f.write(self.zg.text()+"\n\n\n");
            user_input_design_f.write("# name: zp\n# type: scalar\n");
            user_input_design_f.write(self.zp.text()+"\n\n\n");
        os.system("octave /home/ubuntu/OctoCAD/bis/gear/spur-gear/io.m");
        self.createResult();
    def createResult(self):
        with open("/home/ubuntu/.OctoCAD/spur-gear/result.txt","r") as result_f:
            str_Fd=result_f.readline().split("=")[1].rstrip("\n");
            str_Fap=result_f.readline().split("=")[1].rstrip("\n");
            str_Fag=result_f.readline().split("=")[1].rstrip("\n");
            str_Fw=result_f.readline().split("=")[1].rstrip("\n");
            str_BHN=result_f.readline().split("=")[1].rstrip("\n");
            str_m=result_f.readline().split("=")[1].rstrip("\n");
            str_FOS=result_f.readline().split("=")[1].rstrip("\n");
            str_zp=result_f.readline().split("=")[1].rstrip("\n");
            str_zg=result_f.readline().split("=")[1].rstrip("\n");
            str_result="Module of gear pair is "+str_m+" mm\n\nEffective load on the gear pair is "+str_Fd+" N\n\nBending load capacity of pinion is "+str_Fap+" N\n\nBending load capacity of gear "+str_Fag+" N\n\nWear load capacity of gear pair is "+str_Fw+" N\n\nSurface hardness of the gear pair is "+str_BHN+" BHN\n\nAvailabe factor of safety is "+str_FOS+"\n\n";
            result_box=QMessageBox();
            result_box.setWindowTitle("Design of gear pair");
            result_box.setText(str_result);
            result_box.exec_();
            obj_QApplication.exit();
obj_QApplication=QApplication(sys.argv);
obj_spur_design=spur_design();
obj_QApplication.exec_();
sys.exit(0);
