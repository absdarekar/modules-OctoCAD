import os;
from PyQt5 import QtCore, QtGui, QtWidgets;
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
