import math
import numpy
from typing import Union
from geometry.constants import ABSCISSA, ORDINATE, ACCURACY


class Point:
    """
    Класс точка, содержащая две координаты x и y
    """

    def __init__(self, x: float, y: float):
        """
        :param x: Координата x
        :param y: Координата y
        """

        self.x = x
        self.y = y

    def __repr__(self):
        return f'Point({self.x:.5f}, {self.y:.5f})'


class Segment:
    """
    Класс отрезок, содержащая две точки: начальная и конечная
    """

    def __init__(self, start: Point, finish: Point):
        """
        :param start: Начальная точка
        :param finish: Конечная точка
        """

        self.start, self.finish = self._make_order_points(start, finish)

    @staticmethod
    def _make_order_points(p1: Point, p2: Point) -> (Point, Point):
        """

        :param p1:
        :param p2:
        :return:
        """

        if p1.y < p2.y:
            return p1, p2
        elif math.isclose(p1.y, p2.y, abs_tol=ACCURACY):
            if p1.x < p2.x:
                return p1, p2
            else:
                return p2, p1
        else:
            return p2, p1

    def len(self) -> float:
        """
        Вычисление длины отрезка

        :return: Велична длины отрезка
        """

        return math.sqrt((self.finish.x - self.start.x) ** 2 + (self.finish.y - self.start.y) ** 2)

    def does_point_belong(self, point: Point) -> bool:
        """
        Принадлежит ли указанная точка point отрезку?

        :param point: Указанная точка
        :return: Признак принадлежности точки. Принадлежит - True, не принадлежит - False
        """

        cross_product = (point.y - self.start.y) * (self.finish.x - self.start.x) - \
                        (point.x - self.start.x) * (self.finish.y - self.start.y)

        # compare versus epsilon for floating point values, or != 0 if using integers
        if abs(cross_product) > ACCURACY:
            return False

        dot_product = (point.x - self.start.x) * (self.finish.x - self.start.x) + \
                      (point.y - self.start.y) * (self.finish.y - self.start.y)
        if dot_product < 0:
            return False

        squared_length_ba = (self.finish.x - self.start.x) * (self.finish.x - self.start.x) + \
                          (self.finish.y - self.start.y) * (self.finish.y - self.start.y)
        if dot_product > squared_length_ba:
            return False

        return True

    def find_point_with_one_coord(self, value: float, axis: Union[ABSCISSA, ORDINATE]) -> Point:
        """
        Нахождение второй координаты точки, заданной одной координатой и лежащей на отрезке

        :param value: Значение координаты точки
        :param axis: Ось, на которой задано значение координаты точки. Абсцисса или ордината
        :return: Точка с координатами x и y
        """

        # Принадлежит ли значение value отрезку в диапазоне множества координат x
        if axis == ABSCISSA:
            if not min(self.start.x, self.finish.x) <= value <= max(self.start.x, self.finish.x):
                raise ValueError('The value does not belong to x coordinate range')
        # Принадлежит ли значение value отрезку в диапазоне множества координат y
        else:
            if not min(self.start.y, self.finish.y) <= value <= max(self.start.y, self.finish.y):
                raise ValueError('The value does not belong to y coordinate range')

        # Если вырожденный случай, отрезок перпендикулярен Ох
        if abs(self.start.x - self.finish.x) == 0:
            if axis == ABSCISSA:
                raise ValueError('The line is perpendicular to the x axis')
            return Point(self.start.x, value)

        # Уровнение прямой имеет вид: y = kx + b.
        # Уровнение прямой через две заданные точки имеет вид:  y - y1 = k * (x - x1), где
        # k = (y1 - y2) / (x1 - x2)

        k = (self.start.y - self.finish.y) / (self.start.x - self.finish.x)

        if axis == ABSCISSA:
            x = value
            y = k * (x - self.start.x) + self.start.y
        else:
            y = value
            x = (y - self.start.y) / k + self.start.x

        return Point(x, y)

    def get_triangle_angle(self) -> float:
        """
        Вычислить угол поворота или меру поворота подвижного радиус-вектора относительно его начального положения.
        Подробнее тут: http://twt.mpei.ac.ru/math/TRIG/TR_010100.html
        :return: Положительное значение угла поворота
        """

        # Если отрезок расположен перпендикулярно абсциссе
        if math.isclose(self.start.x, self.finish.x, abs_tol=ACCURACY):
            if self.start.y > self.finish.y:
                return 270.0
            else:
                return 90.0

        # Если отрезок расположен перпендикулярно ординате
        if math.isclose(self.start.y, self.finish.y, abs_tol=ACCURACY):
            if self.start.x > self.finish.x:
                return 180.0
            else:
                return 0.0

        # https://www.mathopenref.com/coordslope.html
        m = (self.finish.y - self.start.y) / (self.finish.x - self.start.x)
        angle = numpy.rad2deg(math.atan(m))

        # Значение arctan может быть положительно в 1 и 3 червертях и отрицательно в 2 и 4 соответственно.
        # Поэтому необходимо сделать некоторые преобразования.
        # 2 или 4 четверть
        if angle < 0:
            if self.finish.y > self.start.y:
                angle += 180.0
            else:
                angle += 360.0
        # 1 или 3 четверть
        else:
            if self.finish.y > self.start.y:
                pass
            else:
                angle += 180.0

        return angle
