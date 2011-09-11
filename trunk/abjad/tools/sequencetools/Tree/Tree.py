from abjad.core._StrictComparator import _StrictComparator


class Tree(_StrictComparator):
    r'''.. versionadded:: 2.4

    Abjad data structure to work with a sequence whose elements have been
    grouped into arbitrarily many levels of containment.

    One example would be a list of pitches that have been grouped 
    into cells that have, in turn, been grouped into groups of cells
    that have, in turn, been grouped into groups of groups of cells.
    
    ::

        abjad> from abjad.tools import sequencetools

    Here is a tree::

        abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
        abjad> tree = sequencetools.Tree(sequence)

    ::

        abjad> tree
        Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

    ::

        abjad> tree.parent is None
        True

    ::

        abjad> tree.children
        (Tree([0, 1]), Tree([2, 3]), Tree([4, 5]), Tree([6, 7]))

    ::

        abjad> tree.depth
        3

    Here's an internal node::

        abjad> tree[2]
        Tree([4, 5])

    ::

        abjad> tree[2].parent
        Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

    ::

        abjad> tree[2].children
        (Tree(4), Tree(5))

    ::

        abjad> tree[2].depth
        2

    ::

        abjad> tree[2].level
        1

    Here's a leaf node::


        abjad> tree[2][0]
        Tree(4)

    ::

        abjad> tree[2][0].parent
        Tree([4, 5])

    ::

        abjad> tree[2][0].children
        ()

    ::

        abjad> tree[2][0].depth
        1

    ::

        abjad> tree[2][0].level
        2

    ::

        abjad> tree[2][0].position
        (0, 2)

    ::

        abjad> tree[2][0].payload
        4

    Tree content is immutable.

    Only leaf nodes carry payload. Internal nodes carry no payload.

    Negative levels are available to work with trees bottom-up instead of top-down.
    '''

    def __init__(self, expr):
        self._children = []
        self.parent = None
        try:
            self.payload = None
            for element in expr:
                child = type(self)(element)
                self._children.append(child)
                child.parent = self
        except TypeError:
            self.payload = expr

    ### OVERLOADS ###

    def __contains__(self, expr):
        return expr in self._children

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.payload is not None or other.payload is not None:
                return self.payload == other.payload
            if len(self) == len(other):
                for x, y in zip(self, other):
                    if not x == y:
                        return False
                else:
                    return True
        return False

    def __getitem__(self, expr):
        return self._children[expr]

    def __len__(self):
        return len(self._children)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)

    def __str__(self):
        if self.payload is None:
            return '[%s]' % ', '.join([str(x) for x in self])
        else:
            return repr(self.payload)

    ### PUBLIC ATTRIBUTES ###

    @property
    def children(self):
        '''.. versionadded:: 2.4
        '''
        return tuple(self._children)

    @property
    def depth(self):
        '''.. versionadded:: 2.4
        '''
        levels = set([])
        for node in self.iterate_depth_first():
            levels.add(node.level)
        return max(levels) - self.level + 1

    @property
    def level(self):
        '''.. versionadded:: 2.4
        '''
        return len(self.proper_parentage)

    @property
    def improper_parentage(self):
        '''.. versionadded:: 2.4
        '''
        result = [self]
        cur = self.parent
        while cur is not None:
            result.append(cur)
            cur = cur.parent
        return result

    @property
    def index_in_parent(self):
        '''.. versionadded:: 2.4
        '''
        if self.parent is not None:
            return self.parent._children.index(self)
        else:
            return None

    @property
    def negative_level(self):
        '''.. versionadded:: 2.4
        '''
        return self.level - self.root.depth
        
    @property
    def position(self):
        '''.. versionadded:: 2.4
        '''
        result = []
        for node in self.improper_parentage:
            if node.parent is not None:
                result.append(node.index_in_parent)
        return tuple(result)

    @property
    def proper_parentage(self):
        '''.. versionadded:: 2.4
        '''
        return self.improper_parentage[1:]
    
    @property
    def root(self):
        '''.. versionadded:: 2.4
        '''
        return self.improper_parentage[-1]

    ### PUBLIC METHODS ###

    def iterate_at_level(self, level):
        r'''.. versionadded:: 2.4

        Iterate depth at `level`::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> for x in tree.iterate_at_level(0): x
            ... 
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

        ::

            abjad> for x in tree.iterate_at_level(1): x
            ... 
            Tree([0, 1])
            Tree([2, 3])
            Tree([4, 5])
            Tree([6, 7])

        ::

            abjad> for x in tree.iterate_at_level(2): x
            ... 
            Tree(0)
            Tree(1)
            Tree(2)
            Tree(3)
            Tree(4)
            Tree(5)
            Tree(6)
            Tree(7)

        ::

            abjad> for x in tree.iterate_at_level(-1): x
            ... 
            Tree(0)
            Tree(1)
            Tree(2)
            Tree(3)
            Tree(4)
            Tree(5)
            Tree(6)
            Tree(7)

        ::

            abjad> for x in tree.iterate_at_level(-2): x
            ... 
            Tree([0, 1])
            Tree([2, 3])
            Tree([4, 5])
            Tree([6, 7])

        ::

            abjad> for x in tree.iterate_at_level(-3): x
            ... 
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

        Return node generator.
        '''
        for x in self.iterate_depth_first():
            if 0 <= level:
                if x.level == level:
                    yield x
            else:
                if x.negative_level == level:
                    yield x

    def iterate_depth_first(self):
        '''.. versionadded:: 2.4

        Iterate tree depth-first::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> for node in tree.iterate_depth_first(): node
            ... 
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])
            Tree([0, 1])
            Tree(0)
            Tree(1)
            Tree([2, 3])
            Tree(2)
            Tree(3)
            Tree([4, 5])
            Tree(4)
            Tree(5)
            Tree([6, 7])
            Tree(6)
            Tree(7)

        Return node generator.
        '''
        yield self
        for x in self:
            for y in x.iterate_depth_first():
                yield y

    def iterate_payload(self):
        r'''.. versionadded:: 2.4

        Iterate tree payload::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> for element in tree.iterate_payload():
            ...     element
            ... 
            0
            1
            2
            3
            4
            5
            6
            7

        Return payload generator.
        '''
        for leaf_node in self.iterate_at_level(-1):
            yield leaf_node.payload
