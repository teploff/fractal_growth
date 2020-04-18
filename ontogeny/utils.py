import math
import numpy
from typing import List

from geometry.constants import ABSCISSA, ORDINATE
from geometry.entity_2d import Point, Segment


def engender_branch(bud: Point, length: float, angle: float) -> Point:
    """
    Наростить (создать) ветку (отрезок) от текущей почки (точки) на заданную длину.
    :param bud: Почка (точка) от которой происходит рост ветки (отрезка)
    :param length: Величина длины ветки (отрезка)
    :param angle: Угол поворота относительно Ox
    :return: Конечная почка (точка) на созданной ветке (отрезке)
    """

    x = bud.x + (length * math.cos(angle * math.pi / 180.0))
    y = bud.y + (length * math.sin(angle * math.pi / 180.0))

    return Point(x, y)


def increase_segment(segment: Segment, delta_angle: float, k_length: float) -> Segment:
    """
    Увеличить длину отрезка на коеффициент k_length при этом повернув его на значение угла радиус-вектора delta_angle.
    :param segment: Исходный отрезок, который подвергается увеличению
    :param delta_angle: Угол поворота или меру поворота подвижного радиус-вектора относительно его начального положения
    :param k_length: Коеффициент увеличения длины
    :return: Увеличенный отрезок
    """

    if k_length <= 1:
        raise ValueError('Length coefficient must be more than 1 ')

    angle = segment.get_triangle_angle() + delta_angle
    length = segment.len() * k_length

    finish_point = engender_branch(segment.start, length, angle)

    return Segment(segment.start, finish_point)


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
    d_x = abs(branch.start.x - branch.finish.x)
    d_y = abs(branch.start.y - branch.finish.y)

    if d_x > d_y:
        selected_axis = ABSCISSA
        values = numpy.random.uniform(branch.start.x, branch.finish.x, size=(1, count_buds))
    else:
        selected_axis = ORDINATE
        values = numpy.random.uniform(branch.start.y, branch.finish.y, size=(1, count_buds))

    return [branch.find_point_with_one_coord(coordinate, selected_axis) for coordinate in values[0]]
