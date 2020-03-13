import math


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


class Line:
    """
    Класс прямая, содержащая две точки: начальная и конечная
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
        Вычисление длины прямой

        :return: Велична длины прямой
        """

        return math.sqrt((self.point_2.x - self.point_1.x) ** 2 + (self.point_2.y - self.point_1.x) ** 2)
