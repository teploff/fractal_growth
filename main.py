from typing import List
import pygame
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
from OpenGL.GL import *
# from OpenGL.GLU import *
from geometry.entity_2d import Segment, Point
from ontogeny.entity_2d import Branch
from ontogeny.utils import engender_segment, calculate_equidistant_point
from ontogeny.examles import get_two_level_tree, get_three_level_tree
import random
import math


MIN_ANGLE = -1
MAX_ANGLE = 1
LENGTH_K = 1.05

SCROLL_UP = 4
SCROLL_DOWN = 5
HEIGHT = 900
WIDTH = 1650

display = (WIDTH, HEIGHT)


class Application(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        pygame.init()
        # Далее подключаем наши callback-и по нажатию того или иного
        self.pushButton.clicked.connect(self._engender_fractal)

    def _engender_fractal(self):
        # Инициализация белого окна
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        quit_mode = False
        delta_1 = 0.01
        delta_2 = math.sqrt(3) * delta_1
        segment = Segment(Point(-delta_1 / 10.0, -0.75), Point(delta_1 / 10.0, -0.75))
        segments = [segment]
        active_segments = [segment]
        n = 0
        while not quit_mode:
            for segment in active_segments:
                if segment.len() < 0.1:
                    engender_segment(segment, delta_1)
                else:
                    active_segments.remove(segment)

                    calculate_equidistant_point(segment.start, segment.finish, delta_2 * n)
                # else:
                #     n += 1
                #     calculate_equidistant_point(segment.start, segment.finish, delta_2*n)

            # selected_height_tree = random.randint(0, tree.root.height)
            # selected_branches = tree.get_branches_by_height(selected_height_tree)
            # selected_indexes = tree.get_indexes_by_branches(selected_branches)
            # selected_segments = tree.represent_branches_as_segments(selected_branches)
            self.draw(segments)

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
        pygame.display.flip()
        pygame.time.wait(100)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Application()                  # Создаём объект класса Application
    window.show()                           # Показываем окно
    app.exec_()                             # и запускаем приложение


if __name__ == '__main__':
    main()
