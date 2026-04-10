from copy import deepcopy
from shapely.geometry import Polygon
import math

from fractals.koch.const import ACCURACY, CENTER
from ontogeny.utils import increase_segment_length
from fractals.koch.utils import calc_base_struct, cal_regular_frame, stick_segments, calc_base_base_struct, calc_new_base_struct
from fractals.koch.growth import calc_segment_phases


class Curve:
    """
    Класс построения фрактальных структур на основе метода "Кривая Коха." Подробнее тут:
    https://en.wikipedia.org/wiki/Koch_snowflake
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

    def _calc_fractal_phases(self):
        """
        Вычисление фаз фрактальной структуры.
        :return:
        """
        start_length = self._max_l_l / 2.0
        for _ in range(self._count_depth - 1):
            length = start_length
            delta_length = (self._max_l_l - start_length) / self._settings["count_iterations"]
            for iteration in range(self._settings["count_iterations"]):
                segments_phase = []
                length += delta_length

                for active_segment in self._active_segments:
                    angle = active_segment.get_triangle_angle()
                    height = ((iteration + 1) / self._settings["count_iterations"]) * self._max_l_l * math.sin(self._angle * math.pi / 180.0)
                    segments_phase += calc_base_base_struct(height, length, active_segment.start, angle, self._angle)
                lines = stick_segments(segments_phase, CENTER)

                # TODO: thinking about sticking
                points = []
                for line in lines:
                    points.append([line.start.x, line.start.y])
                    points.append([line.finish.x, line.finish.y])
                p = Polygon(points)
                center = p.centroid
                d_x = CENTER.x - center.x
                d_y = CENTER.y - center.y
                for line in lines:
                    line.start.x += d_x
                    line.start.y += d_y
                    line.finish.x += d_x
                    line.finish.y += d_y

                self.lines.append(lines)

            self._active_segments = self.lines[-1]

    def _calculate_single_phase(self) -> None:
        """
        Вычисление однофазной фраткальной структуры.
        :return:
        """

        self.lines = calc_segment_phases(CENTER, self._settings["count_iterations"], self._max_l_l)
        self._active_segments = deepcopy(self.lines[-1])

        if self._count_depth == 1:
            return

        self._calc_fractal_phases()

    def _calculate_several_phases(self) -> None:
        """
        Вычисление многофазной фраткальной структуры.
        :return:
        """
        beginner_number = 1

        beginner_will_char_grow = True
        if 'count_beginner_from' in self._settings and self._settings['count_beginner_from'] and self._settings['count_beginner_to'] and not (self._settings['count_beginner_from'] <= beginner_number <= self._settings['count_beginner_to']):
            beginner_will_char_grow = False

        self.lines = calc_segment_phases(CENTER, self._settings["count_iterations"], self._max_l_l, beginner_will_char_grow=beginner_will_char_grow, **self._settings)
        self._active_segments = deepcopy(self.lines[-1])

        for segment in self._active_segments:
            segment.depth = 1
            segment.possible = True

        possible = True

        if self._count_depth == 1:
            return

        length = self._settings["coefficient_a"] * self._max_l_l
        height = self._settings["coefficient_h"] * self._max_l_l

        import numpy as np
        # zz = 8 * self._max_l_l
        zz = 0.25 * self._max_l_l
        # self._settings['pattern'] = {depth: max_l for depth, max_l in enumerate([a for a in np.arange(zz, self._max_l_l, -(zz - self._max_l_l)/self._count_depth)])}
        self._settings['pattern'] = {depth: max_l for depth, max_l in enumerate([a for a in np.arange(zz, 2 * self._max_l_l, (2 * self._max_l_l-zz)/self._count_depth)])}

        while possible:
            for active_segment in self._active_segments:
                active_segment.newbie = False

            grown_up_segments_exists = True
            exist = False
            while grown_up_segments_exists:
                grown_up_segments_exists = False
                for index, active_segment in enumerate(self._active_segments):
                    # import random
                    # a = random.randrange(10) * 0.001
                    # if random.randrange(10) < 5:
                    #     a *= -1
                    # print(a)
                    if active_segment.cur_iter == active_segment.max_iter and active_segment.possible:
                        if active_segment.depth == self._count_depth:
                            active_segment.possible = False
                        else:
                            beginner_number += 1
                            beginner_will_char_grow = True
                            if 'count_beginner_from' in self._settings and self._settings['count_beginner_from'] and self._settings['count_beginner_to'] and not (self._settings['count_beginner_from'] <= beginner_number <= self._settings['count_beginner_to']):
                                beginner_will_char_grow = False

                            exist = True
                            grown_up_segments_exists = True
                            curr_angle = active_segment.get_triangle_angle()

                            #TODO: Эксперимент с pattern
                            if self._settings.get('pattern'):
                                length = self._settings["coefficient_a"] * active_segment.max_length

                            segments = calc_base_struct(height, length, active_segment.start, curr_angle, self._angle, prev_segment = active_segment,
                                                        beginner_will_char_grow=beginner_will_char_grow, **self._settings)
                            for s in segments:
                                s.newbie = True

                            next_depth = active_segment.depth + 1
                            for segment in segments:
                                segment.depth = next_depth
                                segment.possible = True

                            self._active_segments[index:index + 1] = segments
                            break

            # if exist:
            #     self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))

            for active_segment in self._active_segments:
                if active_segment.possible and not active_segment.newbie:
                    increase_segment_length(active_segment, active_segment.dt_length, characteristic_exist=True)
            possible = any(active_segment.possible for active_segment in self._active_segments)
            self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))

        pass
    def _new_calculate_stochastic(self) -> None:
        beginner_number = 1

        beginner_will_char_grow = True
        if 'count_beginner_from' in self._settings and self._settings['count_beginner_from'] and self._settings['count_beginner_to'] and not (self._settings['count_beginner_from'] <= beginner_number <= self._settings['count_beginner_to']):
            beginner_will_char_grow = False

        self.lines = calc_segment_phases(CENTER, self._settings["count_iterations"], self._max_l_l, beginner_will_char_grow=beginner_will_char_grow, **self._settings)
        self._active_segments = deepcopy(self.lines[-1])

        for segment in self._active_segments:
            segment.depth = 1
            segment.possible = True

        possible = True

        if self._count_depth == 1:
            return

        # length = self._settings["coefficient_a"] * self._max_l_l
        # height = self._settings["coefficient_h"] * self._max_l_l

        length = 0.5 * self._max_l_l
        height = 0.01 * self._max_l_l

        while possible:
            grown_up_segments_exists = True
            exist = False
            while grown_up_segments_exists:
                grown_up_segments_exists = False
                for index, active_segment in enumerate(self._active_segments):

                    # import random
                    # a = random.randrange(10) * 0.001
                    # if random.randrange(10) < 5:
                    #     a *= -1

                    if active_segment.cur_iter == active_segment.max_iter and active_segment.possible:
                        if active_segment.depth == self._count_depth:
                            active_segment.possible = False
                        else:
                            beginner_number += 1
                            beginner_will_char_grow = True
                            if 'count_beginner_from' in self._settings and self._settings['count_beginner_from'] and self._settings['count_beginner_to'] and not (self._settings['count_beginner_from'] <= beginner_number <= self._settings['count_beginner_to']):
                                beginner_will_char_grow = False

                            exist = True
                            grown_up_segments_exists = True
                            curr_angle = active_segment.get_triangle_angle()
                            segments = calc_base_struct(height, length, active_segment.start, curr_angle, self._angle, prev_segment = active_segment,
                                                        beginner_will_char_grow=beginner_will_char_grow, **self._settings)
                            next_depth = active_segment.depth + 1
                            for segment in segments:
                                segment.depth = next_depth
                                segment.possible = True

                            self._active_segments[index:index + 1] = segments
                            break

            if exist:
                self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))

            for active_segment in self._active_segments:
                if active_segment.possible:
                    increase_segment_length(active_segment, active_segment.dt_length, characteristic_exist=True)
            possible = any(active_segment.possible for active_segment in self._active_segments)
            self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))

    def _calculate_metamorphosis(self) -> None:
        """
        Вычисление метаморфозы фрактальной структуры.
        :return:
        """
        # TODO: порефачить?
        # TODO: begin
        beginner_number = 1

        beginner_will_char_grow = True
        if 'count_beginner_from' in self._settings and self._settings['count_beginner_from'] and self._settings[
            'count_beginner_to'] and not (
                self._settings['count_beginner_from'] <= beginner_number <= self._settings['count_beginner_to']):
            beginner_will_char_grow = False
        # TODO: end

        self.lines = calc_segment_phases(CENTER, self._settings["count_iterations"], self._max_l_l,
                                         beginner_will_char_grow=beginner_will_char_grow, **self._settings)
        self._active_segments = deepcopy(self.lines[-1])

        for segment in self._active_segments:
            segment.depth = 0
            segment.possible = True

        possible = True

        if self._count_depth == 0:
            return

        # depth -> dict(max_val, iterations, left and right angles)
        self._settings['metamorphosis'] = {
            1: {
                'max_length': 0.08,
                'left_angle': 30.0,
                'right_angle': 110.0,
            },
            2: {
                'max_length': 0.08 * 0.75,
                'left_angle': 60.0,
                'right_angle': 60.0,
            },
            3: {
                'max_length': 0.08 * 0.6,
                'left_angle': 110.0,
                'right_angle': 30.0,
            },
            4: {
                'max_length': 0.08 * 0.5,
                'left_angle': 80.0,
                'right_angle': 80.0,
            },
        }

        if self._settings['metamorphosis'].get(self._count_depth, None) is None:
            raise 'not enough configuration for metamorphosis dict settings'

        while possible:
            grown_up_segments_exists = True
            exist = False
            while grown_up_segments_exists:
                grown_up_segments_exists = False
                for index, active_segment in enumerate(self._active_segments):
                    if active_segment.cur_iter == active_segment.max_iter and active_segment.possible:
                        if active_segment.depth == self._count_depth:
                            active_segment.possible = False
                        else:
                            beginner_number += 1
                            beginner_will_char_grow = True
                            if 'count_beginner_from' in self._settings and self._settings['count_beginner_from'] and \
                                    self._settings['count_beginner_to'] and not (
                                    self._settings['count_beginner_from'] <= beginner_number <= self._settings[
                                'count_beginner_to']):
                                beginner_will_char_grow = False

                            exist = True
                            grown_up_segments_exists = True
                            curr_angle = active_segment.get_triangle_angle()

                            length = self._settings["coefficient_a"] * active_segment.max_length
                            height = self._settings["coefficient_h"] * active_segment.max_length

                            segments = calc_new_base_struct(height, length, active_segment.start, curr_angle, self._angle,
                                                        prev_segment=active_segment,
                                                        beginner_will_char_grow=beginner_will_char_grow,
                                                        **self._settings)
                            next_depth = active_segment.depth + 1
                            for segment in segments:
                                segment.depth = next_depth
                                segment.possible = True

                            self._active_segments[index:index + 1] = segments
                            break

            if exist:
                self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))

            for active_segment in self._active_segments:
                if active_segment.possible:
                    increase_segment_length(active_segment, active_segment.dt_length)
            possible = any(active_segment.possible for active_segment in self._active_segments)
            self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))
        pass
    def _calculate_stochastic(self) -> None:
        """
        Вычисление многофазной фраткальной структуры.
        :return:
        """
        self.lines = calc_segment_phases(CENTER, self._settings["count_iterations"], self._max_l_l)
        self._active_segments = deepcopy(self.lines[-1])

        for segment in self._active_segments:
            segment.depth = 1
            segment.possible = True

        possible = True

        if self._count_depth == 1:
            return

        length = self._settings["coefficient_a"] * self._max_l_l
        height = self._settings["coefficient_h"] * self._max_l_l

        accuracy = float(self._max_l_l) / float(self._settings["count_iterations"])

        max_l_segments = {self._active_segments[0].id: self._max_l_l}

        while possible:
            grown_up_segments_exists = True
            exist = False
            while grown_up_segments_exists:
                grown_up_segments_exists = False
                for index, active_segment in enumerate(self._active_segments):

                    import random
                    a = random.randrange(10) * 0.001
                    if random.randrange(10) < 5:
                        a *= -1

                    if active_segment.len() >= max_l_segments[active_segment.id] and active_segment.possible:
                        if active_segment.depth == self._count_depth:
                            active_segment.possible = False
                        else:
                            exist = True
                            grown_up_segments_exists = True
                            curr_angle = active_segment.get_triangle_angle()
                            segments = calc_base_base_struct(height, length, active_segment.start, curr_angle, self._angle)
                            next_depth = active_segment.depth + 1
                            for segment in segments:
                                segment.depth = next_depth
                                segment.possible = True

                            self._active_segments[index:index + 1] = segments
                            for s in segments:
                                max_l_segments[s.id] = length + a
                            break

            if exist:
                self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))

            for active_segment in self._active_segments:
                if active_segment.possible:
                    increase_segment_length(active_segment, self._max_l_l / self._settings["count_iterations"])
            possible = any(active_segment.possible for active_segment in self._active_segments)
            self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))

    def _calculate_regular_polygon(self) -> None:
        """
        Вычисление однофазной фрактальной структуры на основе правильной фигуры.
        :return:
        """
        delta_length = self._max_l_l / self._settings["count_iterations"]
        length = delta_length
        for i in range(self._settings["count_iterations"]):
            length += delta_length
            self.lines.append(cal_regular_frame(CENTER, self._settings["count_angles"], length))

        if self._settings["building_way"] == "inside":
            self._active_segments = self.lines[-1]
        else:
            self._active_segments = self.lines[-1][::-1]

        if self._count_depth == 1:
            return

        self._calc_fractal_phases()

    def build(self):
        """
        Вычисление фратклаьной структуры.
        :return:
        """
        if self._settings["model"] == "single":
            self._calculate_single_phase()
        elif self._settings["model"] == "several":
            self._calculate_several_phases()
        elif self._settings["model"] == "stochastic":
            self._new_calculate_stochastic()
        elif self._settings["model"] == 'metamorphosis':
            self._calculate_metamorphosis()
        elif self._settings["model"] == "regular_polygon":
            self._calculate_regular_polygon()
        else:
            raise ValueError("Unknown model")
