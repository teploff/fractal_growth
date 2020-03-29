from typing import List
import pygame
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
from OpenGL.GL import *
# from OpenGL.GLU import *
from geometry.entity_2d import Point, Segment
from ontogeny.utils import increase_segment
from ontogeny.examles import get_two_level_tree, get_three_level_tree
import random


MIN_ANGLE = -10
MAX_ANGLE = 5
LENGTH_K = 1.1

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

        quit_mode = False
        tree = get_three_level_tree()
        segments = tree.get_branches_as_segments(tree.root)
        while not quit_mode:
            selected_index_branch = random.randint(0, len(tree) - 1)
            self.draw(segments, selected_index_branch)
            delta_angle = random.randint(MIN_ANGLE, MAX_ANGLE)
            new_branch = increase_segment(segments[selected_index_branch], delta_angle, LENGTH_K)
            selected_branch = tree.get_branch_by_index(selected_index_branch)
            children = selected_branch.children
            for child in children:
                s = increase_segment(Segment(selected_branch.segment.start, child.segment.start), delta_angle, LENGTH_K)
                delta_x = s.finish.x - child.segment.start.x
                delta_y = s.finish.y - child.segment.start.y
                child.segment.start = s.finish
                child.segment.finish.x += delta_x
                child.segment.finish.y += delta_y
            tree.update_branch(segments[selected_index_branch], new_branch)
            segments = tree.get_branches_as_segments(tree.root)
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
    def draw(lines: List[Segment], index=None):
        # Черный цвет пера для отображения прямых
        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(2)
        if index is not None:
            for iter1 in range(6):
                # Белый цвет фона
                glClearColor(1, 1, 1, 1)
                glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
                glBegin(GL_LINES)
                for line in lines:
                    glVertex2f(line.start.x, line.start.y)
                    glVertex2f(line.finish.x, line.finish.y)
                glEnd()
                if iter1 % 2 != 0:
                    glBegin(GL_LINES)
                    glColor3f(1.0, 0.0, 0.0)
                    glVertex2f(lines[index].start.x, lines[index].start.y)
                    glVertex2f(lines[index].finish.x, lines[index].finish.y)
                    glEnd()
                    glColor3f(0.0, 0.0, 0.0)
                pygame.display.flip()
                pygame.time.wait(300)
        else:
            # Белый цвет фона
            glClearColor(1, 1, 1, 1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glBegin(GL_LINES)
            for line in lines:
                glVertex2f(line.start.x, line.start.y)
                glVertex2f(line.finish.x, line.finish.y)
            glEnd()
            pygame.display.flip()
            pygame.time.wait(300)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Application()                  # Создаём объект класса Application
    window.show()                           # Показываем окно
    app.exec_()                             # и запускаем приложение


if __name__ == '__main__':
    main()
