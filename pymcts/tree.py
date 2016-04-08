from typing import Any, Generator, Generic, List, Optional, TypeVar

T = TypeVar('T')


class Node(Generic[T]):
    """A generic tree node. Nodes point to their parents, and nodes may have multiple children."""

    def __init__(self, value: T, children: List['Node[T]']=None) -> None:
        self._parent = None  # type: Node[T]
        self._children = []  # type: List[Node[T]]

        self.value = value
        if children:
            self.children = children

    @property
    def children(self) -> List['Node[T]']:
        return self._children

    @children.setter
    def children(self, children: List['Node[T]']=None) -> None:
        if children:
            for child in children:
                child._parent = self
            self._children = children

    @property
    def parent(self) -> 'Node[T]':
        return self._parent

    def add_children(self, children: List['Node[T]']=None):
        if children:
            self.children = self.children + children
        return self

    def add_child(self, child: 'Node[T]'):
        self.add_children([child])
        return self

    def __repr__(self):
        return '{clz}(v={value!r}, [{children}])'.format(
            clz=self.__class__.__name__,
            value=self.value,
            children=', '.join(repr(c) for c in self._children) if self._children else '')

    def traverse_postorder(self) -> Generator["Node[T]", Any, "Node[T]"]:
        """
        Traverse tree rooted at this node via post-order DFS. Results are undefined if
        the tree is modified concurrently.
        """
        for child in self.children:
            yield from child.traverse_postorder()
        yield self


# Empty trees are just None
# Note that mypy doesn't yet support this, but it's in PEP 484
Tree = Optional[Node[T]]
