import os;
import threading;
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
    def createThread(target,threadName,modelWindow=None,homeWindow=None,arguments=None):
        if(isinstance(target,str)):
            command=lambda:os.system("freecad "+target);
            thread=threading.Thread(target=command,name=threadName);
            thread.start();
            modelWindow.close();
            homeWindow.hide();
            thread.join();
            homeWindow.show();
        else:
            thread=threading.Thread(target=target,name=threadName,args=arguments);
            thread.start();
