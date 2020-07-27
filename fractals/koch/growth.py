from typing import List

from geometry.entity_2d import Segment, Point
from ontogeny.utils import increase_segment_length


def calc_segment_phases(center: Point, count_iter: int, len_limit: float) -> List[List[Segment]]:
    """
    Вычисление списка промежуточных фаз роста отрезка за count_iter итераций. Отрезок строится относительно точки center
    и выростает до значения длины len_limit.
    :param center: Центр отрезка.
    :param count_iter: Количество итераций роста отрезка.
    :param len_limit: Предельная величина длины отрезка.
    :return: Список промежуточных фаз роста отрезка.
    """
    lines = []

    segment = Segment(Point(center.x - 0.001, center.y), Point(center.x + 0.001, center.y))
    lines.append([segment])

    while segment.len() < len_limit:
        segment = Segment(Point(segment.start.x, segment.start.y), Point(segment.finish.x, segment.finish.y))
        increase_segment_length(segment, len_limit / count_iter)

        lines.append([segment])

    return lines
