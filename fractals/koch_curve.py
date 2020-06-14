import copy
import math
from typing import List

from geometry.entity_2d import Segment, Point
from ontogeny.utils import engender_segment, increase_segment
from geometry.utils import rotate_by_angle

CENTER = Point(0.0, 0.0)
BETA = 45.0


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
        self._active_segments = []
        self.lines = []

        self._engender_segment()

    def _engender_segment(self):
        """

        :return:
        """

        segment = Segment(Point(CENTER.x - 0.001, CENTER.y), Point(CENTER.x + 0.001, CENTER.y))
        self.lines.append([segment])

        while segment.len() < self._max_l_l:
            segment = Segment(Point(segment.start.x, segment.start.y), Point(segment.finish.x, segment.finish.y))
            # не a / 2N, a/N ведь наращиваешь лишь прямую
            engender_segment(segment, self._max_l_l / self._max_n_iter)
            self.lines.append([segment])

        self._active_segments.append(segment)

    def _make_construction(self, point: Point, angle: float) -> List[Segment]:
        """

        :return:
        """
        
        segments = []
        
        length = self._max_l_l / 2.0
        for iteration in range(self._max_n_iter):
            height = ((iteration + 1) / self._max_n_iter) * self._max_l_l * math.sin(BETA * math.pi / 180.0)
            length += (self._max_l_l / 2.0) / self._max_n_iter

            x_2 = point.x + length * math.cos(angle * math.pi / 180.0)
            y_2 = point.y + length * math.sin(angle * math.pi / 180.0)

            x_3 = x_2 + (height * math.cos((angle + BETA) * math.pi / 180.0)) / math.sin(BETA * math.pi / 180.0)
            y_3 = y_2 + (height * math.sin((angle + BETA) * math.pi / 180.0)) / math.sin(BETA * math.pi / 180.0)

            x_4 = x_3 + (height * math.cos((BETA - angle) * math.pi / 180.0)) / math.sin(BETA * math.pi / 180.0)
            y_4 = y_3 - (height * math.sin((BETA - angle) * math.pi / 180.0)) / math.sin(BETA * math.pi / 180.0)

            x_5 = x_4 + length * math.cos(angle * math.pi / 180.0)
            y_5 = y_4 + length * math.sin(angle * math.pi / 180.0)

            segment_1 = Segment(Point(point.x, point.y), Point(x_2, y_2))
            segment_2 = Segment(Point(x_2, y_2), Point(x_3, y_3))
            segment_3 = Segment(Point(x_3, y_3), Point(x_4, y_4))
            segment_4 = Segment(Point(x_4, y_4), Point(x_5, y_5))

            segments.append([segment_1, segment_2, segment_3, segment_4])
        
        return segments

    def _make_increment(self, segments: List[Segment], d_x: float, d_y: float):
        """

        :param d_x:
        :param d_y:
        :return:
        """

        for segment in segments:
            segment.start.x += d_x
            segment.start.y += d_y
            segment.finish.x += d_x
            segment.finish.y += d_y

    def _rotate_construction(self, segments: List[Segment], angle: float):
        """

        :return:
        """

        x2 = segments[0].start.x + segments[0].len()
        y2 = segments[0].start.y

    def build(self, n_cycles: int):
        """

        :param n_cycles:
        :return:
        """
        for _ in range(n_cycles - 1):
            union_segments = []
            for active_segment in self._active_segments:
                union_segments.append(self._make_construction(active_segment.start, active_segment.get_triangle_angle()))

            for depth in range(len(union_segments[0])):
                depth_segments = [segment[depth] for segment in union_segments]

                for segments in depth_segments:
                    dx = CENTER.x - segments[len(segments)//2 - 1].finish.x
                    dy = CENTER.y - segments[len(segments)//2 - 1].finish.y
                    segments[len(segments)//2 - 1].start.x += dx
                    segments[len(segments)//2 - 1].start.y += dy
                    segments[len(segments)//2 - 1].finish.x += dx
                    segments[len(segments)//2 - 1].finish.y += dy
                    reference_point = segments[len(segments)//2 - 1].start
                    left_side = segments[:len(segments) // 2 - 1]
                    for line in left_side[::-1]:
                        dx = reference_point.x - line.finish.x
                        dy = reference_point.y - line.finish.y
                        line.start.x += dx
                        line.start.y += dy
                        line.finish.x += dx
                        line.finish.y += dy
                        reference_point = line.start

                    dx = CENTER.x - segments[len(segments) // 2].start.x
                    dy = CENTER.y - segments[len(segments) // 2].start.y
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

                    self.lines += depth_segments
