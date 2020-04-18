from anytree import NodeMixin, PreOrderIter
from anytree.search import findall, find
from typing import List, Tuple

from geometry.entity_2d import Segment


class Branch(Segment, NodeMixin):
    """
    Ветка или узел древа, предтавляющий из себя атомарный объект структуры. Каждая ветка представляет из себя отрезок
    (Segment), который характерезуется начальной или конечной точками, также у каждой из ветчки есть потомки (children)
    и родитель (parent)
    """
    def __init__(self, segment: Segment, parent: Segment = None, children: List[Segment] = None):
        super(Segment, self).__init__()
        self.segment = segment
        self.parent = parent
        if children:
            self.children = children

    def __repr__(self):
        return f"Line: {self.segment.start}, {self.segment.finish}"


class PlantTree:
    """
    Древо, представляющее собой совокупность веток или узлов древа Branch.
    """

    def __init__(self, root: Branch):
        self.root = root

    def __len__(self):
        """
        Количество узлов у древа

        :return: Количество узлов (Nodes)
        """

        return len(findall(self.root))

    def get_branch_by_index(self, index: int) -> Branch:
        """
        Получить узел древа (ветку) с указанным индексом

        :param index: Индекс узла древа (ветки)
        :return: Узел древа (ветка)
        """

        branches = findall(self.root)
        for i, branch in enumerate(branches):
            if i == index:
                return branch

        raise IndexError('Specified index is out of range')

    def get_indexes_by_branches(self, branches: List[Branch] or Tuple[Branch]) -> List[int]:
        """

        :param branches:
        :return:
        """

        br = findall(self.root)
        res = []
        for i, b in enumerate(br):
            for bb in branches:
                if bb == b:
                    res.append(i)

        return res

    def get_branches_by_height(self, height) -> Tuple[Branch]:
        """
        Получить узлы древа (ветки) с указанной высотой древа

        :param height: Высота древа
        :return: Узлы древа (ветки)
        """

        return findall(self.root, lambda node: node.height == height)

    def update_branch(self, old_branch: Segment, new_branch: Segment) -> None:
        """
        Змена старой ветки на новоую ветвь.
        :param old_branch: Старая ветвь древа
        :param new_branch: Новая ветвь древа
        :return: None
        """

        branch = find(self.root, lambda node: node.segment == old_branch)
        if branch is None:
            raise ValueError('Passed node does not exist')

        branch.segment = new_branch

    @staticmethod
    def represent_branches_as_segments(branches: List[Branch] or Tuple[Branch]) -> List[Segment]:
        """
        Представить набор узлов древа (ветвей) в виде списка отрезков
        :param branches: Набор узлов древа (ветвей)
        :return: Набор отрезков
        """

        return [branch.segment for branch in branches]

    @staticmethod
    def get_children_branches(branch: Branch) -> List[Branch]:
        """

        :param branch:
        :return:
        """

        return [node for node in PreOrderIter(branch)]

    @staticmethod
    def get_children_branches_as_segments(branch: Branch) -> List[Segment]:
        """
        Получить дочерние узлы древа (ветки) от указанного узла (ветки) branch и представить их в виде массив отрезков
        для дальнейшей отрисовки на экране

        :param branch: Ветка с которой осуществляется поиск дочерних веток
        :return: Список дочерних отрезков
        """

        return [node.segment for node in PreOrderIter(branch)]

