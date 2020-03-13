import numpy
from typing import List

from geometry.entity_2d import Line, Point


ABSCISSA = 'x'
ORDINATE = 'y'


def engender_plant_buds(branch: Line, count_buds: int) -> List[Point]:
    """

    :param branch:
    :param count_buds:
    :return:
    """

    # Находим величины дельт по x и y для того, чтобы понимать на каких именно координатах производить random.
    # Ведь может быть случай, что прямая перпендикулярна Оу или Оx. В первом случае необходимо прозводить random по
    # координатам x, иначе по координатам y
    d_x = abs(branch.point_1.x - branch.point_2.x)
    d_y = abs(branch.point_1.y - branch.point_2.y)

    if d_x > d_y:
        selected_axis = ABSCISSA
        buds = numpy.random.uniform(branch.point_1.x, branch.point_2.x, size=(1, count_buds))
    else:
        selected_axis = ORDINATE
        buds = numpy.random.uniform(branch.point_1.y, branch.point_2.y, size=(1, count_buds))

    # Если вырожденный случай, отрезок перпендикулярен оX
    if d_x == 0:
        return [Point(branch.point_1.x, y) for y in buds[0]]

    if selected_axis == ABSCISSA:
        return [Point(x, ((branch.point_1.y - branch.point_2.y)/(branch.point_1.x - branch.point_2.x))*(x - branch.point_1.x) + branch.point_1.y) for x in buds[0]]
    else:
        return [Point(((branch.point_1.x - branch.point_2.x)/(branch.point_1.y - branch.point_2.y))*(y - branch.point_1.y) + branch.point_1.x, y) for y in buds[0]]
