import math
import numpy
from typing import Union

ABSCISSA = 'x'
ORDINATE = 'y'
DELTA = 0.001


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

        self.start = start
        self.finish = finish

    def length(self) -> float:
        """
        Вычисление длины отрезка

        :return: Велична длины отрезка
        """

        return math.sqrt((self.finish.x - self.start.x) ** 2 + (self.finish.y - self.start.y) ** 2)

    def find_point(self, value: float, axis: Union[ABSCISSA, ORDINATE]) -> Point:
        """
        Нахождение второй координаты точки, заданной одной координатой, на отрезке
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
        if math.isclose(self.start.x, self.finish.x, abs_tol=DELTA):
            if self.start.y > self.finish.y:
                return 270.0
            else:
                return 90.0

        # Если отрезок расположен перпендикулярно ординате
        if math.isclose(self.start.y, self.finish.y, abs_tol=DELTA):
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
