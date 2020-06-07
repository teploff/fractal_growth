import copy
import math

from geometry.entity_2d import Segment, Point
from ontogeny.utils import engender_segment, increase_segment


class Curve:
    """

    """

    def __init__(self, max_l_l: float, max_n_iter: int):
        """

        :param max_l_l:
        :param max_n_iter:
        """

        self._max_l_l = max_l_l
        self._max_n_iter = max_n_iter
        self._active_lines = []
        self.lines = []
        self._state_cache = []

    def _engender_line(self):
        """

        :return:
        """

        segment = Segment(Point(-0.001, -0.75), Point(0.001, -0.75))
        self.lines.append([segment])

        while segment.len() < self._max_l_l:
            segment = Segment(Point(segment.start.x, segment.start.y), Point(segment.finish.x, segment.finish.y))
            # не a / 2N, a/N ведь наращиваешь лишь прямую
            engender_segment(segment, self._max_l_l / self._max_n_iter)
            self.lines.append([segment])

        self._active_lines.append(segment)

    def _make_intermediate_states_cache(self):
        """

        :return:
        """

        delta_line = self._max_l_l / (2.0 * self._max_n_iter)
        delta_triangle = math.sqrt(3) * delta_line

        for k in range(self._max_n_iter):
            delta_h = delta_triangle * (k + 1)
            delta_c = delta_h / math.sqrt(3)
            delta_l = delta_line * (k + 1)
            line_1 = Segment(
                Point(-(self._max_l_l / 2.0) - delta_c - delta_l, 0.0),
                Point(-delta_c, 0.0)
            )
            line_2 = Segment(
                Point(-delta_c, 0.0),
                Point(0.0, delta_h)
            )
            line_3 = Segment(
                Point(0.0, delta_h),
                Point(delta_c, 0.0),
            )
            line_4 = Segment(
                Point(delta_c, 0.0),
                Point(self._max_l_l / 2.0 + delta_c + delta_l, 0.0)
            )
            self._state_cache.append([line_1, line_2, line_3, line_4])

    def build(self, n_cycles: int):
        """

        :param n_cycles:
        :return:
        """

        self._engender_line()
        self._make_intermediate_states_cache()

        for _ in range(n_cycles):
            for state_segments in self._state_cache:
                temp_lines = []
                for segment in self._active_lines:
                    temp_state_segments = copy.deepcopy(state_segments)
                    angle = segment.get_triangle_angle()
                    delta_x = segment.start.x + self._max_l_l / 2.0
                    delta_y = segment.start.y
                    for i, temp_segment in enumerate(temp_state_segments):
                        temp_state_segments[i] = increase_segment(temp_segment, angle, 1.0)
                        temp_state_segments[i].move_by_coord(delta_x, delta_y)
                    temp_lines += temp_state_segments
                self.lines.append(temp_lines)
            self._active_lines = self.lines[-1]
