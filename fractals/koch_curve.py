import math
from copy import deepcopy
from typing import List

from geometry.entity_2d import Segment, Point
from ontogeny.utils import engender_segment

CENTER = Point(0.0, 0.0)


class Curve:
    """

    """

    def __init__(self, count_depth: int, line_len: float, angle: float, **settings):
        """
        Инициализация параметро построения фрактальной структуры.
        :param count_depth: Глубина построения фрактала.
        :param line_len: Предельное значение длины отрезка.
        :param angle: Угол равнобередренного треугольника в градусах.
        :param settings: Дополнительные настройки.
        """

        self._count_depth = count_depth
        self._max_l_l = line_len
        self._angle = angle
        self._settings = settings

        self._active_segments = []
        self.lines = []

    def _engender_segment(self, count_iter: int):
        """

        :return:
        """

        segment = Segment(Point(CENTER.x - 0.001, CENTER.y), Point(CENTER.x + 0.001, CENTER.y))
        self.lines.append([segment])

        while segment.len() < self._max_l_l:
            segment = Segment(Point(segment.start.x, segment.start.y), Point(segment.finish.x, segment.finish.y))
            engender_segment(segment, self._max_l_l / count_iter)

            self.lines.append([segment])

        self._active_segments.append(segment)

    @staticmethod
    def _make_construction(max_iter: int, angle: float, max_length: float, start_length: float, point: Point,
                           curr_angle: float) -> List[List[Segment]]:
        """
        Формирование списков промежуточных фаз роста фрактальной структуры.
        :param max_iter: Количество итераций роста фрактальной структуры.
        :param angle: Угол равнобедренного треугольника.
        :param max_length: Предельное значение длины отрезка.
        :param start_length: Начальное знаение отрезка.
        :param point: Точка на основе которой просиходит рост.
        :param curr_angle: Угол наклона фрактальной структуры.
        :return: Список промежуточных фаз фрактальной структуры.
        """
        
        segments = []
        length = start_length
        delta_length = (max_length - start_length) / max_iter

        for iteration in range(max_iter):
            height = ((iteration + 1) / max_iter) * max_length * math.sin(angle * math.pi / 180.0)
            length += delta_length

            x_2 = point.x + length * math.cos(curr_angle * math.pi / 180.0)
            y_2 = point.y + length * math.sin(curr_angle * math.pi / 180.0)

            x_3 = x_2 + (height * math.cos((curr_angle + angle) * math.pi / 180.0)) / math.sin(angle * math.pi / 180.0)
            y_3 = y_2 + (height * math.sin((curr_angle + angle) * math.pi / 180.0)) / math.sin(angle * math.pi / 180.0)

            x_4 = x_3 + (height * math.cos((angle - curr_angle) * math.pi / 180.0)) / math.sin(angle * math.pi / 180.0)
            y_4 = y_3 - (height * math.sin((angle - curr_angle) * math.pi / 180.0)) / math.sin(angle * math.pi / 180.0)

            x_5 = x_4 + length * math.cos(curr_angle * math.pi / 180.0)
            y_5 = y_4 + length * math.sin(curr_angle * math.pi / 180.0)

            segment_1 = Segment(Point(point.x, point.y), Point(x_2, y_2))
            segment_2 = Segment(Point(x_2, y_2), Point(x_3, y_3))
            segment_3 = Segment(Point(x_3, y_3), Point(x_4, y_4))
            segment_4 = Segment(Point(x_4, y_4), Point(x_5, y_5))

            segments.append([segment_1, segment_2, segment_3, segment_4])
        
        return segments

    @staticmethod
    def _make_temp_construction(height, length, point: Point, curr_angle: float, angle: float) -> List[Segment]:
        """

        :param height:
        :param length:
        :param point:
        :param curr_angle:
        :param angle:
        :return:
        """

        x_2 = point.x + length * math.cos(curr_angle * math.pi / 180.0)
        y_2 = point.y + length * math.sin(curr_angle * math.pi / 180.0)

        x_3 = x_2 + (height * math.cos((curr_angle + angle) * math.pi / 180.0)) / math.sin(angle * math.pi / 180.0)
        y_3 = y_2 + (height * math.sin((curr_angle + angle) * math.pi / 180.0)) / math.sin(angle * math.pi / 180.0)

        x_4 = x_3 + (height * math.cos((angle - curr_angle) * math.pi / 180.0)) / math.sin(angle * math.pi / 180.0)
        y_4 = y_3 - (height * math.sin((angle - curr_angle) * math.pi / 180.0)) / math.sin(angle * math.pi / 180.0)

        x_5 = x_4 + length * math.cos(curr_angle * math.pi / 180.0)
        y_5 = y_4 + length * math.sin(curr_angle * math.pi / 180.0)

        segment_1 = Segment(Point(point.x, point.y), Point(x_2, y_2))
        segment_2 = Segment(Point(x_2, y_2), Point(x_3, y_3))
        segment_3 = Segment(Point(x_3, y_3), Point(x_4, y_4))
        segment_4 = Segment(Point(x_4, y_4), Point(x_5, y_5))

        return [segment_1, segment_2, segment_3, segment_4]

    @staticmethod
    def _stick_together(segments: List[Segment], point: Point) -> List[Segment]:
        """

        :param segments:
        :param point:
        :return:
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

    def _calculate_single_phase(self):
        """
        Вычисление однофазной фраткальной структуры.
        :return:
        """
        self._engender_segment(self._settings["count_iter"])

        if self._count_depth == 1:
            return

        for cycle in range(self._count_depth - 1):
            segments_phase = []

            for active_segment in self._active_segments:
                angle = active_segment.get_triangle_angle()
                segments_phase.append(self._make_construction(
                    self._settings["count_iter"], self._angle, self._max_l_l, self._max_l_l / 2.0, active_segment.start, angle))

            for iteration in range(self._settings["count_iter"]):
                union_segments = []
                for segments in segments_phase:
                    union_segments += segments[iteration]
                self.lines.append(self._stick_together(union_segments, CENTER))

            # Заносим в список активных отрезков последние вычисленные отрезки
            self._active_segments = [segment for segments in segments_phase for segment in segments[-1]]

    def _calculate_several_phases(self):
        """

        :return:
        """
        self._engender_segment(self._settings["k_growth"])

        if self._count_depth == 1:
            return

        length = self._settings["count_iter_a"] * self._max_l_l
        height = self._settings["count_iter_b"] * self._max_l_l

        while len(self._active_segments) < 4**(self._count_depth + 2):
            grown_up_segments_exists = True
            exist = False
            while grown_up_segments_exists:
                grown_up_segments_exists = False
                for index, active_segment in enumerate(self._active_segments):
                    if math.isclose(active_segment.len(), self._max_l_l, abs_tol=self._max_l_l/self._settings["k_growth"]):
                        exist = True
                        grown_up_segments_exists = True
                        curr_angle = active_segment.get_triangle_angle()
                        self._active_segments[index:index + 1] = self._make_temp_construction(height, length, active_segment.start, curr_angle, self._angle)
                        break

            if exist:
                self.lines.append(deepcopy(self._stick_together(deepcopy(self._active_segments), CENTER)))

            for active_segment in self._active_segments:
                engender_segment(active_segment, self._max_l_l / self._settings["k_growth"])
            self.lines.append(deepcopy(self._stick_together(deepcopy(self._active_segments), CENTER)))

    def build(self):
        """
        Вычисление фратклаьной структуры.
        :return:
        """

        if self._settings["model"] == "single":
            self._calculate_single_phase()
        else:
            self._calculate_several_phases()
