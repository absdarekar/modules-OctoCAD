# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ModuleGui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class ModuleGui(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 470)
        MainWindow.setMinimumSize(QtCore.QSize(600, 470))
        MainWindow.setMaximumSize(QtCore.QSize(600, 470))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(600, 470))
        self.centralwidget.setMaximumSize(QtCore.QSize(600, 470))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 580, 450))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gear = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.gear.setMaximumSize(QtCore.QSize(16777215, 25))
        self.gear.setObjectName("gear")
        self.verticalLayout_2.addWidget(self.gear)
        self.spurGear = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.spurGear.setObjectName("spurGear")
        self.verticalLayout_2.addWidget(self.spurGear)
        self.helicalGear = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.helicalGear.setObjectName("helicalGear")
        self.verticalLayout_2.addWidget(self.helicalGear)
        self.bevelGear = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        self.bevelGear.setObjectName("bevelGear")
        self.verticalLayout_2.addWidget(self.bevelGear)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Modules"))
        self.gear.setText(_translate("MainWindow", "Gear"))
        self.spurGear.setText(_translate("MainWindow", "Spur Gear"))
        self.helicalGear.setText(_translate("MainWindow", "Helical Gear"))
        self.bevelGear.setText(_translate("MainWindow", "Bevel Gear"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ModuleGui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
