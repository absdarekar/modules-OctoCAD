import os;
import threading;
from PyQt5 import QtCore, QtGui, QtWidgets;
from gui.octocad.OutputGui import OutputGui;
class Utility():
    def alignToCenter(argWindow):
        window=argWindow.frameGeometry();
        center=QtWidgets.QDesktopWidget().availableGeometry().center();
        window.moveCenter(center);
        argWindow.move(window.topLeft());
    def saveFile(path):
        file, fileFilter=QtWidgets.QFileDialog.getSaveFileName(caption='',directory=os.path.expanduser('~'));
        with open(file,"w") as file_f:
            with open(path,"r") as appData_f:
                data=appData_f.read();
                file_f.write(data);
    def setupDialog(self,gui,moduleWindow,function):
        self.dialog=QtWidgets.QDialog();
        Utility.alignToCenter(self.dialog);
        gui.setupUi(self.dialog);
        self.dialog.show();
        moduleWindow.close();
        gui.buttonBox.accepted.connect(function);
    def setupOutputUi(self,title,file):
        self.outputWindow=QtWidgets.QMainWindow();
        Utility.alignToCenter(self.outputWindow);
        self.outputGui=OutputGui();
        self.outputGui.setupUi(self.outputWindow);
        self.outputWindow.setWindowTitle(title);
        self.outputGui.plainTextEdit.setPlainText(open(file).read());
        self.outputWindow.show();
        close=self.outputGui.buttonBox.button(QtWidgets.QDialogButtonBox.Close);
        close.clicked.connect(self.outputWindow.close);
        save=self.outputGui.buttonBox.button(QtWidgets.QDialogButtonBox.Save);
        saveFunction=lambda:Utility.saveFile(file);
        save.clicked.connect(saveFunction);
    def runFreecad(path,name,homeWindow):
        command=lambda:os.system("freecad "+path);
        thread=threading.Thread(target=command,name=name);
        thread.start();
        homeWindow.hide();
        thread.join();
        homeWindow.show();
