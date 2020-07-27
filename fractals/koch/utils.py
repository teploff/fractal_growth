import math
from typing import List

from geometry.entity_2d import Point, Segment


def calc_base_struct(h: float, length: float, point: Point, struct_angle: float, triangle_angle: float) -> \
        List[Segment]:
    """
    Вычисление базовой структуры формирования фрактала `Кривая коха` c текущими значениями высоты треугольника h и
    отрезками length, не принадлежащие самому треугольнику. Фигура задается пятью точками или четырьмя отрезками и
    имеет следующий вид:

                              (x3, y3)
                                  *
                                 /|\
                                / | \
                   length      /  |h \
    (x1, y1)*-----------------*   |   *-----------------*(x5, y5)
                        (x2, y2)    (x4, y4)

    :param h: Высота треугольника.
    :param length: Длина отрезков [(x1, y1), (x2, y2)] и [(x4, y4), (x5, y5)].
    :param point: Начальная точка (x1, y1), на основе которой просиходит формирование структуры.
    :param struct_angle: Угол наклона структуры.
    :param triangle_angle: Угол равнобедренного треугольника.
    :return: Список отрезков вычисленной структуры.
    """
    x_2 = point.x + length * math.cos(struct_angle * math.pi / 180.0)
    y_2 = point.y + length * math.sin(struct_angle * math.pi / 180.0)

    x_3 = x_2 + (h * math.cos((struct_angle + triangle_angle) * math.pi / 180.0)) / math.sin(
        triangle_angle * math.pi / 180.0)
    y_3 = y_2 + (h * math.sin((struct_angle + triangle_angle) * math.pi / 180.0)) / math.sin(
        triangle_angle * math.pi / 180.0)

    x_4 = x_3 + (h * math.cos((triangle_angle - struct_angle) * math.pi / 180.0)) / math.sin(
        triangle_angle * math.pi / 180.0)
    y_4 = y_3 - (h * math.sin((triangle_angle - struct_angle) * math.pi / 180.0)) / math.sin(
        triangle_angle * math.pi / 180.0)

    x_5 = x_4 + length * math.cos(struct_angle * math.pi / 180.0)
    y_5 = y_4 + length * math.sin(struct_angle * math.pi / 180.0)

    segment_1 = Segment(Point(point.x, point.y), Point(x_2, y_2))
    segment_2 = Segment(Point(x_2, y_2), Point(x_3, y_3))
    segment_3 = Segment(Point(x_3, y_3), Point(x_4, y_4))
    segment_4 = Segment(Point(x_4, y_4), Point(x_5, y_5))

    return [segment_1, segment_2, segment_3, segment_4]


def cal_regular_frame(center: Point, corners_n: int, side_length: float) -> List[Segment]:
    """
    Вычисление правильной фигуры (равносторонний треугольник, квадрат, правильный пятиугольник и т.д.).
    :param center: Координата центральной, равноудаленной точки от заданных углов правильной фигуры.
    :param corners_n: Количество углов правильной фигуры.
    :param side_length: Величина стороны фигуры.
    :return: Список отрезков (замкнутный полигон фигуры).
    """
    points = []

    for i in range(corners_n):
        x = side_length / (2 * math.sin(math.pi / corners_n)) * math.cos(2 * math.pi * i / corners_n) + center.x
        y = side_length / (2 * math.sin(math.pi / corners_n)) * math.sin(2 * math.pi * i / corners_n) + center.y
        points.append(Point(x, y))

    return [Segment(points[i], points[i + 1]) for i in range(-1, corners_n - 1)]


def stick_segments(segments: List[Segment], point: Point) -> List[Segment]:
    """
    Склеивание отрезков segments относительно точки point. ВАЖНО: количество отрезкво в списке segments должно быть
    четно, потому что используется метод дихотомии.
    :param segments: Список отрезков.
    :param point: Точка, относительно которой происходит склеивание.
    :return: Список склеянных отрезков относительно точки point.
    """
    # TODO: make it pretty!!!
    dx = point.x - segments[len(segments) // 2 - 1].finish.x
    dy = point.y - segments[len(segments) // 2 - 1].finish.y
    segments[len(segments) // 2 - 1].start.x += dx
    segments[len(segments) // 2 - 1].start.y += dy
    segments[len(segments) // 2 - 1].finish.x += dx
    segments[len(segments) // 2 - 1].finish.y += dy
    reference_point = segments[len(segments) // 2 - 1].start
    left_side = segments[:len(segments) // 2 - 1]
    for line in left_side[::-1]:
        dx = reference_point.x - line.finish.x
        dy = reference_point.y - line.finish.y
        line.start.x += dx
        line.start.y += dy
        line.finish.x += dx
        line.finish.y += dy
        reference_point = line.start

    dx = point.x - segments[len(segments) // 2].start.x
    dy = point.y - segments[len(segments) // 2].start.y
    segments[len(segments) // 2].start.x += dx
    segments[len(segments) // 2].start.y += dy
    segments[len(segments) // 2].finish.x += dx
    segments[len(segments) // 2].finish.y += dy
    reference_point = segments[len(segments) // 2].finish
    right_side = segments[len(segments) // 2 + 1:]
    for line in right_side:
        dx = reference_point.x - line.start.x
        dy = reference_point.y - line.start.y
        line.start.x += dx
        line.start.y += dy
        line.finish.x += dx
        line.finish.y += dy
        reference_point = line.finish

    return segments
