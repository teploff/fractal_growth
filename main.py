from typing import List, Tuple
import pygame
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets, QtGui
import design  # Это наш конвертированный файл дизайна
from OpenGL.GL import *
# from OpenGL.GLU import *
from geometry.entity_2d import Segment, Point
from fractals.koch_curve import Curve
from PIL import Image, ImageOps


SCROLL_UP = 4
SCROLL_DOWN = 5
HEIGHT = 1000
WIDTH = 1000

display = (WIDTH, HEIGHT)

MAX_LINE_LENGTH = 0.05
N_ITER = 20
BLACK = (0.0, 0.0, 0.0)
WHITE = (1.0, 1.0, 1.0)

DIRECTORY = './pictures/'


class Application(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # initialize components from generated design.py
        super().__init__()
        self.setupUi(self)

        # make default settings
        self.rgb_lines = BLACK
        self.rgb_background = WHITE
        self.l_image.setPixmap(QtGui.QPixmap("./static/single_phase_model.png"))
        self.l_several_phase_count_iter_a.setHidden(True)
        self.dsb_several_phase_count_iter_a.setHidden(True)
        self.l_several_phase_count_iter_b.setHidden(True)
        self.dsb_several_phase_count_iter_b.setHidden(True)
        self.l_several_phase_k_growth.setHidden(True)
        self.dsb_several_phase_k_growth.setHidden(True)

        pygame.init()

        # callbacks
        self.pb_engender_fractal.clicked.connect(self._engender_fractal)
        self.pb_build_point_path.clicked.connect(self._point_growth_path)
        self.pb_line_color.clicked.connect(self._pick_lines_color)
        self.pb_background_color.clicked.connect(self._pick_background_color)
        self.rb_single_phase.clicked.connect(self._enable_single_phase)
        self.rb_several_phase.clicked.connect(self._enable_several_phases)

    def _engender_fractal(self):
        """
        Наростить фрактал.
        :return:
        """
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

        settings = dict()
        if self.rb_single_phase.isChecked():
            settings["model"] = "single"
            settings["count_iter"] = self.sb_single_phase_count_iter_a.value()
        else:
            settings["model"] = "several"
            settings["count_iter_a"] = self.dsb_several_phase_count_iter_a.value()
            settings["count_iter_b"] = self.dsb_several_phase_count_iter_b.value()
            settings["k_growth"] = int(self.dsb_several_phase_k_growth.value())

        koch_curve = Curve(self.sb_fractal_depth.value(), self.dsb_max_line_legth.value(), self.dsb_angle.value(),
                           **settings)
        koch_curve.build()

        index = 0
        quit_mode = False
        while not quit_mode:
            self.draw(koch_curve.lines[index % len(koch_curve.lines)], self.rgb_lines, self.rgb_background,
                      self.sb_draw_latency.value())
            # TODO: make save image
            # self.save_image(DIRECTORY, str(index) + '.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

            index += 1

    def _point_growth_path(self):
        """
        Построить траекторию роста точек фрактала
        :return:
        """
        # Инициализация белого окна
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        quit_mode = False
        koch_curve = Curve(self.dsb_max_line_legth.value(), N_ITER)
        koch_curve.build(self.sb_fractal_depth.value())

        while not quit_mode:
            new_lines = []
            i = 0
            while i < len(koch_curve.lines) - 2:
                lll = []
                for j in range(i + 1):
                    lll.append(Segment(koch_curve.lines[j][0].start, koch_curve.lines[j + 1][0].start))
                    lll.append(Segment(koch_curve.lines[j][len(koch_curve.lines[j]) - 1].finish,
                                       koch_curve.lines[j + 1][len(koch_curve.lines[j + 1]) - 1].finish))
                new_lines.append(lll)
                i += 1

            for i, lines in enumerate(new_lines):
                self.draw(lines, BLACK, WHITE)
                self.save_image(DIRECTORY, str(i) + '.png')

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

    def _pick_lines_color(self) -> None:
        """
        Выбор паитры для отрисовки отрезков.
        :return:
        """
        color = QtWidgets.QColorDialog.getColor()

        self.rgb_lines = (color.redF(), color.greenF(), color.blueF())
        self.pb_line_color.setStyleSheet(f"QWidget {{ background-color: {color.name()} }}")

    def _pick_background_color(self) -> None:
        """
        Выбор палитры для заливки фона.
        :return:
        """
        color = QtWidgets.QColorDialog.getColor()

        self.rgb_background = (color.redF(), color.greenF(), color.blueF())
        self.pb_background_color.setStyleSheet(f"QWidget {{ background-color: {color.name()} }}")

    def _enable_single_phase(self) -> None:
        """
        Выбор построения однофазной модели.
        :return:
        """
        self.l_image.setPixmap(QtGui.QPixmap("./static/single_phase_model.png"))
        self.l_single_phase_count_iter_a.setHidden(False)
        self.sb_single_phase_count_iter_a.setHidden(False)
        self.l_several_phase_count_iter_a.setHidden(True)
        self.dsb_several_phase_count_iter_a.setHidden(True)
        self.l_several_phase_count_iter_b.setHidden(True)
        self.dsb_several_phase_count_iter_b.setHidden(True)
        self.l_several_phase_k_growth.setHidden(True)
        self.dsb_several_phase_k_growth.setHidden(True)

    def _enable_several_phases(self) -> None:
        """
        Выбор построения многофазной модели.
        :return:
        """
        self.l_image.setPixmap(QtGui.QPixmap("./static/several_phases_model.png"))
        self.l_single_phase_count_iter_a.setHidden(True)
        self.sb_single_phase_count_iter_a.setHidden(True)
        self.l_several_phase_count_iter_a.setHidden(False)
        self.dsb_several_phase_count_iter_a.setHidden(False)
        self.l_several_phase_count_iter_b.setHidden(False)
        self.dsb_several_phase_count_iter_b.setHidden(False)
        self.l_several_phase_k_growth.setHidden(False)
        self.dsb_several_phase_k_growth.setHidden(False)

    @staticmethod
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
    def save_image(directory: str, file_name: str) -> None:
        """
        Сохранение текущего состояния канваса OpenGL в виде PNG файла на диск.
        :param directory: Полный или относительный путь дирректории, куда будет производиться сохранение.
        :param file_name: Наименование файла.
        :return:
        """
        glPixelStorei(GL_PACK_ALIGNMENT, 1)

        data = glReadPixels(0, 0, WIDTH, HEIGHT, GL_RGBA, GL_UNSIGNED_BYTE)
        image = Image.frombytes("RGBA", (WIDTH, HEIGHT), data)
        image = ImageOps.flip(image)  # in my case image is flipped top-bottom for some reason
        image.save(directory + file_name, 'PNG')


def main():
    app = QtWidgets.QApplication(sys.argv)

    window = Application()
    window.show()

    app.exec_()


if __name__ == '__main__':
    main()
