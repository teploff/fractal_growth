import math
from geometry.entity_2d import Point, Segment


def rotate_by_angle(segment: Segment, teta: float) -> Point:
    x = math.cos(teta * math.pi / 180.0) * segment.finish.x - math.sin(teta * math.pi / 180.0) * segment.finish.y - \
        segment.start.x * math.cos(teta * math.pi / 180.0) + segment.start.y * math.sin(teta * math.pi / 180.0) + \
        segment.start.x
    y = math.sin(teta * math.pi / 180.0) * segment.finish.x + math.cos(teta * math.pi / 180.0) * segment.finish.y - \
        segment.start.x * math.sin(teta * math.pi / 180.0) - segment.start.y * math.cos(teta * math.pi / 180.0) + \
        segment.start.y

    return Point(x, y)


if __name__ == '__main__':
    s1 = Segment(Point(-6.0, 0.0), Point(-3.0, 0.0))
    s2 = Segment(Point(-3.0, 0.0), Point(0.0, 3.0))
    s3 = Segment(Point(0.0, 3.0), Point(3.0, 0.0))
    s4 = Segment(Point(3.0, 0.0), Point(6.0, 0.0))

    new_point = rotate_by_angle(s1, 90)
    d_x = new_point.x - s1.finish.x
    d_y = new_point.y - s1.finish.y
    s1.finish = new_point
    s2.start.x += d_x
    s2.start.y += d_y
    s2.finish.x += d_x
    s2.finish.y += d_y
    s3.start.x += d_x
    s3.start.y += d_y
    s3.finish.x += d_x
    s3.finish.y += d_y
    s4.start.x += d_x
    s4.start.y += d_y
    s4.finish.x += d_x
    s4.finish.y += d_y

    new_point = rotate_by_angle(s2, 90)
    d_x = new_point.x - s2.finish.x
    d_y = new_point.y - s2.finish.y
    s2.start = s1.finish
    s2.finish = new_point
    s3.start.x += d_x
    s3.start.y += d_y
    s3.finish.x += d_x
    s3.finish.y += d_y
    s4.start.x += d_x
    s4.start.y += d_y
    s4.finish.x += d_x
    s4.finish.y += d_y

    new_point = rotate_by_angle(s3, 90)
    d_x = new_point.x - s3.finish.x
    d_y = new_point.y - s3.finish.y
    s3.start = s2.finish
    s3.finish = new_point
    s4.start.x += d_x
    s4.start.y += d_y
    s4.finish.x += d_x
    s4.finish.y += d_y

    new_point = rotate_by_angle(s4, 90)
    d_x = new_point.x - s4.finish.x
    d_y = new_point.y - s4.finish.y
    s4.start = s3.finish
    s4.finish = new_point

    print(s1.start, s1.finish)
    print(s2.start, s2.finish)
    print(s3.start, s3.finish)
    print(s4.start, s4.finish)
