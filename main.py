from typing import List, Tuple
import pygame
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui, QtCore
from ui.main_window import Ui_MainWindow
from OpenGL.GL import *
# from OpenGL.GLU import *
from geometry.entity_2d import Segment
from fractals.koch.curve import Curve
from PIL import Image, ImageOps
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from functools import wraps
from pathlib import Path

SCROLL_UP = 4
SCROLL_DOWN = 5
HEIGHT = 1000
WIDTH = 1000

display = (WIDTH, HEIGHT)

MAX_LINE_LENGTH = 0.05
N_ITER = 20
BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)


def is_calculations_absent(f):
    """
    Вычисления фрактальной структуры отсутствуют?
    :return:
    """

    @wraps(f)
    def _impl(self):
        """
        Вычисления фрактальной структуры отсутствуют?
        :param self:
        :return:
        """
        if self.koch_curve is None:
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText('Ошибка')
            msg.setInformativeText('Вычисления отсутсвуют. Необходимо вычислить фрактал!')
            msg.setWindowTitle('Error')
            msg.exec_()
        else:
            f(self)
    return _impl


class Application(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        # initialize components from generated design.py
        super().__init__()
        self.setupUi(self)

        self.koch_curve = None
        self.export_folder_path = None

        # make default settings
        self.error_dialog = QtWidgets.QErrorMessage()
        self.rgb_lines = BLACK
        self.rgb_background = WHITE
        self.l_image.setPixmap(QtGui.QPixmap("./static/single_phase_model.png"))
        self.lb_regular_polygon_count_angle.setHidden(True)
        self.sb_regular_polygon_count_angle.setHidden(True)
        self.rb_regular_polygon_build_inside.setHidden(True)
        self.rb_regular_polygon_build_outside.setHidden(True)
        self.l_several_phase_coefficient_a.setHidden(True)
        self.dsb_several_phase_coefficient_a.setHidden(True)
        self.l_several_phase_coefficient_h.setHidden(True)
        self.dsb_several_phase_coefficient_h.setHidden(True)
        self.l_several_phase_count_iterations.setHidden(True)
        self.sb_several_phase_count_iterations.setHidden(True)

        pygame.init()

        # callbacks
        self.pb_calculate_fractal.clicked.connect(self._calculation_fractal)
        self.pb_visualize.clicked.connect(self._visualize_fractal_growth)
        self.pb_build_point_path.clicked.connect(self._visualize_point_path_growth)
        self.pb_thin_out.clicked.connect(self._visualize_thin_out_fractal_growth)
        self.pb_line_color.clicked.connect(self._pick_lines_color)
        self.pb_background_color.clicked.connect(self._pick_background_color)
        self.rb_single_phase.clicked.connect(self._enable_single_phase)
        self.rb_several_phases.clicked.connect(self._several_phases)
        self.rb_regular_polygon.clicked.connect(self._enable_regular_polygon)
        self.cb_screenshot.clicked.connect(self._make_screenshot)
        self.pb_screenshot_path.clicked.connect(self._choose_file_path)
        self.pb_graph_line_len.clicked.connect(self._plot_graph_line_len)
        self.pb_graph_line_len_one_and_several_phases.clicked.connect(self._plot_graph_line_len_one_and_several_phases)
        self.pb_graph_scale.clicked.connect(self._plot_graph_scale)
        self.pb_graph_scale_one_and_several_phases.clicked.connect(self._plot_graph_scale_one_and_several_phases)
        self.pb_graph_angle.clicked.connect(self._plot_graph_angle)

    def _calculation_fractal(self):
        """
        Вычислить фрактальную структуру.
        :return:
        """
        settings = dict()
        if self.rb_single_phase.isChecked():
            settings["model"] = "single"
            settings["count_iterations"] = self.sb_single_phase_count_iterations.value()
        elif self.rb_several_phases.isChecked():
            settings["model"] = "several"
            settings["coefficient_a"] = self.dsb_several_phase_coefficient_a.value()
            settings["coefficient_h"] = self.dsb_several_phase_coefficient_h.value()
            settings["count_iterations"] = int(self.sb_several_phase_count_iterations.value())
        else:
            settings["model"] = "regular_polygon"
            settings["count_iterations"] = self.sb_single_phase_count_iterations.value()
            settings["count_angles"] = self.sb_regular_polygon_count_angle.value()
            settings["building_way"] = "inside" if self.rb_regular_polygon_build_inside.isChecked() else "outside"

        self.koch_curve = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(), self.dsb_angle.value(),
                                **settings)
        self.koch_curve.build()

    @is_calculations_absent
    def _visualize_fractal_growth(self):
        """
        Визуализировать вычисленную фрактальную структуру.
        :return:
        """

        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

        index = 0
        quit_mode = False
        while not quit_mode:
            self.draw(self.koch_curve.lines[index % len(self.koch_curve.lines)], self.rgb_lines, self.rgb_background,
                      self.sb_draw_latency.value())
            # # TODO: make save image
            if self.cb_screenshot.isChecked() and self.export_folder_path is not None:
                if index != 0 and index < len(self.koch_curve.lines):
                    self.save_image(self.export_folder_path, str(index) + '.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

            index += 1

    def _visualize_point_path_growth(self):
        """
        Визуализировать траекторию точек роста вычисленной фрактальной структуры.
        :return:
        """
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

        index = 0
        quit_mode = False
        while not quit_mode:
            a = []
            for i in range(index % len(self.koch_curve.lines)):
                a += self.koch_curve.lines[i]
            self.draw_points(a, self.rgb_lines, self.rgb_background, self.sb_draw_latency.value())

            # TODO: make save image
            if self.cb_screenshot.isChecked() and self.export_folder_path is not None:
                if index != 0 and index < len(self.koch_curve.lines):
                    self.save_image(self.export_folder_path, str(index) + '.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

            index += 1

    @is_calculations_absent
    def _visualize_thin_out_fractal_growth(self) -> None:
        """
        Прорядить фазы построения фрактальной структуры.
        :return:
        """
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

        index = 0
        quit_mode = False
        lines = []

        # TODO: move to separate module
        if self.sb_thinning_percentage.value() > 0:
            percent = self.sb_thinning_percentage.value() * 0.01
            kz = len(self.koch_curve.lines) * percent
            kio = int(len(self.koch_curve.lines) / kz)
            lyly = [i for i in range(0, len(self.koch_curve.lines), kio)]
            lines = [lines for index, lines in enumerate(self.koch_curve.lines) if index % 40 == 0]

        while not quit_mode:
            a = []
            for i in range(index % len(lines)):
                a += lines[i]
            self.draw(a, self.rgb_lines, self.rgb_background, self.sb_draw_latency.value())

            # TODO: make save image
            if self.cb_screenshot.isChecked() and self.export_folder_path is not None:
                if index != 0 and index < len(self.koch_curve.lines):
                    self.save_image(self.export_folder_path, str(index) + '.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

            index += 1

    def _pick_lines_color(self) -> None:
        """
        Выбор паитры для отрисовки отрезков.
        :return:
        """
        color = QtWidgets.QColorDialog.getColor()

        self.rgb_lines = (color.redF(), color.greenF(), color.blueF())
        self.pb_line_color.setStyleSheet(f'QWidget {{ background-color: {color.name()} }}')

    def _pick_background_color(self) -> None:
        """
        Выбор палитры для заливки фона.
        :return:
        """
        color = QtWidgets.QColorDialog.getColor()

        self.rgb_background = (color.redF(), color.greenF(), color.blueF())
        self.pb_background_color.setStyleSheet(f'QWidget {{ background-color: {color.name()} }}')

    def _enable_single_phase(self) -> None:
        """
        Выбор построения однофазной модели.
        :return:
        """
        self.l_image.setPixmap(QtGui.QPixmap("./static/single_phase_model.png"))
        self.l_single_phase_count_iterations.setHidden(False)
        self.sb_single_phase_count_iterations.setHidden(False)
        self.lb_regular_polygon_count_angle.setHidden(True)
        self.sb_regular_polygon_count_angle.setHidden(True)
        self.rb_regular_polygon_build_inside.setHidden(True)
        self.rb_regular_polygon_build_outside.setHidden(True)
        self.l_several_phase_coefficient_a.setHidden(True)
        self.dsb_several_phase_coefficient_a.setHidden(True)
        self.l_several_phase_coefficient_h.setHidden(True)
        self.dsb_several_phase_coefficient_h.setHidden(True)
        self.l_several_phase_count_iterations.setHidden(True)
        self.sb_several_phase_count_iterations.setHidden(True)

    def _several_phases(self) -> None:
        """
        Выбор построения многофазной модели.
        :return:
        """
        self.l_image.setPixmap(QtGui.QPixmap("./static/several_phases_model.png"))
        self.l_single_phase_count_iterations.setHidden(False)
        self.sb_single_phase_count_iterations.setHidden(False)
        self.lb_regular_polygon_count_angle.setHidden(True)
        self.sb_regular_polygon_count_angle.setHidden(True)
        self.rb_regular_polygon_build_inside.setHidden(True)
        self.rb_regular_polygon_build_outside.setHidden(True)
        self.l_several_phase_coefficient_a.setHidden(False)
        self.dsb_several_phase_coefficient_a.setHidden(False)
        self.l_several_phase_coefficient_h.setHidden(False)
        self.dsb_several_phase_coefficient_h.setHidden(False)
        self.l_several_phase_count_iterations.setHidden(True)
        self.sb_several_phase_count_iterations.setHidden(True)

    def _enable_regular_polygon(self) -> None:
        """
        Выбор построения правильной фигуры.
        :return:
        """
        self.l_image.setPixmap(QtGui.QPixmap("./static/single_phase_model.png"))
        self.l_single_phase_count_iterations.setHidden(False)
        self.sb_single_phase_count_iterations.setHidden(False)
        self.lb_regular_polygon_count_angle.setHidden(False)
        self.sb_regular_polygon_count_angle.setHidden(False)
        self.rb_regular_polygon_build_inside.setHidden(False)
        self.rb_regular_polygon_build_outside.setHidden(False)
        self.l_several_phase_coefficient_a.setHidden(True)
        self.dsb_several_phase_coefficient_a.setHidden(True)
        self.l_several_phase_coefficient_h.setHidden(True)
        self.dsb_several_phase_coefficient_h.setHidden(True)
        self.l_several_phase_count_iterations.setHidden(True)
        self.sb_several_phase_count_iterations.setHidden(True)

    def _make_screenshot(self) -> None:
        """
        Включит или отключить опцию экспорта скриншотов построения структур.
        :return:
        """
        if self.cb_screenshot.isChecked():
            self.pb_screenshot_path.setEnabled(True)
        else:
            self.pb_screenshot_path.setEnabled(False)

    def _choose_file_path(self) -> None:
        """
        Выбор директории экспорта изображений.
        :return:
        """

        self.export_folder_path = Path(QtWidgets.QFileDialog.getExistingDirectory(
            self, 'Select exporting folder...', '/home', QtWidgets.QFileDialog.ShowDirsOnly))

        preview = str(self.export_folder_path)
        if len(preview) > 20:
            preview = preview[:20] + "..."
        self.pb_screenshot_path.setText(preview)

    # TODO: approximation
    @is_calculations_absent
    def _plot_graph_line_len(self) -> None:
        """
        # TODO: docstring
        :return:
        """
        # TODO: to name this shirt
        x_train = [i for i in range(len(self.koch_curve.lines))]
        y_train = [sum(line.len() for line in lines) for i, lines in enumerate(self.koch_curve.lines)]
        y = [sum(line.len() for line in lines) for i, lines in enumerate(self.koch_curve.lines)
             if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]
        x = [i for i in range(len(self.koch_curve.lines)) if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]
        x = x[1:]
        y = y[1:]
        x = np.array(x)
        y = np.array(y)
        x_train = np.array(x_train)
        y_train = np.array(y_train)

        [a, b], res1 = curve_fit(lambda x1, a, b: a * np.exp(b * x1), x_train, y_train, p0=[0.01285, 0.0351])

        y1 = a * np.exp(b * x_train)
        fig, ax = plt.subplots()
        ax.plot(x, y, 'o', label='Original data', markersize=5)
        ax.plot(x_train, y1)
        ax.set(xlabel='Число циклов роста фрактала, ед.', ylabel='Длина фрактальной линии, ед.')
        ax.grid(True)
        plt.show()

    def _plot_graph_line_len_one_and_several_phases(self) -> None:
        """

        :return:
        """

        settings = dict()
        settings["model"] = "single"
        settings["count_iterations"] = self.sb_single_phase_count_iterations.value()
        one_phase_model = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(), self.dsb_angle.value(),
                                **settings)
        one_phase_model.build()

        settings["model"] = "irregular"
        settings["coefficient_a"] = self.dsb_several_phase_coefficient_a.value()
        settings["coefficient_h"] = self.dsb_several_phase_coefficient_h.value()
        settings["count_iterations"] = int(self.sb_several_phase_count_iterations.value())
        several_phase_model = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                    self.dsb_angle.value(), **settings)
        several_phase_model.build()

        settings["model"] = "irregular"
        settings["coefficient_a"] = self.dsb_several_phase_coefficient_a.value()
        settings["coefficient_h"] = self.dsb_several_phase_coefficient_h.value()
        settings["count_iterations"] = int(self.sb_several_phase_count_iterations.value() - 30)
        several_phase_model_2 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                      self.dsb_angle.value(), **settings)
        several_phase_model_2.build()

        # TODO: to name this shirt
        line_lens_train_single = [sum(line.len() for line in lines) for lines in one_phase_model.lines]
        # delete points of line growth
        line_lens_train_single = line_lens_train_single[self.sb_single_phase_count_iterations.value():]
        x_x_train = [i for i in range(len(line_lens_train_single))]
        y_y_train = line_lens_train_single[:]

        y3_y = np.array([self.dsb_max_line_legth.value() * 4 ** ((i + 1) / self.sb_several_phase_count_iterations.value())
                         for i in range(len(line_lens_train_single))])

        line_lens_train_single = [(i, value) for i, value in enumerate(line_lens_train_single)
                                 if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]
        x_train_single = [pair[0] for pair in line_lens_train_single]
        line_lens_train_single = [pair[1] for pair in line_lens_train_single]

        line_lens_train_several = [sum(line.len() for line in lines) for lines in several_phase_model.lines]
        # delete points of line growth
        line_lens_train_several = line_lens_train_several[self.sb_several_phase_count_iterations.value():]
        x_train_several = [i for i in range(len(line_lens_train_several))]

        line_lens_train_several_2 = [sum(line.len() for line in lines) for lines in several_phase_model_2.lines]
        # delete points of line growth
        line_lens_train_several_2 = line_lens_train_several_2[self.sb_several_phase_count_iterations.value() - 30:]
        x_train_several_2 = [i for i in range(len(line_lens_train_several_2))]

        fig, ax = plt.subplots()
        ax.plot(x_x_train, y_y_train, label=r'$a$', c='black', linewidth=5)
        ax.plot(x_train_several, line_lens_train_several, linestyle=":", label=r'$b$', c='black', linewidth=5)
        ax.plot(x_train_several_2, line_lens_train_several_2, linestyle="--", label=r'$c$', c='black', linewidth=5)
        ax.plot(x_train_single, line_lens_train_single, 's', markersize=10, markeredgewidth=3, label=r'$f_1$', c='black')
        # ax.plot([i for i in range(len(y3_y))], y3_y, linestyle="-", label=r'$f_1$', c='black', linewidth=2)
        ax.set_xlim(xmin=100)
        ax.set_ylim(ymin=-50)
        ax.grid(True)
        ax.legend(loc='upper left', fancybox=True, framealpha=1, shadow=True, borderpad=1)
        ax.set(xlabel='Число циклов роста, ед.', ylabel='Длина фрактальной линии, ед.')

        # setting label sizes after creation
        ax.xaxis.label.set_size(30)
        ax.yaxis.label.set_size(30)

        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.legend(fontsize=30)
        plt.show()

    # TODO: approximation
    @is_calculations_absent
    def _plot_graph_scale(self):
        """
        # TODO: docstring
        :return:
        """
        # TODO: to name this shirt
        y_x_train = [abs(max(max(line.start.x, line.finish.x) for line in lines) - min(min(line.start.x, line.finish.x) for line in lines)) for lines in self.koch_curve.lines]
        y_x = [value for i, value in enumerate(y_x_train)
               if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]
        y_y_train = [abs(max(max(line.start.y, line.finish.y) for line in lines) -
                 min(min(line.start.y, line.finish.y) for line in lines)) for lines in self.koch_curve.lines]
        y_y = [value for i, value in enumerate(y_y_train)
               if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]
        x_train = [i for i in range(len(self.koch_curve.lines))]
        x = [i for i in range(len(self.koch_curve.lines)) if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]

        y_x_train = np.array(y_x_train)
        y_x = np.array(y_x)
        y_y_train = np.array(y_y_train)
        y_y = np.array(y_y)
        x_train = np.array(x_train)
        x = np.array(x)

        [a_y_x, b_y_x], _ = curve_fit(lambda x1, a, b: a * np.exp(b * x1), x_train, y_x_train, p0=[0.01285, 0.0351])
        [a_y_y, b_y_y], _ = curve_fit(lambda x1, a, b: a * np.exp(b * x1), x_train, y_y_train, p0=[0.01285, 0.0351])

        y1_x = a_y_x * np.exp(b_y_x * x_train)
        y2_y = a_y_y * np.exp(b_y_y * x_train)

        fig, ax = plt.subplots()
        ax.plot(x, y_x, 'x', markersize=8, markeredgewidth=3, label='Значение размаха фрактала по oX от его глубины', c='black')
        ax.plot(x_train, y1_x, linestyle="--", label='Размах фрактала по oX', c='black')
        ax.plot(x, y_y, 'x', markersize=8, markeredgewidth=3, label='Значение размаха фрактала по oY от его глубины', c='black')
        ax.plot(x_train, y2_y, linestyle=":", label='Размах фрактала по oY', c='black')
        ax.grid(True)
        ax.legend(loc='upper left', fancybox=True, framealpha=1, shadow=True, borderpad=1)
        ax.set(xlabel='Число циклов роста фрактала, ед.', ylabel='Размах фрактала, ед.')
        plt.show()

    def _plot_graph_scale_one_and_several_phases(self):
        """

        :return:
        """
        settings = dict()
        settings["model"] = "single"
        settings["count_iterations"] = self.sb_single_phase_count_iterations.value()
        one_phase_model = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(), self.dsb_angle.value(),
                                **settings)
        one_phase_model.build()

        wingspan_train_single_2 = [abs(max(max(line.start.x, line.finish.x) for line in lines) - min(
            min(line.start.x, line.finish.x) for line in lines)) for lines in one_phase_model.lines]
        # delete points of line growth
        wingspan_train_single_2 = wingspan_train_single_2[self.sb_single_phase_count_iterations.value():]
        x_train_single_2 = [i for i in range(len(wingspan_train_single_2))]

        settings["model"] = "irregular"
        settings["coefficient_a"] = self.dsb_several_phase_coefficient_a.value()
        settings["coefficient_h"] = self.dsb_several_phase_coefficient_h.value()
        settings["count_iterations"] = self.sb_several_phase_count_iterations.value()
        several_phase_model_1 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                    self.dsb_angle.value(), **settings)
        several_phase_model_1.build()

        wingspan_train_several_1 = [abs(max(max(line.start.x, line.finish.x) for line in lines) - min(
            min(line.start.x, line.finish.x) for line in lines)) for lines in several_phase_model_1.lines]
        # delete points of line growth
        wingspan_train_several_1 = wingspan_train_several_1[self.sb_several_phase_count_iterations.value():]
        x_train_several_1 = [i for i in range(len(wingspan_train_several_1))]
        print("First calculation is over")

        settings["model"] = "irregular"
        settings["coefficient_a"] = self.dsb_several_phase_coefficient_a.value()
        settings["coefficient_h"] = self.dsb_several_phase_coefficient_h.value()
        settings["count_iterations"] = int(self.sb_several_phase_count_iterations.value() - 30)
        several_phase_model_2 = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(),
                                      self.dsb_angle.value(), **settings)
        several_phase_model_2.build()

        wingspan_train_several_2 = [abs(max(max(line.start.x, line.finish.x) for line in lines) - min(
            min(line.start.x, line.finish.x) for line in lines)) for lines in several_phase_model_2.lines]
        # delete points of line growth
        wingspan_train_several_2 = wingspan_train_several_2[self.sb_several_phase_count_iterations.value() - 30:]
        x_train_several_2 = [i for i in range(len(wingspan_train_several_2))]
        print("Second calculation is over")

        # TODO: to name this shirt
        wingspan_train_single = [abs(max(max(line.start.x, line.finish.x) for line in lines) - min(
            min(line.start.x, line.finish.x) for line in lines)) for lines in one_phase_model.lines]
        # delete points of line growth
        wingspan_train_single = wingspan_train_single[self.sb_single_phase_count_iterations.value():]

        import math
        y3_y = np.array([self.dsb_max_line_legth.value() * ((2 + 2 * math.cos(np.deg2rad(self.dsb_angle.value()))) ** (
                (i + 1) / self.sb_several_phase_count_iterations.value())) for i in range(len(wingspan_train_single))])

        wingspan_train_single = [(i, value) for i, value in enumerate(wingspan_train_single)
                                 if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]
        x_train_single = [pair[0] for pair in wingspan_train_single]
        wingspan_train_single = [pair[1] for pair in wingspan_train_single]

        fig, ax = plt.subplots()
        fig.set_size_inches(18.5, 10.5)
        ax.plot(x_train_single_2, wingspan_train_single_2, label=r'$a$', c='black', linewidth=5)
        ax.plot(x_train_several_1, wingspan_train_several_1, linestyle=":", label=r'$b$', c='black', linewidth=5)
        ax.plot(x_train_several_2, wingspan_train_several_2, linestyle="--", label=r'$c$', c='black', linewidth=5)
        ax.plot(x_train_single, wingspan_train_single, 's', markersize=10, markeredgewidth=3, label=r'$f_2$', c='black')
        ax.set_xlim(xmin=5)
        ax.set_ylim(ymin=-25)
        ax.grid(True)
        ax.legend(loc='lower right', fancybox=True, framealpha=1, shadow=True, borderpad=1)
        ax.set(xlabel='Число циклов роста, ед.', ylabel='Размах фрактала, ед.')

        # setting label sizes after creation
        ax.xaxis.label.set_size(30)
        ax.yaxis.label.set_size(30)

        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        plt.legend(fontsize=30)
        plt.show()

    @is_calculations_absent
    def _plot_graph_angle(self):
        """
        # TODO: docstring
        :return:
        """
        eps = 0.2
        theta = [[np.deg2rad(line.get_triangle_angle()) for line in lines] for i, lines in enumerate(self.koch_curve.lines) if i % (self.sb_single_phase_count_iterations.value() - 1) == 0]
        theta = theta[1:]
        r = [1 + n * eps for n in range(len(theta))]
        ax = plt.subplot(111, polar=True)
        for i in range(len(r)):
            ax.scatter(theta[i], [r[i] for _ in range(len(theta[i]))], alpha=1, linewidths=2.5, c='black')
        ax.set_rmax(2.5)
        rings = [i * 0.25 for i in range(11)]
        rings_labels = ["1" if value == 1.0 else "" for value in rings]
        plt.rgrids(rings, rings_labels)
        ax.grid(True)

        plt.xticks(fontsize=30)
        plt.yticks(fontsize=30)
        ax.set_title(r'$\beta=' + str(int(self.dsb_angle.value())) + r'°$', va='bottom', fontsize=30)

        plt.show()

    @staticmethod
    # TODO: make common method with draw points
    # TODO: move to another package
    def draw(lines: List[Segment], rgb_lines: Tuple[float, float, float], rgb_background: Tuple[float, float, float],
             draw_latency: int) -> None:
        """
        Прорисовка на канвасе OpenGL.
        :param lines: Список отрезков, которые необходимо отобразить.
        :param rgb_lines: RGB пера, которым будут отрисованы отрезки.
        :param rgb_background: RGB фона.
        :param draw_latency: задержка при отрисовке.
        :return:
        """
        glColor3f(*rgb_lines)
        glLineWidth(2)
        glClearColor(*rgb_background, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glBegin(GL_LINES)
        for line in lines:
            glVertex2f(line.start.x, line.start.y)
            glVertex2f(line.finish.x, line.finish.y)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(draw_latency)

    @staticmethod
    # TODO: make common method with draw lines
    # TODO: move to another package
    def draw_points(lines: List[Segment], rgb_lines: Tuple[float, float, float],
                    rgb_background: Tuple[float, float, float], draw_latency: int) -> None:
        """
        Прорисовка на канвасе OpenGL.
        :param lines: Список отрезков, которые необходимо отобразить.
        :param rgb_lines: RGB пера, которым будут отрисованы отрезки.
        :param rgb_background: RGB фона.
        :param draw_latency: задержка при отрисовке.
        :return:
        """
        glColor3f(*rgb_lines)
        glPointSize(2)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(*rgb_background, 1)

        glBegin(GL_POINTS)
        for line in lines:
            glVertex2f(line.start.x, line.start.y)
            glVertex2f(line.finish.x, line.finish.y)
        glEnd()

        pygame.display.flip()
        pygame.time.wait(draw_latency)

    @staticmethod
    # TODO: make full file path
    # TODO: choose color to transparency
    # TODO: move to another package
    def save_image(directory: Path, file_name: str) -> None:
        """
        Сохранение текущего состояния канваса OpenGL в виде PNG файла на диск с прозрачным фоном, заменив при этом все
        белые пиксели.
        :param directory: Полный или относительный путь дирректории, куда будет производиться сохранение.
        :param file_name: Наименование файла.
        :return:
        """
        glPixelStorei(GL_PACK_ALIGNMENT, 1)

        rough_data = glReadPixels(0, 0, WIDTH, HEIGHT, GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (WIDTH, HEIGHT), rough_data)
        image = ImageOps.flip(image)  # in my case image is flipped top-bottom for some reason
        data = image.getdata()
        new_data = []
        for item in data:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        image.putdata(new_data)

        image.save(directory / file_name, 'PNG')


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = Application()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
