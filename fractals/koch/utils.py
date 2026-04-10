import math
import random
from typing import List

from geometry.entity_2d import Point, Segment

def calc_base_base_struct(h: float, length: float, point: Point, struct_angle: float, triangle_angle: float) -> \
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

def calc_base_struct(h: float, length: float, point: Point, struct_angle: float, triangle_angle: float,
                     prev_segment: Segment = None, beginner_will_char_grow: bool = True, **kwargs) -> List[Segment]:
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
    :param prev_segment: Родительский отрезок.
    :param beginner_will_char_grow: Будет ли расти по величине сам треугольник для параметра.
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

    # Создаем тут многофазность за счет того, что корректируем кол-во итераций роста от порядка фрактала
    if kwargs.get('model') and kwargs.get('model') == 'several':
        count_iterations = prev_segment.max_iter + int(prev_segment.max_iter * 0.1 * (prev_segment.depth + 1))
    else:
        count_iterations = prev_segment.max_iter

    seg_weight_1 = seg_weight_2 = seg_weight_3 = seg_weight_4 = 0
    max_seg_weight_1 = max_seg_weight_2 = max_seg_weight_3 = max_seg_weight_4 = 0
    dt_seg_weight_1 = dt_seg_weight_2 = dt_seg_weight_3 = dt_seg_weight_4 = 0
    if kwargs and kwargs.get('max_char_val_from', None):
        seg_weight_1 = prev_segment.max_weight / 2.0
        seg_weight_4 = prev_segment.max_weight / 2.0

        # TODO: Для того, чтобы сделать спект вариативным
        max_seg_weight_4 = prev_segment.max_weight + random.uniform((prev_segment.max_weight / 2.0) * 0.05, (prev_segment.max_weight / 2.0) * 0.6)
        max_seg_weight_1 = prev_segment.max_weight + random.uniform((prev_segment.max_weight / 2.0) * 0.05, (prev_segment.max_weight / 2.0) * 0.6)
        #
        # max_seg_weight_4 = prev_segment.max_weight
        # max_seg_weight_1 = prev_segment.max_weight

        ## TODO: Так ли это?
        # rnd = random.uniform(kwargs['max_char_val_from'], kwargs['max_char_val_to'])
        # max_seg_weight_2 = random.uniform(kwargs['max_char_val_from'], kwargs['max_char_val_to'])
        # max_seg_weight_3 = random.uniform(kwargs['max_char_val_from'], kwargs['max_char_val_to'])

        # TODO: Для того, чтобы сделать спект вариативным
        if kwargs.get('spectr_variant'):
            if kwargs.get('spectr_variant') == 'ordinary_numerator':
                max_seg_weight_2 = random.uniform(kwargs['max_char_val_from'] * (prev_segment.depth + 1), kwargs['max_char_val_to'] * (prev_segment.depth + 1))
                max_seg_weight_3 = random.uniform(kwargs['max_char_val_from'] * (prev_segment.depth + 1), kwargs['max_char_val_to'] * (prev_segment.depth + 1))
            elif kwargs.get('spectr_variant') == 'ordinary_denominator':
                max_seg_weight_2 = random.uniform(kwargs['max_char_val_from'] / (prev_segment.depth + 1), kwargs['max_char_val_to'] * (prev_segment.depth + 1))
                max_seg_weight_3 = random.uniform(kwargs['max_char_val_from'] / (prev_segment.depth + 1), kwargs['max_char_val_to'] * (prev_segment.depth + 1))
            elif kwargs.get('spectr_variant') == 'quadratic_numerator':
                max_seg_weight_2 = random.uniform(kwargs['max_char_val_from'] * prev_segment.depth * (prev_segment.depth + 1), kwargs['max_char_val_to'] * prev_segment.depth * (prev_segment.depth + 1))
                max_seg_weight_3 = random.uniform(kwargs['max_char_val_from'] * prev_segment.depth * (prev_segment.depth + 1), kwargs['max_char_val_to'] * prev_segment.depth * (prev_segment.depth + 1))
            elif kwargs.get('spectr_variant') == 'quadratic_denominator':
                max_seg_weight_2 = random.uniform(kwargs['max_char_val_from'] / (prev_segment.depth * (prev_segment.depth + 1)), kwargs['max_char_val_to'] / (prev_segment.depth * (prev_segment.depth + 1)))
                max_seg_weight_3 = random.uniform(kwargs['max_char_val_from'] / (prev_segment.depth * (prev_segment.depth + 1)), kwargs['max_char_val_to'] / (prev_segment.depth * (prev_segment.depth + 1)))
            else:
                raise 'Unknown spectr_variant'
        else:
            max_seg_weight_2 = random.uniform(kwargs['max_char_val_from']/(prev_segment.depth + 1), kwargs['max_char_val_to']/(prev_segment.depth + 1))
            max_seg_weight_3 = random.uniform(kwargs['max_char_val_from']/(prev_segment.depth + 1), kwargs['max_char_val_to']/(prev_segment.depth + 1))

        # TODO: Место для второго рисунка гистограммы масс для статьи
        # max_seg_weight_2 = random.uniform(kwargs['max_char_val_from'], kwargs['max_char_val_to'])
        # max_seg_weight_3 = random.uniform(kwargs['max_char_val_from'], kwargs['max_char_val_to'])
        seg_weight_2 = max_seg_weight_2 / float(count_iterations * 100) # TODO: Сделать коэффициент не из потолка, а из длины. А откуда длина начальная взялась - другой вопрос :)
        seg_weight_3 = max_seg_weight_3 / float(count_iterations * 100)
        if not beginner_will_char_grow:
            max_seg_weight_2 = 0
            max_seg_weight_3 = 0
            seg_weight_2 = 0
            seg_weight_3 = 0
            seg_weight_1 = prev_segment.max_weight / 2.0
            seg_weight_4 = prev_segment.max_weight / 2.0

        if beginner_will_char_grow and prev_segment.max_weight == 0:
            max_seg_weight_1 = 0.0
            max_seg_weight_4 = 0.0
            seg_weight_1 = 0.0
            seg_weight_4 = 0.0

    segment_1 = Segment(Point(point.x, point.y), Point(x_2, y_2), weight=seg_weight_1, dt_length=None, dt_weight=dt_seg_weight_1, max_weight=max_seg_weight_1, cur_iter=1, max_iter=prev_segment.max_iter, depth=prev_segment.depth)
    segment_2 = Segment(Point(x_2, y_2), Point(x_3, y_3), weight=seg_weight_2, dt_length=None, dt_weight=dt_seg_weight_2, max_weight=max_seg_weight_2, cur_iter=1, max_iter=count_iterations, depth=prev_segment.depth)
    segment_3 = Segment(Point(x_3, y_3), Point(x_4, y_4), weight=seg_weight_3, dt_length=None, dt_weight=dt_seg_weight_3, max_weight=max_seg_weight_3, cur_iter=1, max_iter=count_iterations, depth=prev_segment.depth)
    segment_4 = Segment(Point(x_4, y_4), Point(x_5, y_5), weight=seg_weight_4, dt_length=None, dt_weight=dt_seg_weight_4, max_weight=max_seg_weight_4, cur_iter=1, max_iter=prev_segment.max_iter, depth=prev_segment.depth)

    if kwargs.get('model') and kwargs.get('model') == 'stochastic':
        a = random.randrange(10) * 0.001
        if random.randrange(10) < 5:
            a *= -1
        max_val = kwargs['max_val'] + a

        segment_1.dt_length = (max_val - segment_1.len()) / float(prev_segment.max_iter - 1)
        segment_2.dt_length = (max_val - segment_2.len()) / float(count_iterations - 1)
        segment_3.dt_length = (max_val - segment_3.len()) / float(count_iterations - 1)
        segment_4.dt_length = (max_val - segment_4.len()) / float(prev_segment.max_iter - 1)
    else:
        # TODO: Сделать тут попытку закономерности длины отрезков центрального треугольника от порядка фрактала
        if kwargs.get('pattern'):
            segment_1.dt_length = (prev_segment.max_length - segment_1.len()) / float(prev_segment.max_iter - 1)
            segment_2.dt_length = (kwargs.get('pattern').get(prev_segment.depth) - segment_2.len()) / float(count_iterations - 1)
            segment_3.dt_length = (kwargs.get('pattern').get(prev_segment.depth) - segment_3.len()) / float(count_iterations - 1)
            segment_4.dt_length = (prev_segment.max_length - segment_4.len()) / float(prev_segment.max_iter - 1)

            segment_1.max_length = prev_segment.max_length
            segment_2.max_length = kwargs.get('pattern').get(prev_segment.depth)
            segment_3.max_length = kwargs.get('pattern').get(prev_segment.depth)
            segment_4.max_length = prev_segment.max_length
        else:
            segment_1.dt_length = (kwargs['max_val'] - segment_1.len()) / float(prev_segment.max_iter - 1)
            segment_2.dt_length = (kwargs['max_val'] - segment_2.len()) / float(count_iterations - 1)
            segment_3.dt_length = (kwargs['max_val'] - segment_3.len()) / float(count_iterations - 1)
            segment_4.dt_length = (kwargs['max_val'] - segment_4.len()) / float(prev_segment.max_iter - 1)

    if kwargs and kwargs.get('max_char_val_from', None):
        dt_seg_weight_1 =  (max_seg_weight_1 - seg_weight_1) / float(prev_segment.max_iter - 1)
        dt_seg_weight_4 =  (max_seg_weight_4 - seg_weight_4) / float(prev_segment.max_iter - 1)
        dt_seg_weight_2 = (max_seg_weight_2 - seg_weight_2) / float(count_iterations)
        dt_seg_weight_3 = (max_seg_weight_3 - seg_weight_3) / float(count_iterations)

        segment_1.dt_weight = dt_seg_weight_1
        segment_2.dt_weight = dt_seg_weight_2
        segment_3.dt_weight = dt_seg_weight_3
        segment_4.dt_weight = dt_seg_weight_4

        # segment_2.weight = dt_seg_weight_2
        # segment_3.weight = dt_seg_weight_3

    return [segment_1, segment_2, segment_3, segment_4]


def calc_new_base_struct(h: float, length: float, point: Point, struct_angle: float, triangle_angle: float,
                     prev_segment: Segment = None, beginner_will_char_grow: bool = True, **kwargs) -> List[Segment]:
    """
    Вычисление новой-измененной базовой структуры формирования фрактала `Кривая коха` c текущими значениями высоты треугольника h и
    отрезками length, не принадлежащие самому треугольнику. Фигура задается пятью точками или четырьмя отрезками и
    имеет следующий вид:

                              (x3, y3)
                                  *
                                 /|\
                                / | \
                   length      /  |h \
    (x1, y1)*-----------------*   |   *-----------------*(x5, y5)
                        (x2, y2)    (x4, y4)
    Отличие от привычной базовой структуры заключается в том, что треугольник вцетре не равнобедренный, а произвольный.
    В данном случае - прямоугольный.
    :param h: Высота треугольника.
    :param length: Длина отрезков [(x1, y1), (x2, y2)] и [(x4, y4), (x5, y5)].
    :param point: Начальная точка (x1, y1), на основе которой просиходит формирование структуры.
    :param struct_angle: Угол наклона структуры.
    :param triangle_angle: Угол равнобедренного треугольника.
    :param prev_segment: Родительский отрезок.
    :param beginner_will_char_grow: Будет ли расти по величине сам треугольник для параметра.
    :return: Список отрезков вычисленной структуры.
    """
    x_2 = point.x + length * math.cos(struct_angle * math.pi / 180.0)
    y_2 = point.y + length * math.sin(struct_angle * math.pi / 180.0)

    # x_3 = x_2 + (h * math.cos((struct_angle + triangle_angle) * math.pi / 180.0)) / math.sin(
    #     triangle_angle * math.pi / 180.0)
    # y_3 = y_2 + (h * math.sin((struct_angle + triangle_angle) * math.pi / 180.0)) / math.sin(
    #     triangle_angle * math.pi / 180.0)
    #
    # x_4 = x_3 + (h * math.cos((struct_angle-kwargs['metamorphosis_angle']) * math.pi / 180.0)) / math.sin(
    #     kwargs['metamorphosis_angle'] * math.pi / 180.0)
    # y_4 = y_3 + (h * math.sin((struct_angle-kwargs['metamorphosis_angle']) * math.pi / 180.0)) / math.sin(
    #     kwargs['metamorphosis_angle'] * math.pi / 180.0)

    current_depth = prev_segment.depth + 1

    x_3 = x_2 + (h * math.cos((struct_angle + kwargs['metamorphosis'][current_depth]['left_angle']) * math.pi / 180.0)) / math.sin(
        kwargs['metamorphosis'][current_depth]['left_angle'] * math.pi / 180.0)
    y_3 = y_2 + (h * math.sin((struct_angle + kwargs['metamorphosis'][current_depth]['left_angle']) * math.pi / 180.0)) / math.sin(
        kwargs['metamorphosis'][current_depth]['left_angle'] * math.pi / 180.0)

    x_4 = x_3 + (h * math.cos((struct_angle-kwargs['metamorphosis'][current_depth]['right_angle']) * math.pi / 180.0)) / math.sin(
        kwargs['metamorphosis'][current_depth]['right_angle'] * math.pi / 180.0)
    y_4 = y_3 + (h * math.sin((struct_angle-kwargs['metamorphosis'][current_depth]['right_angle']) * math.pi / 180.0)) / math.sin(
        kwargs['metamorphosis'][current_depth]['right_angle'] * math.pi / 180.0)

    x_5 = x_4 + length * math.cos(struct_angle * math.pi / 180.0)
    y_5 = y_4 + length * math.sin(struct_angle * math.pi / 180.0)

    # Создаем тут многофазность за счет того, что корректируем кол-во итераций роста от порядка фрактала
    if kwargs.get('model') and kwargs.get('model') == 'several':
        count_iterations = prev_segment.max_iter + int(prev_segment.max_iter * 0.1 * (prev_segment.depth + 1))
    else:
        count_iterations = prev_segment.max_iter

    segment_1 = Segment(Point(point.x, point.y), Point(x_2, y_2), dt_length=None, cur_iter=1, max_iter=prev_segment.max_iter, depth=prev_segment.depth)
    segment_2 = Segment(Point(x_2, y_2), Point(x_3, y_3), dt_length=None, cur_iter=1, max_iter=count_iterations, depth=prev_segment.depth)
    segment_3 = Segment(Point(x_3, y_3), Point(x_4, y_4), dt_length=None, cur_iter=1, max_iter=count_iterations, depth=prev_segment.depth)
    segment_4 = Segment(Point(x_4, y_4), Point(x_5, y_5),  dt_length=None, cur_iter=1, max_iter=prev_segment.max_iter, depth=prev_segment.depth)

    # # TODO: Сделать тут попытку закономерности длины отрезков центрального треугольника от порядка фрактала
    # if kwargs.get('pattern'):
    #     segment_1.dt_length = (prev_segment.max_length - segment_1.len()) / float(prev_segment.max_iter - 1)
    #     segment_2.dt_length = (kwargs.get('pattern').get(prev_segment.depth) - segment_2.len()) / float(count_iterations - 1)
    #     segment_3.dt_length = (kwargs.get('pattern').get(prev_segment.depth) - segment_3.len()) / float(count_iterations - 1)
    #     segment_4.dt_length = (prev_segment.max_length - segment_4.len()) / float(prev_segment.max_iter - 1)
    #
    #     segment_1.max_length = prev_segment.max_length
    #     segment_2.max_length = kwargs.get('pattern').get(prev_segment.depth)
    #     segment_3.max_length = kwargs.get('pattern').get(prev_segment.depth)
    #     segment_4.max_length = prev_segment.max_length
    # else:
    #     ss = kwargs['max_val'] * math.sin(triangle_angle * math.pi / 180.0) / math.sin(kwargs['metamorphosis_angle'] * math.pi / 180.0)
    #
    #     segment_1.dt_length = (kwargs['max_val'] - segment_1.len()) / float(prev_segment.max_iter - 1)
    #     segment_2.dt_length = (kwargs['max_val'] - segment_2.len()) / float(count_iterations - 1)
    #     segment_3.dt_length = (ss - segment_3.len()) / float(count_iterations - 1)
    #     segment_4.dt_length = (kwargs['max_val'] - segment_4.len()) / float(prev_segment.max_iter - 1)
    #
    #     segment_1.max_length = kwargs['max_val']
    #     segment_2.max_length = kwargs['max_val']
    #     segment_3.max_length = ss
    #     segment_4.max_length = kwargs['max_val']

    ss = kwargs['metamorphosis'][current_depth]['max_length'] * math.sin(kwargs['metamorphosis'][current_depth]['left_angle'] * math.pi / 180.0) / math.sin(kwargs['metamorphosis'][current_depth]['right_angle'] * math.pi / 180.0)

    segment_1.dt_length = (kwargs['metamorphosis'][current_depth]['max_length'] - segment_1.len()) / float(prev_segment.max_iter - 1)
    segment_2.dt_length = (kwargs['metamorphosis'][current_depth]['max_length'] - segment_2.len()) / float(count_iterations - 1)
    segment_3.dt_length = (ss - segment_3.len()) / float(count_iterations - 1)
    segment_4.dt_length = (kwargs['metamorphosis'][current_depth]['max_length'] - segment_4.len()) / float(prev_segment.max_iter - 1)

    segment_1.max_length = kwargs['metamorphosis'][current_depth]['max_length']
    segment_2.max_length = kwargs['metamorphosis'][current_depth]['max_length']
    segment_3.max_length = ss
    segment_4.max_length = kwargs['metamorphosis'][current_depth]['max_length']

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
