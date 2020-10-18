# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'HomeGui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class HomeGui(object):
    def setupUi(self, MainWindow,path):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(600, 470)
        MainWindow.setMinimumSize(QtCore.QSize(600, 470))
        MainWindow.setMaximumSize(QtCore.QSize(600, 470))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(path+"/icon/logo.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.design = QtWidgets.QPushButton(self.groupBox)
        self.design.setMinimumSize(QtCore.QSize(0, 200))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(path+"/icon/design.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.design.setIcon(icon1)
        self.design.setIconSize(QtCore.QSize(80, 80))
        self.design.setObjectName("design")
        self.gridLayout.addWidget(self.design, 0, 0, 1, 1)
        self.model = QtWidgets.QPushButton(self.groupBox)
        self.model.setMinimumSize(QtCore.QSize(0, 200))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(path+"/icon/3d-modeling.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.model.setIcon(icon2)
        self.model.setIconSize(QtCore.QSize(80, 80))
        self.model.setObjectName("model")
        self.gridLayout.addWidget(self.model, 0, 1, 1, 1)
        self.help = QtWidgets.QPushButton(self.groupBox)
        self.help.setMinimumSize(QtCore.QSize(0, 200))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(path+"/icon/information.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.help.setIcon(icon3)
        self.help.setIconSize(QtCore.QSize(80, 80))
        self.help.setObjectName("help")
        self.gridLayout.addWidget(self.help, 1, 0, 1, 1)
        self.about = QtWidgets.QPushButton(self.groupBox)
        self.about.setMinimumSize(QtCore.QSize(0, 200))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(path+"/icon/about-us.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.about.setIcon(icon4)
        self.about.setIconSize(QtCore.QSize(80, 80))
        self.about.setObjectName("about")
        self.gridLayout.addWidget(self.about, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.groupBox)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "OctoCAD©"))
        self.groupBox.setTitle(_translate("MainWindow", "Select"))
        self.design.setText(_translate("MainWindow", "Design"))
        self.model.setText(_translate("MainWindow", "Generate 3-D model"))
        self.help.setText(_translate("MainWindow", "Help"))
        self.about.setText(_translate("MainWindow", "About Us"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = HomeGui()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
