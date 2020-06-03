import math
import numpy
from typing import List

from geometry.constants import ABSCISSA, ORDINATE
from geometry.entity_2d import Point, Segment


def calculate_equidistant_point(p1: Point, p2: Point, height) -> Point:
    """
    Вычсиление точки, являющейся:
        - равноудаленной от точек p1 и p2
        - точкой, через которую можно провести перпендикуляр к отрезку (p1, p2) высотой height

    :param p1: Начальная точка
    :param p2: Конечная точка
    :param height: Величина перпендикуляра, опущенного на отрезок, представленный  точками p1 и p2
    :return: Равноудаленная точка
    """

    x = (p1.x + p2.x) / 2.0 + (height / (math.sqrt((p1.y - p2.y) ** 2 + (p2.x - p1.x) ** 2))) * (p1.y - p2.y)
    y = (p1.y + p2.y) / 2.0 + (height / (math.sqrt((p1.y - p2.y) ** 2 + (p2.x - p1.x) ** 2))) * (p2.x - p1.x)

    return Point(x, y)


def divide_into_two_equal_parts(p1, p2):
    """
    Деление отрезка, представленного двумя точками p1 и p2, на две равные части.

    :param p1: Начальная точка, представленная кортежем вида: (x, y)
    :param p2: Конечная точка, представленная кортежем вида: (x, y)
    :return: Равные отрезки, представленные в виде кортежа точек (x1, y1), (x2, y2), (x3, y3)
    """

    x = 1.0 / 2.0 * (p1[0] + p2[0])
    y = 1.0 / 2.0 * (p1[1] + p2[1])

    return p1, (x, y), p2


def engender_segment(segment: Segment, length: float) -> None:
    """

    :param segment:
    :param length:
    :return:
    """

    delta_l = length / 2.0
    angle = segment.get_triangle_angle()

    if angle == 90:
        segment.start.y -= delta_l
        segment.finish.y += delta_l
    elif angle == 0:
        segment.start.x -= delta_l
        segment.finish.x += delta_l
    elif 0 < angle < 90:
        segment.start.x -= delta_l * math.cos(angle * math.pi / 180.0)
        segment.start.y -= delta_l * math.sin(angle * math.pi / 180.0)
        segment.finish.x += delta_l * math.cos(angle * math.pi / 180.0)
        segment.finish.y += delta_l * math.sin(angle * math.pi / 180.0)
    else:
        segment.start.x += delta_l * math.cos((180.0 - angle) * math.pi / 180.0)
        segment.start.y -= delta_l * math.sin((180.0 - angle) * math.pi / 180.0)
        segment.finish.x -= delta_l * math.cos((180.0 - angle) * math.pi / 180.0)
        segment.finish.y += delta_l * math.sin((180.0 - angle) * math.pi / 180.0)


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
