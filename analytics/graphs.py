import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from typing import List
from geometry.entity_2d import Segment


def plot_graph_line_len(lines: List[List[Segment]], count_iterations: int) -> None:
    """
    Формирование графика зависимости длины фрактальной линии от числа циклов роста.
    :param lines: Список промежуточных фаз роста (списков отрезков) фрактальной структуры.
    :param count_iterations: Количество циклов роста отрезка а.
    :return:
    """

    x_train = np.array([i for i in range(len(lines))])
    y_train = np.array([sum(line.len() for line in lines) for i, lines in enumerate(lines)])
    y = np.array([sum(line.len() for line in lines)
                  for i, lines in enumerate(lines) if i % (count_iterations - 1) == 0])
    x = np.array([i for i in range(len(lines)) if i % (count_iterations - 1) == 0])

    [a, b], res1 = curve_fit(lambda x1, k1, k2: k1 * np.exp(k2 * x1), x_train, y_train, p0=[0.01285, 0.0351])

    y1 = a * np.exp(b * x_train)
    fig, ax = plt.subplots()
    ax.plot(x, y, 'o', label='Original data', markersize=5)
    ax.plot(x_train, y1)
    ax.set(xlabel='Число циклов роста фрактала, ед.', ylabel='Длина фрактальной линии, ед.')
    ax.grid(True)
    plt.show()


def plot_graph_scale(lines: List[List[Segment]], count_iterations: int) -> None:
    """
    Формирование графика зависимости величина размаха фрактала от числа циклов роста.
    :param lines: Список промежуточных фаз роста (списков отрезков) фрактальной структуры.
    :param count_iterations: Количество циклов роста отрезка а.
    :return:
    """

    # TODO: refactoring -> lines lines ...
    y_x_train = [abs(max(max(line.start.x, line.finish.x) for line in lines) - min(min(line.start.x, line.finish.x) for line in lines)) for lines in lines]
    y_x = [value for i, value in enumerate(y_x_train)
           if i % (count_iterations - 1) == 0]
    y_y_train = [abs(max(max(line.start.y, line.finish.y) for line in lines) -
             min(min(line.start.y, line.finish.y) for line in lines)) for lines in lines]
    y_y = [value for i, value in enumerate(y_y_train)
           if i % (count_iterations - 1) == 0]
    x_train = [i for i in range(len(lines))]
    x = [i for i in range(len(lines)) if i % (count_iterations - 1) == 0]

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
