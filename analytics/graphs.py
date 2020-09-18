import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import numpy as np
from typing import List
from geometry.entity_2d import Segment


def plot_line_len(lines: List[List[Segment]], count_iterations: int) -> None:
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


def plot_scale(lines: List[List[Segment]], count_iterations: int) -> None:
    """
    Формирование графика зависимости величина размаха фрактала от числа циклов роста.
    :param lines: Список промежуточных фаз роста (списков отрезков) фрактальной структуры.
    :param count_iterations: Количество циклов роста отрезка а.
    :return:
    """

    y_x_train = [
        abs(max(max(line.start.x, line.finish.x) for line in segments) - min(min(line.start.x, line.finish.x) for line in segments)) for segments in lines]
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


def plot_angle(lines: List[List[Segment]], count_iterations: int, angle: float):
    """
    :param lines: Список промежуточных фаз роста (списков отрезков) фрактальной структуры.
    :param count_iterations: Количество циклов роста отрезка а.
    :param angle: Угол равнобедренного треугольника базовой треугольной струкутры.
    :return:
    """

    eps = 0.2
    theta = [[np.deg2rad(line.get_triangle_angle()) for line in lines] for i, lines in enumerate(lines)
             if i % (count_iterations - 1) == 0]
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
    ax.set_title(r'$\beta=' + str(int(angle)) + r'°$', va='bottom', fontsize=30)

    plt.show()


def plot_line_len_single_several_phases(
        one_phase_segments: List[List[Segment]],
        several_phases_segments_1: List[List[Segment]],
        several_phases_segments_2: List[List[Segment]],
        count_iterations: int,
        max_a_len: float
) -> None:
    """

    :return:
    """

    # TODO: to name this shirt
    line_lens_train_single = [sum(line.len() for line in lines) for lines in one_phase_segments]
    # delete points of line growth
    x_x_train = [i for i in range(len(line_lens_train_single))]
    y_y_train = line_lens_train_single[:]

    y3_y = np.array([max_a_len * 4 ** ((i + 1) / count_iterations)
                     for i in range(len(line_lens_train_single))])

    line_lens_train_single = [(i, value) for i, value in enumerate(line_lens_train_single)
                              if i % (count_iterations - 1) == 0]
    x_train_single = [pair[0] for pair in line_lens_train_single]
    line_lens_train_single = [pair[1] for pair in line_lens_train_single]

    line_lens_train_several = [sum(line.len() for line in lines) for lines in several_phases_segments_1]
    # delete points of line growth
    x_train_several = [i for i in range(len(line_lens_train_several))]

    line_lens_train_several_2 = [sum(line.len() for line in lines) for lines in several_phases_segments_2]
    # delete points of line growth
    x_train_several_2 = [i for i in range(len(line_lens_train_several_2))]

    fig, ax = plt.subplots()
    ax.plot(x_x_train, y_y_train, label=r'$a$', c='black', linewidth=5)
    ax.plot(x_train_several, line_lens_train_several, linestyle=":", label=r'$b$', c='black', linewidth=5)
    ax.plot(x_train_several_2, line_lens_train_several_2, linestyle="--", label=r'$c$', c='black', linewidth=5)
    ax.plot(x_train_single, line_lens_train_single, 's', markersize=10, markeredgewidth=3, label=r'$f_1$', c='black')

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


def plot_graph_scale_one_and_several_phases(self):
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
