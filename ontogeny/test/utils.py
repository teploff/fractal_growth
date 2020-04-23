
import unittest
import math
from geometry.entity_2d import Point, Segment
from ontogeny.utils import engender_segment


class TestEngenderSegment(unittest.TestCase):

    def test_positive_coefficient_of_the_line(self):
        segment = Segment(Point(-1.0, -1.0), Point(1.0, 1.0))
        engender_segment(segment, 2.0 * math.sqrt(2))
        self.assertTrue(math.isclose(segment.start.x, -2.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.start.y, -2.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.finish.x, 2.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.finish.y, 2.0, abs_tol=0.0001))

    def test_negative_coefficient_of_the_line(self):
        segment = Segment(Point(1.0, -1.0), Point(-1.0, 1.0))
        engender_segment(segment, 2.0 * math.sqrt(2))
        self.assertTrue(math.isclose(segment.start.x, 2.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.start.y, -2.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.finish.x, -2.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.finish.y, 2.0, abs_tol=0.0001))

    def test_zero_coefficient_of_the_line(self):
        segment = Segment(Point(-1.0, 0.0), Point(1.0, 0.0))
        engender_segment(segment, 2.0)
        self.assertTrue(math.isclose(segment.start.x, -2.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.start.y, 0.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.finish.x, 2.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.finish.y, 0.0, abs_tol=0.0001))

    def test_null_coefficient_of_the_line(self):
        segment = Segment(Point(0.0, -1.0), Point(0.0, 1.0))
        engender_segment(segment, 2.0)
        self.assertTrue(math.isclose(segment.start.x, 0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.start.y, -2.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.finish.x, 0.0, abs_tol=0.0001))
        self.assertTrue(math.isclose(segment.finish.y, 2.0, abs_tol=0.0001))


if __name__ == '__main__':
    unittest.main()