# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(597, 400)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.dsb_max_line_legth = QtWidgets.QDoubleSpinBox(self.centralWidget)
        self.dsb_max_line_legth.setGeometry(QtCore.QRect(250, 100, 63, 26))
        self.dsb_max_line_legth.setMinimum(0.01)
        self.dsb_max_line_legth.setMaximum(1.0)
        self.dsb_max_line_legth.setSingleStep(0.01)
        self.dsb_max_line_legth.setProperty("value", 0.05)
        self.dsb_max_line_legth.setObjectName("dsb_max_line_legth")
        self.pb_line_color = QtWidgets.QPushButton(self.centralWidget)
        self.pb_line_color.setGeometry(QtCore.QRect(30, 160, 111, 25))
        self.pb_line_color.setObjectName("pb_line_color")
        self.pb_background_color = QtWidgets.QPushButton(self.centralWidget)
        self.pb_background_color.setGeometry(QtCore.QRect(180, 160, 89, 25))
        self.pb_background_color.setObjectName("pb_background_color")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 209, 17))
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(40, 60, 129, 17))
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.sb_fractal_depth = QtWidgets.QSpinBox(self.centralWidget)
        self.sb_fractal_depth.setGeometry(QtCore.QRect(180, 60, 42, 26))
        self.sb_fractal_depth.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_fractal_depth.setMinimum(1)
        self.sb_fractal_depth.setMaximum(10)
        self.sb_fractal_depth.setObjectName("sb_fractal_depth")
        self.pb_engender_fractal = QtWidgets.QPushButton(self.centralWidget)
        self.pb_engender_fractal.setGeometry(QtCore.QRect(94, 240, 80, 25))
        self.pb_engender_fractal.setObjectName("pb_engender_fractal")
        self.pb_build_point_path = QtWidgets.QPushButton(self.centralWidget)
        self.pb_build_point_path.setGeometry(QtCore.QRect(180, 240, 178, 25))
        self.pb_build_point_path.setObjectName("pb_build_point_path")
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 597, 22))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pb_line_color.setText(_translate("MainWindow", "Цвет прямых"))
        self.pb_background_color.setText(_translate("MainWindow", "Цвет фона"))
        self.label_2.setText(_translate("MainWindow", "Max значение длины отрезка"))
        self.label.setText(_translate("MainWindow", "Глубина фрактала"))
        self.pb_engender_fractal.setText(_translate("MainWindow", "Фрактал"))
        self.pb_build_point_path.setText(_translate("MainWindow", "Траектория роста точек"))
