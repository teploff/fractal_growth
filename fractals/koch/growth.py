import random
from typing import List

from geometry.entity_2d import Segment, Point
from ontogeny.utils import increase_segment_length


def calc_segment_phases(center: Point, count_iter: int, len_limit: float, beginner_will_char_grow: bool = True, **kwargs) -> List[List[Segment]]:
    """
    Вычисление списка промежуточных фаз роста отрезка за count_iter итераций. Отрезок строится относительно точки center
    и выростает до значения длины len_limit.
    :param center: Центр отрезка.
    :param count_iter: Количество итераций роста отрезка.
    :param len_limit: Предельная величина длины отрезка.
    :param beginner_will_char_grow: Будет ли расти по величине сам треугольник для параметра.
    :return: Список промежуточных фаз роста отрезка.
    """
    lines = []
    tmp_weight = weight_iter = max_char_val = 0

    if kwargs and kwargs.get('max_char_val_from', None):
        max_char_val = random.uniform(kwargs['max_char_val_from'], kwargs['max_char_val_to'])
        tmp_weight = weight_iter = max_char_val / float(count_iter)
        if not beginner_will_char_grow:
            max_char_val = 0.0
            tmp_weight = 0.0
            weight_iter = 0.0

    cur_iter = 1

    segment = Segment(Point(center.x - 0.001, center.y), Point(center.x + 0.001, center.y), weight=tmp_weight, dt_weight=weight_iter, cur_iter=cur_iter, max_iter=count_iter, depth=0, max_length=kwargs['max_val'])
    dt_length = (len_limit - segment.len()) / float(count_iter - 2)
    segment.dt_length = dt_length

    lines.append([segment])

    while segment.cur_iter != count_iter:
        tmp_weight += weight_iter
        cur_iter += 1

        segment = Segment(Point(segment.start.x, segment.start.y), Point(segment.finish.x, segment.finish.y), weight=tmp_weight, dt_weight=weight_iter, dt_length=dt_length, max_weight=max_char_val, cur_iter=cur_iter, max_iter=count_iter, max_length=kwargs['max_val'])
        increase_segment_length(segment, dt_length)

        lines.append([segment])

    return lines
