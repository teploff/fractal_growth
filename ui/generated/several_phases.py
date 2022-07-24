# Form implementation generated from reading ui file 'ui/static/several_phases.ui'
#
# Created by: PyQt6 UI code generator 6.3.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(389, 332)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralWidget)
        self.verticalLayout.setContentsMargins(11, 11, 11, 11)
        self.verticalLayout.setSpacing(6)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setSpacing(6)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem)
        self.sb_fractal_depth = QtWidgets.QSpinBox(self.centralWidget)
        self.sb_fractal_depth.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sb_fractal_depth.setMinimum(1)
        self.sb_fractal_depth.setMaximum(10)
        self.sb_fractal_depth.setObjectName("sb_fractal_depth")
        self.horizontalLayout_5.addWidget(self.sb_fractal_depth)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(6)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_9.addWidget(self.label_4)
        spacerItem1 = QtWidgets.QSpacerItem(18, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem1)
        self.dsb_max_line_legth = QtWidgets.QDoubleSpinBox(self.centralWidget)
        self.dsb_max_line_legth.setMinimum(0.01)
        self.dsb_max_line_legth.setMaximum(1.0)
        self.dsb_max_line_legth.setSingleStep(0.01)
        self.dsb_max_line_legth.setProperty("value", 0.05)
        self.dsb_max_line_legth.setObjectName("dsb_max_line_legth")
        self.horizontalLayout_9.addWidget(self.dsb_max_line_legth)
        self.verticalLayout.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setSpacing(6)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.l_single_phase_count_iterations_2 = QtWidgets.QLabel(self.centralWidget)
        self.l_single_phase_count_iterations_2.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.l_single_phase_count_iterations_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.l_single_phase_count_iterations_2.setObjectName("l_single_phase_count_iterations_2")
        self.horizontalLayout_15.addWidget(self.l_single_phase_count_iterations_2)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_15.addItem(spacerItem2)
        self.sb_count_iterations = QtWidgets.QSpinBox(self.centralWidget)
        self.sb_count_iterations.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.sb_count_iterations.setMinimum(1)
        self.sb_count_iterations.setMaximum(200)
        self.sb_count_iterations.setSingleStep(5)
        self.sb_count_iterations.setProperty("value", 40)
        self.sb_count_iterations.setObjectName("sb_count_iterations")
        self.horizontalLayout_15.addWidget(self.sb_count_iterations)
        self.verticalLayout.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setSpacing(6)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.centralWidget)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        spacerItem3 = QtWidgets.QSpacerItem(13, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem3)
        self.dsb_angle = QtWidgets.QDoubleSpinBox(self.centralWidget)
        self.dsb_angle.setMinimum(1.0)
        self.dsb_angle.setMaximum(89.0)
        self.dsb_angle.setSingleStep(0.1)
        self.dsb_angle.setProperty("value", 45.0)
        self.dsb_angle.setObjectName("dsb_angle")
        self.horizontalLayout_10.addWidget(self.dsb_angle)
        self.verticalLayout.addLayout(self.horizontalLayout_10)
        self.lb_image = QtWidgets.QLabel(self.centralWidget)
        self.lb_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.lb_image.setObjectName("lb_image")
        self.verticalLayout.addWidget(self.lb_image)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setSpacing(6)
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.l_several_phase_coefficient_a_2 = QtWidgets.QLabel(self.centralWidget)
        self.l_several_phase_coefficient_a_2.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.l_several_phase_coefficient_a_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.l_several_phase_coefficient_a_2.setObjectName("l_several_phase_coefficient_a_2")
        self.horizontalLayout_21.addWidget(self.l_several_phase_coefficient_a_2)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_21.addItem(spacerItem4)
        self.dsb_several_phase_coefficient_a = QtWidgets.QDoubleSpinBox(self.centralWidget)
        self.dsb_several_phase_coefficient_a.setMinimum(0.01)
        self.dsb_several_phase_coefficient_a.setMaximum(1.0)
        self.dsb_several_phase_coefficient_a.setSingleStep(0.01)
        self.dsb_several_phase_coefficient_a.setProperty("value", 0.5)
        self.dsb_several_phase_coefficient_a.setObjectName("dsb_several_phase_coefficient_a")
        self.horizontalLayout_21.addWidget(self.dsb_several_phase_coefficient_a)
        self.verticalLayout.addLayout(self.horizontalLayout_21)
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_22.setSpacing(6)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        self.l_several_phase_coefficient_h_2 = QtWidgets.QLabel(self.centralWidget)
        self.l_several_phase_coefficient_h_2.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.l_several_phase_coefficient_h_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.l_several_phase_coefficient_h_2.setObjectName("l_several_phase_coefficient_h_2")
        self.horizontalLayout_22.addWidget(self.l_several_phase_coefficient_h_2)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_22.addItem(spacerItem5)
        self.dsb_several_phase_coefficient_h = QtWidgets.QDoubleSpinBox(self.centralWidget)
        self.dsb_several_phase_coefficient_h.setMinimum(0.01)
        self.dsb_several_phase_coefficient_h.setMaximum(1.0)
        self.dsb_several_phase_coefficient_h.setSingleStep(0.01)
        self.dsb_several_phase_coefficient_h.setProperty("value", 0.1)
        self.dsb_several_phase_coefficient_h.setObjectName("dsb_several_phase_coefficient_h")
        self.horizontalLayout_22.addWidget(self.dsb_several_phase_coefficient_h)
        self.verticalLayout.addLayout(self.horizontalLayout_22)
        self.pb_calculate_fractal = QtWidgets.QPushButton(self.centralWidget)
        self.pb_calculate_fractal.setObjectName("pb_calculate_fractal")
        self.verticalLayout.addWidget(self.pb_calculate_fractal)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 389, 22))
        self.menuBar.setObjectName("menuBar")
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtWidgets.QToolBar(MainWindow)
        self.mainToolBar.setObjectName("mainToolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Размах фрактала от количества фаз"))
        self.label_3.setText(_translate("MainWindow", "Глубина фрактала"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p>Max значение длины отрезка <span style=\" font-style:italic;\">a</span></p></body></html>"))
        self.l_single_phase_count_iterations_2.setText(_translate("MainWindow", "<html><head/><body><p>Количество итераций роста отрезка <span style=\" font-style:italic;\">a</span></p></body></html>"))
        self.label_10.setText(_translate("MainWindow", "Значение угла треугольника"))
        self.lb_image.setText(_translate("MainWindow", "Image"))
        self.l_several_phase_coefficient_a_2.setText(_translate("MainWindow", "<html><head/><body><p>Коэффициент начальной длины отрезка <span style=\" font-style:italic;\">a</span></p></body></html>"))
        self.l_several_phase_coefficient_h_2.setText(_translate("MainWindow", "<html><head/><body><p>Коэффициент начальной длины отрезка <span style=\" font-style:italic;\">h</span></p></body></html>"))
        self.pb_calculate_fractal.setText(_translate("MainWindow", "Вычислить"))
