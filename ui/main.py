from functools import wraps
from typing import List, Tuple
import pygame
from PyQt5 import QtWidgets, QtGui
from OpenGL.GL import *
from geometry.entity_2d import Segment
from fractals.koch.curve import Curve
from PIL import Image, ImageOps
from pathlib import Path

from settings import STATIC_PATH

from ui.generated.main import Ui_MainWindow
from ui.implementation.single_phase import SinglePhaseUI
from ui.implementation.several_phases import SeveralPhasesUI
from ui.implementation.regular_polygon import RegularPolygonUI
from ui.implementation.single_several_phases import SingleSeveralPhasesUI

HEIGHT = 1000
WIDTH = 1000

display = (WIDTH, HEIGHT)

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


class MainUI(QtWidgets.QMainWindow, Ui_MainWindow):
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
        self.lb_image.setPixmap(QtGui.QPixmap(str(STATIC_PATH / 'single_phase_model.png')))
        self.lb_regular_polygon_count_angle.setHidden(True)
        self.sb_regular_polygon_count_angle.setHidden(True)
        self.rb_regular_polygon_build_inside.setHidden(True)
        self.rb_regular_polygon_build_outside.setHidden(True)
        self.l_several_phase_coefficient_a.setHidden(True)
        self.dsb_several_phase_coefficient_a.setHidden(True)
        self.l_several_phase_coefficient_h.setHidden(True)
        self.dsb_several_phase_coefficient_h.setHidden(True)

        self.single_phase_window = SinglePhaseUI()
        self.several_phases_window = SeveralPhasesUI()
        self.regular_polygon_window = RegularPolygonUI()
        self.single_and_several_phases_window = SingleSeveralPhasesUI()

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

        # graphs
        # fractal len
        self.pb_graph_line_len_single_phase.clicked.connect(self._plot_line_len_single_phase)
        self.pb_graph_line_len_several_phases.clicked.connect(self._plot_line_len_several_phases)
        self.pb_graph_line_len_regular_polygon.clicked.connect(self._plot_line_len_polygon)
        # fractal span
        self.pb_graph_fractal_span_single_phase.clicked.connect(self._plot_fractal_span_single_phase)
        self.pb_graph_fractal_span_several_phases.clicked.connect(self._plot_fractal_span_several_phases)
        self.pb_graph_fractal_span_regular_polygon.clicked.connect(self._plot_fractal_span_polygon)
        # angles in polar system
        self.pb_graph_angle_single_phase.clicked.connect(self._plot_angle_single_phase)
        self.pb_graph_angle_several_phases.clicked.connect(self._plot_angle_several_phases)
        self.pb_graph_angle_regular_polygon.clicked.connect(self._plot_angle_polygon)
        # mix
        self.pb_graph_line_len_single_and_several_phases.clicked.connect(self._plot_line_len_single_and_several_phases)
        self.pb_graph_fractal_span_one_and_several_phases.clicked.connect(
            self._plot_fractal_span_one_and_several_phases)

    def _calculation_fractal(self):
        """
        Вычислить фрактальную структуру.
        :return:
        """
        settings = dict()
        if self.rb_single_phase.isChecked():
            settings["model"] = "single"
            settings["count_iterations"] = self.sb_count_iterations.value()
        elif self.rb_several_phases.isChecked():
            settings["model"] = "several"
            settings["coefficient_a"] = self.dsb_several_phase_coefficient_a.value()
            settings["coefficient_h"] = self.dsb_several_phase_coefficient_h.value()
            settings["count_iterations"] = int(self.sb_count_iterations.value())
        else:
            settings["model"] = "regular_polygon"
            settings["count_iterations"] = self.sb_count_iterations.value()
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
        self.lb_image.setPixmap(QtGui.QPixmap(str(STATIC_PATH / 'single_phase_model.png')))
        self.lb_regular_polygon_count_angle.hide()
        self.sb_regular_polygon_count_angle.hide()
        self.rb_regular_polygon_build_inside.hide()
        self.rb_regular_polygon_build_outside.hide()
        self.l_several_phase_coefficient_a.hide()
        self.dsb_several_phase_coefficient_a.hide()
        self.l_several_phase_coefficient_h.hide()
        self.dsb_several_phase_coefficient_h.hide()

    def _several_phases(self) -> None:
        """
        Выбор построения многофазной модели.
        :return:
        """
        self.lb_image.setPixmap(QtGui.QPixmap(str(STATIC_PATH / 'several_phases_model.png')))
        self.lb_regular_polygon_count_angle.setHidden(True)
        self.sb_regular_polygon_count_angle.setHidden(True)
        self.rb_regular_polygon_build_inside.setHidden(True)
        self.rb_regular_polygon_build_outside.setHidden(True)
        self.l_several_phase_coefficient_a.setHidden(False)
        self.dsb_several_phase_coefficient_a.setHidden(False)
        self.l_several_phase_coefficient_h.setHidden(False)
        self.dsb_several_phase_coefficient_h.setHidden(False)

    def _enable_regular_polygon(self) -> None:
        """
        Выбор построения правильной фигуры.
        :return:
        """
        self.lb_image.setPixmap(QtGui.QPixmap(str(STATIC_PATH / 'single_phase_model.png')))
        self.lb_regular_polygon_count_angle.setHidden(False)
        self.sb_regular_polygon_count_angle.setHidden(False)
        self.rb_regular_polygon_build_inside.setHidden(False)
        self.rb_regular_polygon_build_outside.setHidden(False)
        self.l_several_phase_coefficient_a.setHidden(True)
        self.dsb_several_phase_coefficient_a.setHidden(True)
        self.l_several_phase_coefficient_h.setHidden(True)
        self.dsb_several_phase_coefficient_h.setHidden(True)

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
            self, 'Select exporting folder...', '/', QtWidgets.QFileDialog.ShowDirsOnly))

        preview = str(self.export_folder_path)
        if len(preview) > 20:
            preview = preview[:20] + "..."
        self.pb_screenshot_path.setText(preview)

    def _plot_line_len_single_phase(self) -> None:
        """

        :return:
        """
        self.single_phase_window.graph_type = 'len'
        self.single_phase_window.show()

    def _plot_line_len_several_phases(self) -> None:
        """

        :return:
        """
        self.several_phases_window.graph_type = 'len'
        self.several_phases_window.show()

    def _plot_line_len_polygon(self) -> None:
        """

        :return:
        """
        self.regular_polygon_window.graph_type = 'len'
        self.regular_polygon_window.show()

    def _plot_fractal_span_single_phase(self) -> None:
        """

        :return:
        """
        self.single_phase_window.graph_type = 'span'
        self.single_phase_window.show()

    def _plot_fractal_span_several_phases(self) -> None:
        """

        :return:
        """
        self.several_phases_window.graph_type = 'span'
        self.several_phases_window.show()

    def _plot_fractal_span_polygon(self) -> None:
        """

        :return:
        """
        self.regular_polygon_window.graph_type = 'span'
        self.regular_polygon_window.show()

    def _plot_angle_single_phase(self) -> None:
        """

        :return:
        """
        self.single_phase_window.graph_type = 'angle'
        self.single_phase_window.show()

    def _plot_angle_several_phases(self) -> None:
        """

        :return:
        """
        self.several_phases_window.graph_type = 'angle'
        self.several_phases_window.show()

    def _plot_angle_polygon(self) -> None:
        """

        :return:
        """
        self.regular_polygon_window.graph_type = 'angle'
        self.regular_polygon_window.show()

    def _plot_line_len_single_and_several_phases(self) -> None:
        """

        :return:
        """
        self.single_and_several_phases_window.graph_type = 'line'
        self.single_and_several_phases_window.show()

    def _plot_fractal_span_one_and_several_phases(self) -> None:
        """

        :return:
        """
        self.single_and_several_phases_window.graph_type = 'span'
        self.single_and_several_phases_window.show()

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
