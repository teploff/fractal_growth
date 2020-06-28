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
        MainWindow.resize(658, 452)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout_5.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout_5.setSpacing(6)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(6)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_4.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_4.setSpacing(6)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(6)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(6)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSpacing(6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.sb_fractal_depth = QtWidgets.QSpinBox(self.groupBox_2)
        self.sb_fractal_depth.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_fractal_depth.setMinimum(1)
        self.sb_fractal_depth.setMaximum(10)
        self.sb_fractal_depth.setObjectName("sb_fractal_depth")
        self.verticalLayout_4.addWidget(self.sb_fractal_depth)
        self.dsb_max_line_legth = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.dsb_max_line_legth.setMinimum(0.01)
        self.dsb_max_line_legth.setMaximum(1.0)
        self.dsb_max_line_legth.setSingleStep(0.01)
        self.dsb_max_line_legth.setProperty("value", 0.05)
        self.dsb_max_line_legth.setObjectName("dsb_max_line_legth")
        self.verticalLayout_4.addWidget(self.dsb_max_line_legth)
        self.horizontalLayout_4.addLayout(self.verticalLayout_4)
        self.horizontalLayout_6.addWidget(self.groupBox_2)
        self.groupBox = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_2.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.pb_line_color = QtWidgets.QPushButton(self.groupBox)
        self.pb_line_color.setText("")
        self.pb_line_color.setObjectName("pb_line_color")
        self.verticalLayout_2.addWidget(self.pb_line_color)
        self.pb_background_color = QtWidgets.QPushButton(self.groupBox)
        self.pb_background_color.setStyleSheet("QWidget { background-color: rgb(46, 52, 54) }")
        self.pb_background_color.setText("")
        self.pb_background_color.setObjectName("pb_background_color")
        self.verticalLayout_2.addWidget(self.pb_background_color)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout_6.addWidget(self.groupBox)
        self.verticalLayout_5.addLayout(self.horizontalLayout_6)
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralWidget)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_7.setContentsMargins(11, 11, 11, 11)
        self.horizontalLayout_7.setSpacing(6)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_5 = QtWidgets.QLabel(self.groupBox_3)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_5.addWidget(self.label_5)
        self.sb_draw_latency = QtWidgets.QSpinBox(self.groupBox_3)
        self.sb_draw_latency.setAlignment(QtCore.Qt.AlignCenter)
        self.sb_draw_latency.setMinimum(0)
        self.sb_draw_latency.setMaximum(1000)
        self.sb_draw_latency.setSingleStep(100)
        self.sb_draw_latency.setProperty("value", 0)
        self.sb_draw_latency.setObjectName("sb_draw_latency")
        self.horizontalLayout_5.addWidget(self.sb_draw_latency)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_5)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.pb_engender_fractal = QtWidgets.QPushButton(self.groupBox_3)
        self.pb_engender_fractal.setObjectName("pb_engender_fractal")
        self.verticalLayout_6.addWidget(self.pb_engender_fractal)
        self.pb_build_point_path = QtWidgets.QPushButton(self.groupBox_3)
        self.pb_build_point_path.setObjectName("pb_build_point_path")
        self.verticalLayout_6.addWidget(self.pb_build_point_path)
        self.horizontalLayout_7.addLayout(self.verticalLayout_6)
        self.verticalLayout_5.addWidget(self.groupBox_3)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 658, 22))
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
        self.groupBox_2.setTitle(_translate("MainWindow", "Конфигурация фрактала"))
        self.label.setText(_translate("MainWindow", "Глубина фрактала"))
        self.label_2.setText(_translate("MainWindow", "Max значение длины отрезка"))
        self.groupBox.setTitle(_translate("MainWindow", "Палитра цветов"))
        self.label_3.setText(_translate("MainWindow", "Цвет отрезков"))
        self.label_4.setText(_translate("MainWindow", "Цвет фона"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Построение"))
        self.label_5.setText(_translate("MainWindow", "Задержка при отрисовке, мс"))
        self.pb_engender_fractal.setText(_translate("MainWindow", "Фрактал"))
        self.pb_build_point_path.setText(_translate("MainWindow", "Траектория роста точек"))
