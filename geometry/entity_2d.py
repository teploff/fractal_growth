import math
from typing import Union

ABSCISSA = 'x'
ORDINATE = 'y'


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


class Segment:
    """
    Класс отрезок, содержащая две точки: начальная и конечная
    """
    def __init__(self, point_1: Point, point_2: Point):
        """
        :param point_1: Начальная точка
        :param point_2: Конечная точка
        """

        self.point_1 = point_1
        self.point_2 = point_2

    def length(self) -> float:
        """
        Вычисление длины отрезка

        :return: Велична длины отрезка
        """

        return math.sqrt((self.point_2.x - self.point_1.x) ** 2 + (self.point_2.y - self.point_1.x) ** 2)

    def find_point(self, value: float, axis: Union[ABSCISSA, ORDINATE]) -> Point:
        """
        Нахождение второй координаты точки, заданной одной координатой, на отрезке
        :param value: Значение координаты точки
        :param axis: Ось, на которой задано значение координаты точки. Абсцисса или ордината
        :return: Точка с координатами x и y
        """

        # Принадлежит ли значение value отрезку в диапазоне множества координат x
        if axis == ABSCISSA:
            if not min(self.point_1.x, self.point_2.x) <= value <= max(self.point_1.x, self.point_2.x):
                raise ValueError('The value does not belong to x coordinate range')
        # Принадлежит ли значение value отрезку в диапазоне множества координат y
        else:
            if not min(self.point_1.y, self.point_2.y) <= value <= max(self.point_1.y, self.point_2.y):
                raise ValueError('The value does not belong to y coordinate range')

        # Если вырожденный случай, отрезок перпендикулярен Ох
        if abs(self.point_1.x - self.point_2.x) == 0:
            if axis == ABSCISSA:
                raise ValueError('The line is perpendicular to the x axis')
            return Point(self.point_1.x, value)

        # Уровнение прямой имеет вид: y = kx + b.
        # Уровнение прямой через две заданные точки имеет вид:  y - y1 = k * (x - x1), где
        # k = (y1 - y2) / (x1 - x2)

        k = (self.point_1.y - self.point_2.y) / (self.point_1.x - self.point_2.x)

        if axis == ABSCISSA:
            x = value
            y = k * (x - self.point_1.x) + self.point_1.y
        else:
            y = value
            x = (y - self.point_1.y) / k + self.point_1.x

        return Point(x, y)
