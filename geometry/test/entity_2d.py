
import unittest
from geometry.entity_2d import Point, Segment


class TestPointOrderingInSegment(unittest.TestCase):

    def test_positive_coefficient_of_the_line(self):
        first_point = Point(-1.0, -1.0)
        second_point = Point(1.0, 1.0)
        segment = Segment(first_point, second_point)
        self.assertEqual(segment.start, first_point)
        self.assertEqual(segment.finish, second_point)

        segment = Segment(second_point, first_point)
        self.assertEqual(segment.start, first_point)
        self.assertEqual(segment.finish, second_point)

    def test_negative_coefficient_of_the_line(self):
        first_point = Point(-1.0, 1.0)
        second_point = Point(1.0, -1.0)
        segment = Segment(first_point, second_point)
        self.assertEqual(segment.start, second_point)
        self.assertEqual(segment.finish, first_point)

        segment = Segment(second_point, first_point)
        self.assertEqual(segment.start, second_point)
        self.assertEqual(segment.finish, first_point)

    def test_zero_coefficient_of_the_line(self):
        first_point = Point(-1.0, 0.0)
        second_point = Point(1.0, 0.0)
        segment = Segment(first_point, second_point)
        self.assertEqual(segment.start, first_point)
        self.assertEqual(segment.finish, second_point)

        segment = Segment(second_point, first_point)
        self.assertEqual(segment.start, first_point)
        self.assertEqual(segment.finish, second_point)

    def test_null_coefficient_of_the_line(self):
        first_point = Point(0.0, -1.0)
        second_point = Point(0.0, 1.0)
        segment = Segment(first_point, second_point)
        self.assertEqual(segment.start, first_point)
        self.assertEqual(segment.finish, second_point)

        segment = Segment(second_point, first_point)
        self.assertEqual(segment.start, first_point)
        self.assertEqual(segment.finish, second_point)


if __name__ == '__main__':
    unittest.main()
