import time;
from PySide2 import QtWidgets;
from gui.octocad.StatusGui import StatusGui;
class Status():
    def __init__(self):
        self.start=time.time();
        self.statusGui=StatusGui();
        self.status=QtWidgets.QDialog();
        self.statusGui.setupUi(self.status);
        self.status.show();
    def updateStatus(self,message):
        timeStamp=str(round(time.time()-self.start,2))
        self.statusGui.status.append("["+timeStamp+"] "+message);
        QtWidgets.QApplication.processEvents();
