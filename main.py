import numpy as np
import matplotlib.pyplot as plt

class Node:

    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def compair(self, value, index, toggle):
        if value[index] < self.value[index]:
            if self.left:
                self.left.add(value, not toggle)
            else:
                self.left = Node(value)
        else:
            if self.right:
                self.right.add(value, not toggle)
            else:
                self.right = Node(value)

    def add(self, value, toggle):
        if toggle:
            self.compair(value, 0, toggle)
        else:
            self.compair(value, 1, toggle)

    def contains(self, value, toggle):
        idx = 1 - int(toggle)
        if self.value == value:
            return True
        else:
            if value[idx] < self.value[idx]:
                if self.left:
                    return self.left.contains(value, not toggle)
                else:
                    return False
            else:
                if self.right:
                    return self.right.contains(value, not toggle)
                else:
                    return False
    def range_search(self, min_coords, max_coords, list, toggle):
        idx = 1 - int(toggle)
        if min_coords[0] <= self.value[0] <= max_coords[0] and min_coords[1] <= self.value[1] <= max_coords[1]:
            list.append(self.value)
        if self.left and min_coords[idx] < self.value[idx]:
            self.left.range_search(min_coords, max_coords, list, not toggle)
        if self.right and max_coords[idx] > self.value[idx]:
            self.right.range_search(min_coords, max_coords, list, not toggle)

    def findDepth(self, depth):
        print(depth)
        if self.left:
            self.left.findDepth(depth + 1)
        if self.right:
            self.right.findDepth(depth+1)



class KDTree:

    def __init__(self):
        self.root = None

    def add(self, value):
        if not self.root:
            self.root = Node(value)
        else:
            self.root.add(value, True)

    def contains(self, value):
        if not self.root:
            return False
        else:
            return self.root.contains(value, True)

    def range_search(self, min_coords, max_coords):
        """
        Return [(x1, y1), (x2, y2), ...]

        min_coords[0]: min x coord of rectangle
        min_coords[1]: min y coord of rectangle

        max_coords[0]: max x coord of rectangle
        max_coords[1]: max y coord of rectangle
        """
        list = []
        if self.root:
            self.root.range_search(min_coords, max_coords, list, True)
        return list

    def insert_list(self, X, toggle = True):
        """
        Takes in a list of [[x1, y1], [x2, y2]] and inserts a balanced subtree
        """
        if len(X) == 1:
            self.add(X[0])
        elif len(X) > 0:
            idx = 1 - int(toggle)
            XSorted = sorted(X, key=lambda u: u[idx])
            middleIdx = len(XSorted)//2
            self.add(XSorted[middleIdx])
            left = XSorted[:middleIdx]
            self.insert_list(left, not toggle)
            right = XSorted[middleIdx + 1:]
            self.insert_list(right, not toggle)

    def findDepth(self):
        self.root.findDepth(0)


def test_range():
    np.random.seed(0)
    X = np.random.rand(1000, 2)
    tree = KDTree()
    xmin = 0.1
    xmax = 0.2
    ymin = 0.6
    ymax = 0.7
    ## Brute force
    XBrute = X[(X[:, 0] >= xmin)*(X[:, 0] <= xmax)*(X[:, 1] >= ymin)*(X[:, 1] <= ymax), :]
    for x in X:
        tree.add((x[0], x[1]))
    XMy = tree.range_search((xmin, ymin), (xmax, ymax))
    print(len(XMy)) # Should be 11
    XMy = np.array(XMy)
    plt.scatter(X[:, 0], X[:, 1])
    plt.scatter(XBrute[:, 0], XBrute[:, 1], c='C1')
    plt.scatter(XMy[:, 0], XMy[:, 1], marker='x', c='C2')
    plt.show()

def test_list():
    np.random.seed(0)
    X = np.random.rand(31, 2).tolist()
    tree = KDTree()
    tree.insert_list(X)
    res = tree.range_search((-10, -10), (10, 10))
    tree.findDepth()


if __name__ == '__main__':
    test_list()

