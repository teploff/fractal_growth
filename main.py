from typing import List
import pygame
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
from OpenGL.GL import *
# from OpenGL.GLU import *
from geometry.entity_2d import Segment, Point
from fractals.koch_curve import Curve


MIN_ANGLE = -1
MAX_ANGLE = 1
LENGTH_K = 1.05

SCROLL_UP = 4
SCROLL_DOWN = 5
HEIGHT = 900
WIDTH = 1650

display = (WIDTH, HEIGHT)

MAX_LINE_LENGTH = 0.05
N_ITER = 20


class Application(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        pygame.init()
        # Далее подключаем наши callback-и по нажатию того или иного
        self.pushButton.clicked.connect(self._engender_fractal)
        self.pushButton_2.clicked.connect(self._point_growth_path)

    def _engender_fractal(self):
        # Инициализация белого окна
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        quit_mode = False
        koch_curve = Curve(float(self.lineEdit.text()), N_ITER)
        koch_curve.build(self.spinBox.value())

        while not quit_mode:
            for i, lines in enumerate(koch_curve.lines):
                self.draw(lines)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

    def _point_growth_path(self):
        """

        :return:
        """

        # Инициализация белого окна
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        quit_mode = False
        koch_curve = Curve(float(self.lineEdit.text()), N_ITER)
        koch_curve.build(self.spinBox.value())

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
                self.draw(lines)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

    @staticmethod
    def draw(lines: List[Segment], selected_lines=None):
        # Черный цвет пера для отображения прямых
        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(2)
        # Белый цвет фона
        glClearColor(1, 1, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_LINES)
        for line in lines:
            glVertex2f(line.start.x, line.start.y)
            glVertex2f(line.finish.x, line.finish.y)
        glEnd()
        pygame.image.save(pygame.display.get_surface(), "circle.png")
        pygame.display.flip()
        pygame.time.wait(100)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Application()                  # Создаём объект класса Application
    window.show()                           # Показываем окно
    app.exec_()                             # и запускаем приложение


if __name__ == '__main__':
    main()
