from typing import List
import pygame
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
from OpenGL.GL import *
# from OpenGL.GLU import *
import math
from geometry.entity_2d import Point, Line
# import random
# import time

SCROLL_UP = 4
SCROLL_DOWN = 5
HEIGHT = 800
WIDTH = 800


class Application(QtWidgets.QMainWindow, design.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        # Далее подключаем наши callback-и по нажатию того или иного
        self.pushButton.clicked.connect(self._enable_stochastic_fractal_mode)

    def _enable_stochastic_fractal_mode(self):
        pygame.init()
        display = (WIDTH, HEIGHT)
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)

        # self.draw(lines)
        quit_mode = False
        while not quit_mode:
            p1 = Point(0, 0)
            p2 = create_point(p1, 0.1, 45)
            p3 = create_point(p2, 0.1, 90)
            p4 = create_point(p3, 0.1, 135)
            p5 = create_point(p4, 0.1, 180)
            p6 = create_point(p5, 0.1, 225)
            p7 = create_point(p6, 0.1, 270)
            p8 = create_point(p7, 0.1, 315)
            p9 = create_point(p8, 0.1, 360)
            p10 = create_point(p9, 0.1, 45)

            z = [Line(p1, p2), Line(p2, p3), Line(p3, p4), Line(p4, p5), Line(p5, p6), Line(p6, p7), Line(p7, p8), Line(p8, p9), Line(p9, p10)]
            # Белый цвет фона
            glClearColor(1, 1, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            self.draw(z)
            pygame.display.flip()
            pygame.time.wait(500)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit_mode = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == SCROLL_UP:
                        pass
                    elif event.button == SCROLL_DOWN:
                        pass
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        for angle in range(0, 180, 5):
                            pass
                            # glRotate(10, 0, 1, 0)
                            # time.sleep(0.05)
                            # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                            # self.draw(lines)
                            # pygame.display.flip()
                    elif event.key == pygame.K_LEFT:
                        for angle in range(0, 180, 5):
                            pass
                            # glRotate(10, 0, -1, 0)
                            # time.sleep(0.05)
                            # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                            # self.draw(lines)
                            # pygame.display.flip()
                    elif event.key == pygame.K_UP:
                        for angle in range(0, 180, 5):
                            pass
                            # glRotate(10, -1, 0, 0)
                            # time.sleep(0.05)
                            # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                            # self.draw(lines)
                            # pygame.display.flip()
                    elif event.key == pygame.K_DOWN:
                        for angle in range(0, 180, 5):
                            pass
                            # glRotate(10, 1, 0, 0)
                            # time.sleep(0.05)
                            # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                            # self.draw(lines)
                            pygame.display.flip()
                    if event.key == pygame.K_SPACE:
                        pass
                    if event.key == pygame.K_d:
                        pass
                    elif event.key == pygame.K_a:
                        pass
                    elif event.key == pygame.K_w:
                        pass
                    elif event.key == pygame.K_s:
                        pass
                    elif event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit_mode = True

    @staticmethod
    def draw(lines: List[Line]):
        # Черный цвет пера для отображения прямых
        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(2)
        glBegin(GL_LINES)
        for line in lines:
            glVertex2f(line.point_1.x, line.point_1.y)
            glVertex2f(line.point_2.x, line.point_2.y)
        glEnd()


def create_point(point: Point, distance: float, angle: float) -> Point:
    """

    :param point: Начальная точка с координатами x и y
    :param distance: Расстояние, на котором будет находиться новая точка
    :param angle: Угол поворота
    :return: Новая точка с координатами x и y
    """

    x = point.x + (distance * math.cos(angle * math.pi / 180.0))
    y = point.y + (distance * math.sin(angle * math.pi / 180.0))

    return Point(x, y)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Application()                  # Создаём объект класса Application
    window.show()                           # Показываем окно
    app.exec_()                             # и запускаем приложение


if __name__ == '__main__':
    main()
