from geometry.entity_2d import Point, Segment
from ontogeny.entity_2d import Branch, PlantTree
from ontogeny.utils import engender_branch, engender_random_buds


def get_two_level_tree() -> PlantTree:
    """

    :return:
    """

    p1 = Point(0, -1)
    p2 = engender_branch(p1, 0.5, 90)
    l1 = Segment(p1, p2)
    root = Branch(l1)
    tree = PlantTree(root)
    p3, p4 = engender_random_buds(l1, 2)
    p5 = engender_branch(p3, 0.4, 45)
    p6 = engender_branch(p4, 0.4, 135)
    l2 = Segment(p3, p5)
    l3 = Segment(p4, p6)
    node1 = Branch(l2, parent=root)
    node2 = Branch(l3, parent=root)

    return tree


def get_three_level_tree() -> PlantTree:
    p1 = Point(0, -1)
    p2 = engender_branch(p1, 0.5, 90)
    l1 = Segment(p1, p2)
    print("Angle = ", l1.get_triangle_angle())
    root = Branch(l1)
    tree = PlantTree(root)
    p3, p4 = engender_random_buds(l1, 2)
    p5 = engender_branch(p3, 0.4, 45)
    p6 = engender_branch(p4, 0.4, 135)
    l2 = Segment(p3, p5)
    print("Angle 2 = ", l2.get_triangle_angle())
    l3 = Segment(p4, p6)
    print("Angle 3 = ", l3.get_triangle_angle())
    node1 = Branch(l2, parent=root)
    node2 = Branch(l3, parent=root)
    p7, p8 = engender_random_buds(Segment(p3, p5), 2)
    p9 = engender_branch(p7, 0.3, 67.5)
    p10 = engender_branch(p8, 0.2, 22.5)
    l4 = Segment(p7, p9)
    l5 = Segment(p8, p10)
    node3 = Branch(l4, parent=node1)
    node4 = Branch(l5, parent=node1)
    p11, p12 = engender_random_buds(Segment(p4, p6), 2)
    p13 = engender_branch(p11, 0.4, 157.5)
    p14 = engender_branch(p12, 0.4, 112.5)
    l6 = Segment(p12, p14)
    l7 = Segment(p11, p13)
    node5 = Branch(l6, parent=node2)
    node6 = Branch(l7, parent=node2)

    return tree
