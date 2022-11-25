# Shira Taitelbaum 322207341
# There is no priority in Python which allows custom sorting function
import heapq
from functools import total_ordering

from ways.info import SPEED_RANGES


# I used the code from the class' github
class PriorityQueue :

    def __init__(self, f=lambda x : x) :
        self.heap = []
        self.f = f

    def append(self, item) :
        heapq.heappush(self.heap, (self.f(item), item))

    def extend(self, items) :
        for item in items :
            self.append(item)

    def pop(self) :
        if self.heap :
            return heapq.heappop(self.heap)[1]
        else :
            raise Exception('Trying to pop from empty PriorityQueue.')

    def __len__(self) :
        return len(self.heap)

    def __contains__(self, key) :
        return any([item == key for _, item in self.heap])

    def __getitem__(self, key) :
        for value, item in self.heap :
            if item == key :
                return value
        raise KeyError(str(key) + " is not in the priority queue")

    def __delitem__(self, key) :
        try :
            del self.heap[[item == key for _, item in self.heap].index(True)]
        except ValueError :
            raise KeyError(str(key) + " is not in the priority queue")
        heapq.heapify(self.heap)

    def __repr__(self) :
        return str(self.heap)


@total_ordering
class Node :
    def __init__(self, junction_inx, parent=None, path_cost=0, real_path_cost=0) :
        self.junction_inx = junction_inx
        self.parent = parent
        self.path_cost = path_cost
        self.real_path_cost = real_path_cost

    def expand(self, juc, f) :
        neighbors = []
        for i in range(len(juc.links)) :
            node = Node(juc.links[i].target, self)
            node.path_cost = self.path_cost + f(node)
            neighbors.append(node)
        return neighbors

    def expandastar(self, juc, f, g) :
        neighbors = []
        for i in range(len(juc.links)) :
            node = Node(juc.links[i].target, self)
            node.path_cost = self.path_cost + f(node)
            node.real_path_cost = self.real_path_cost + g(node)
            neighbors.append(node)
        return neighbors

    def path(self) :
        node, path_back = self, []
        while node :
            path_back.append(node.junction_inx)
            node = node.parent
        path_back.reverse()
        return list(path_back)

    def __repr__(self) :
        return f"<{self.junction_inx}>"

    def __lt__(self, node) :
        return self.junction_inx < node.junction_inx

    def __eq__(self, other) :
        return isinstance(other, Node) and self.junction_inx == other.junction_inx

    def __ne__(self, other) :
        return not (self == other)

    def __hash__(self) :
        return hash(self.junction_inx)
