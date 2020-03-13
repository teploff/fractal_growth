import numpy
from typing import List

from geometry.entity_2d import ABSCISSA, ORDINATE, Point, Segment


def engender_random_buds(branch: Segment, count_buds: int) -> List[Point]:
    """
    Найти (наростить) при помощи генератора случайных чисел точки (почки) на отрезке (ветке).
    :param branch: Ветка, на которой необходимо наростить почки
    :param count_buds: Требуемое количество почек
    :return: Результирующий массив почек
    """

    # Находим величины дельт по x и y для того, чтобы понимать на каких именно координатах производить рост (random)
    # почек. Возможен случай, что ветка (отрезок) перпендикулярна Оу или Оx. В первом случае необходимо прозводить рост
    # (random) по координатам x, иначе по координатам y
    d_x = abs(branch.point_1.x - branch.point_2.x)
    d_y = abs(branch.point_1.y - branch.point_2.y)

    if d_x > d_y:
        selected_axis = ABSCISSA
        values = numpy.random.uniform(branch.point_1.x, branch.point_2.x, size=(1, count_buds))
    else:
        selected_axis = ORDINATE
        values = numpy.random.uniform(branch.point_1.y, branch.point_2.y, size=(1, count_buds))

    return [branch.find_point(coordinate, selected_axis) for coordinate in values[0]]
