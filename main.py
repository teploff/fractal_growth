from typing import List
import pygame
import sys  # sys нужен для передачи argv в QApplication
from PyQt5 import QtWidgets
import design  # Это наш конвертированный файл дизайна
from OpenGL.GL import *
# from OpenGL.GLU import *
from geometry.entity_2d import Segment
from ontogeny.entity_2d import Branch
from ontogeny.utils import increase_segment
from ontogeny.examles import get_two_level_tree, get_three_level_tree
import random


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
        self.pushButton.clicked.connect(self._engender_tree)

    def _engender_tree(self):
        # Инициализация белого окна
        pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
        quit_mode = False
        tree = get_three_level_tree()
        segments = tree.get_children_branches_as_segments(tree.root)
        while not quit_mode:
            selected_height_tree = random.randint(0, tree.root.height)
            selected_branches = tree.get_branches_by_height(selected_height_tree)
            selected_indexes = tree.get_indexes_by_branches(selected_branches)
            selected_segments = tree.represent_branches_as_segments(selected_branches)
            self.draw(segments, selected_segments)

            for index, branch in enumerate(selected_branches):
                if selected_indexes[index] == 0:
                    delta_angle = 0
                else:
                    delta_angle = random.randint(MIN_ANGLE, MAX_ANGLE)
                new_branch = increase_segment(segments[selected_indexes[index]], delta_angle, LENGTH_K)
                selected_branch = tree.get_branch_by_index(selected_indexes[index])
                children = selected_branch.children
                for child in children:
                    s = increase_segment(Segment(selected_branch.segment.start, child.segment.start), delta_angle, LENGTH_K)
                    delta_x = s.finish.x - child.segment.start.x
                    delta_y = s.finish.y - child.segment.start.y
                    child.segment.start = s.finish
                    child.segment.finish.x += delta_x
                    child.segment.finish.y += delta_y
                    self.recursive_shift_coords(child, delta_x, delta_y)
                tree.update_branch(segments[selected_indexes[index]], new_branch)

            segments = tree.get_children_branches_as_segments(tree.root)
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
                        pass
                    elif event.key == pygame.K_LEFT:
                        pass
                    elif event.key == pygame.K_UP:
                        pass
                    elif event.key == pygame.K_DOWN:
                        pass
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
    def draw(lines: List[Segment], selected_lines=None):
        # Черный цвет пера для отображения прямых
        glColor3f(0.0, 0.0, 0.0)
        glLineWidth(2)
        if selected_lines is not None:
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
                    for line in selected_lines:
                        glBegin(GL_LINES)
                        glColor3f(1.0, 0.0, 0.0)
                        glVertex2f(line.start.x, line.start.y)
                        glVertex2f(line.finish.x, line.finish.y)
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

    def recursive_shift_coords(self, parent: Branch, delta_x: float, delta_y: float):
        for child in parent.children:
            child.segment.start.x += delta_x
            child.segment.start.y += delta_y
            child.segment.finish.x += delta_x
            child.segment.finish.y += delta_y

            if child.children:
                self.recursive_shift_coords(child, delta_x, delta_y)


def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Application()                  # Создаём объект класса Application
    window.show()                           # Показываем окно
    app.exec_()                             # и запускаем приложение


if __name__ == '__main__':
    main()
