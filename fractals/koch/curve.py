from copy import deepcopy
from shapely.geometry import Polygon
import math

from fractals.koch.const import ACCURACY, CENTER
from ontogeny.utils import increase_segment_length
from fractals.koch.utils import calc_base_struct, cal_regular_frame, stick_segments
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
                    segments_phase += calc_base_struct(height, length, active_segment.start, angle, self._angle)
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
        self.lines = calc_segment_phases(CENTER, self._settings["count_iterations"], self._max_l_l)
        self._active_segments = deepcopy(self.lines[-1])

        if self._count_depth == 1:
            return

        length = self._settings["coefficient_a"] * self._max_l_l
        height = self._settings["coefficient_h"] * self._max_l_l

        while len(self._active_segments) < 4 ** (self._count_depth + 2):
            grown_up_segments_exists = True
            exist = False
            while grown_up_segments_exists:
                grown_up_segments_exists = False
                for index, active_segment in enumerate(self._active_segments):
                    if math.isclose(active_segment.len(), self._max_l_l, abs_tol=ACCURACY):
                        exist = True
                        grown_up_segments_exists = True
                        curr_angle = active_segment.get_triangle_angle()
                        self._active_segments[index:index + 1] = calc_base_struct(height, length, active_segment.start,
                                                                                  curr_angle, self._angle)
                        break

            if exist:
                self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))

            for active_segment in self._active_segments:
                increase_segment_length(active_segment, self._max_l_l / self._settings["count_iterations"])
            self.lines.append(deepcopy(stick_segments(deepcopy(self._active_segments), CENTER)))

    def _calculate_irregular_phases(self) -> None:
        """

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

        while possible:
            grown_up_segments_exists = True
            exist = False
            while grown_up_segments_exists:
                grown_up_segments_exists = False
                for index, active_segment in enumerate(self._active_segments):
                    if math.isclose(active_segment.len(), self._max_l_l, abs_tol=ACCURACY) and active_segment.possible:
                        if active_segment.depth == self._count_depth:
                            active_segment.possible = False
                        else:
                            exist = True
                            grown_up_segments_exists = True
                            curr_angle = active_segment.get_triangle_angle()
                            segments = calc_base_struct(height, length, active_segment.start, curr_angle, self._angle)
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
        elif self._settings["model"] == "irregular":
            self._calculate_irregular_phases()
        elif self._settings["model"] == "regular_polygon":
            self._calculate_regular_polygon()
        else:
            raise ValueError("Unknown model")
