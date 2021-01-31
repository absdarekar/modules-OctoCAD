import os;
import threading;
from PyQt5 import QtCore, QtGui, QtWidgets;
from PyQt5.QtWidgets import QFileDialog;
class Utility():
    def saveFile(path):
        file, fileFilter=QFileDialog.getSaveFileName(caption='',directory=os.path.expanduser('~'));
        with open(file,"w") as file_f:
            with open(path,"r") as appData_f:
                data=appData_f.read();
                file_f.write(data);
    def createThread(filePath,threadName,modelUi,octocadUi):
        execute=lambda:os.system("freecad "+filePath);
        thread=threading.Thread(target=execute,name=threadName);
        thread.start();
        modelUi.close();
        octocadUi.hide();
        thread.join();
        octocadUi.show();
