from Error import IncomparableItemsRaiser


class BinarySearchTree:
    def __init__(self, value):
        self.__value = value
        self.__left_child = None
        self.__right_child = None
        self.__parent = None

    def __repr__(self):
        return '\n'.join(self.display())

    def get_value(self):
        return self.__value

    def get_left(self):
        return self.__left_child

    def get_right(self):
        return self.__right_child

    def get_parent(self):
        return self.__parent

    def set_value(self, value):
        self.__value = value

    def set_left(self, left):
        self.__left_child = left
        if type(left) is BinarySearchTree:
            left.set_parent(self)

    def set_right(self, right):
        self.__right_child = right
        if type(right) is BinarySearchTree:
            right.set_parent(self)

    def set_parent(self, parent):
        self.__parent = parent

    def has_value(self):
        return self.get_value() is not None

    def has_left(self):
        return self.get_left() is not None

    def has_right(self):
        return self.get_right() is not None

    def has_parent(self):
        return self.get_parent() is not None

    def is_empty(self):
        return not self.has_value() and self.is_leaf()

    def is_leaf(self):
        return not self.has_right() and not self.has_left()

    def min_value(self):
        current = self

        while current.has_left():
            current = current.get_left()

        return current.get_value()

    def max_value(self):
        current = self

        while current.has_right():
            current = current.get_right()

        return current.get_value()

    def search(self, value):
        try:
            if self.get_value() == value:
                return self
            elif self.get_value() > value:
                return self.get_left().search(value) if self.has_left() else None
            else:
                return self.get_right().search(value) if self.has_right else None
        except TypeError:
            raise IncomparableItemsRaiser(value)

    def insert(self, value):
        try:
            if self.is_leaf() and not self.has_value():
                self.set_value(value)
                return self

            if self.get_value() > value:
                if not self.has_left():
                    self.set_left(BinarySearchTree(value))
                    return self.get_left()
                else:
                    return self.get_left().insert(value)
            elif self.get_value() < value:
                if not self.has_right():
                    self.set_right(BinarySearchTree(value))
                    return self.get_right()
                else:
                    return self.get_right().insert(value)
        except TypeError:
            raise IncomparableItemsRaiser(value)

    def remove(self, value):
        if value is None:
            return

        node = self.search(value)

        if node.has_parent():
            parent = node.get_parent()

            if node.is_leaf():
                if parent.get_left() == node:
                    parent.set_left(None)
                else:
                    parent.set_right(None)

            else:
                if node.has_right() and node.has_left():
                    left = node.get_left()
                    parent.set_right(node.get_right())
                    temp = parent.get_right()
                    while temp.has_left():
                        temp = temp.get_left()
                    temp.set_left(left)

                elif not node.has_left():
                    parent.set_right(node.get_right())

                else:
                    parent.set_right(node.get_left())

            return self

        else:
            if node.is_leaf():
                return None

            if not node.has_right():
                return node.get_left()

            if not node.has_left():
                return node.get_right()

            left = node.get_left()
            right = node.get_right()
            temp = right

            while temp.has_left():
                temp = temp.get_left()

            temp.set_left(left)

            return right

    def get_all_nodes(self):
        return self.get_left().get_all_nodes() \
                if self.has_left() else [] + [self.get_value()] + \
                self.get_right().get_all_nodes() if self.has_right() else []

    def _balance(self, nodes, start, end):
        if start > end:
            return None

        mid = (start + end) // 2
        node = nodes[mid]

        node.set_left(self._balance(nodes, start, mid - 1))
        node.set_right(self._balance(nodes, mid + 1, end))

        return node

    def balance(self):
        nodes = self.get_all_nodes()
        return self._balance(nodes, 0, len(nodes) - 1)

    def depth(self):
        if self.is_leaf():
            return 1
        return 1 + max(self.get_left().depth() if self.has_left() else 0,
                       self.get_right().depth() if self.has_right() else 0)

    def find_max_node_length(self):
        return max(len(str(self.get_value())),
                   self.get_left().find_max_node_length() if self.has_left() else -1,
                   self.get_right().find_max_node_length() if self.has_right() else -1)

    def values_in_level(self, level):
        if level == 0:
            return [str(self.get_value())]

        return (self.get_left().values_in_level(level-1) if self.has_left() else [''] * (2 ** (level - 1))) + \
               (self.get_right().values_in_level(level-1) if self.has_right() else [''] * (2 ** (level - 1)))

    def display(self):
        lines = []
        node_width = self.find_max_node_length()
        node_width += ((node_width + 1) % 2)
        depth = self.depth()
        line_width = (2 ** depth - 1) * node_width
        spacer1 = (line_width - node_width) // (2 * node_width)
        space1 = ' ' * node_width * spacer1

        left_corner = (' ' * (node_width - 1) + '_')
        right_corner = ('_' + ' ' * (node_width - 1))
        middle_spacer = (' ' * ((node_width - 1) // 2) + '|' + ' ' * ((node_width - 1) // 2))
        _ = '_' * node_width

        for level in range(depth):
            spacer2 = 2 * spacer1 + 1
            space2 = ' ' * node_width * spacer2
            line1 = ''
            line2 = space1
            line3 = space1
            values = [('{:^%s.%s}' % (node_width, node_width)).format(j) for j in self.values_in_level(level)]
            for i in range(len(values)):
                if i < len(values) // 2:
                    cond1 = len(values[i * 2].strip()) > 0
                    cond2 = len(values[i * 2 + 1].strip()) > 0
                    left = (left_corner + _ * spacer1 if cond1 else ' ' * (node_width + node_width*spacer1))
                    right = (_ * spacer1 + right_corner if cond2 else ' ' * (node_width + node_width*spacer1))
                    middle = (('_' if cond1 else ' ') * ((node_width - 1) // 2) +
                              ('|' if(cond1 or cond2) else ' ') +
                              ('_' if cond2 else ' ') * ((node_width - 1) // 2))
                    ___ = left + middle + right
                    line1 += (space1 + ___ + space1 + ' ' * node_width)

                line2 += (middle_spacer if len(values[i].strip()) > 0 else ' ' * node_width) + space2
                line3 += values[i] + space2

            if level > 0:
                lines.append(line1)
                lines.append(line2)
            lines.append(line3)
            spacer1 = (spacer1 - 1) // 2
            space1 = ' ' * node_width * spacer1

        return lines


class LinkedList:
    def __init__(self, value):
        self.__value = value
        self.__next = None
        self.__prev = None

    def __repr__(self):
        return ''.join(self.display())

    def get_value(self):
        return self.__value

    def get_next(self):
        return self.__next

    def get_prev(self):
        return self.__prev

    def set_value(self, value):
        self.__value = value

    def set_next(self, next_):
        self.__next = next_

        if next_ is not None:
            next_.set_prev(self)

    def set_prev(self, prev):
        self.__prev = prev

    def is_empty(self):
        return self.get_value() is None and self.get_next() is None

    def insert_at_head(self, value):
        old_value = self.get_value()
        old_next = self.get_next()
        self.set_value(value)
        self.set_next(LinkedList(old_value))
        self.get_next().set_next(old_next)

    def insert_at_end(self, value):
        temp = self

        while temp.get_next() is not None:
            temp = temp.get_next()

        temp.set_next(LinkedList(value))

    def search(self, value):
        temp = self

        while temp is not None:
            if temp.get_value() == value:
                break
            temp = temp.get_next()

        return temp

    def delete(self, value):
        node = self.search(value)

        if node.get_prev() is not None:
            node.get_prev().set_next(node.get_next())
        else:
            self.set_value(self.get_next().get_value())
            self.set_next(self.get_next().get_next())

    def display(self):
        temp = self
        lines = []

        while temp.get_next() is not None:
            lines.append(str(temp.get_value()) + ' <--> ')
            temp = temp.get_next()

        lines.append(temp.get_value())

        return lines


class Stack:
    def __init__(self):
        self.values = []

    def __repr__(self):
        return '\n'.join(self.display())

    def top(self):
        return self.values[-1]

    def push(self, value):
        self.values.append(value)

    def pop(self):
        try:
            return self.values.pop()
        except IndexError:
            pass

    def is_empty(self):
        return len(self.values) == 0

    def reverse(self):
        _reversed = Stack()

        while not self.is_empty():
            _reversed.push(self.pop())

        self.values = _reversed.values

    def display(self):
        lines = []

        if len(self.values) > 0:
            max_node_length = max(len(str(i)) for i in self.values)
            top_line = ' %s ' % ('_' * (max_node_length + 2))
            bottom_line = top_line.replace('_', '͞')
            lines.append(top_line)
            for i in range(len(self.values)):
                value = self.values[-i-1]
                line = ('| {:^%s.%s} |' % (max_node_length, max_node_length)).format(str(value))
                lines.append(line + (' <- Top' if i == 0 else ''))
            lines.append(bottom_line)
        else:
            lines.append(' __ \n|  |\n ͞͞ \n')

        return lines


class RedBlackTree:
    pass


class AVLTree:
    pass


class WAVLTree:
    pass


class MaxHeap:
    pass


class Graph:
    pass
