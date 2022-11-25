"""
Path class for player. Container class for placing steps when walking.
"""

from more_itertools import windowed
from src.game.utils import id_seq


class Path:
    """
    Path class for container for steps.
    """
    def __init__(self, A=None, data=None, player_id=0):
        self.A = A
        self.data = data or []
        self.id = player_id

    @property
    def loop_edge(self):
        """
        Edge that closes the loop. (path[0], path[-1).
        Separated in order to render a different color when needed.
        """
        if self.is_loop:
            return self.data[0], self.data[-1]

    @property
    def max_stepped(self):
        """
        Maximum number of steps has been reached.
        """
        return len(self.data) == len(self.A.keys())

    @property
    def edges(self):
        """
        Player as edges.
        windowed(self.path + self.path[:1] if self.is_loop else self.path, 2).
        If loop but edges need another coloring.
        """
        if self.has_edge:
            return windowed(self.data + self.data[:1] if self.is_hamiltonian else self.data, 2)
        return False

    @property
    def has_edge(self):
        """
        If path has at least an edge, i.e.,  two nodes.
        """
        return len(self.data) > 1

    @property
    def next_steps(self):
        """
        Steps adjacent to head.
        """
        return self.A[self.data[-1]]

    @property
    def seq_type(self):
        """
        Get sequence type: snake, loop or broken.
        """
        return id_seq(self.data, self.A)

    @property
    def is_loop(self):
        """
        True if sequence is a loop.
        """
        return self.seq_type == 'loop'

    @property
    def is_hamiltonian(self):
        """
        Test if end is a loop and the length is equal to the number of vertices.
        """
        return self.is_loop and self.max_stepped

    def index(self, n):
        """
        Get node from this path.
        """
        return self.data.index(n)

    def is_head(self, node):
        """
        if node is self.path[-1].
        """
        return node == self.data[-1]

    def is_butt(self, node):
        """
        if node is self.path[0].
        """
        return node == self.data[0]

    def is_end(self, node):
        """
        If node is an end: seq[0] or seq[-1]
        """
        return node in (self.data[0], self.data[-1])

    def in_body(self, node):
        """
        if node is not either head nor origin.
        """
        return node in self.data[1:-1]

    def rotate(self, node):
        """
        Swap the head to another if seq is loop.
        """
        if self.is_loop:
            # if not node.is_head:
            idx = self.data.index(node)
            self.data = self.data[idx + 1:] + self.data[:idx + 1]
        else:
            pass
            # raise TypeError('SEQUENCE MUST BE A LOOP')

    def split(self, node):
        """
        Spit sequence into a loop and a snake.

        node to click to activate split is self.path[0] before hand or self.path[idx - 1]
        """
        idx = self.data.index(node)
        new_path = self.data[:idx]
        self.data = self.data[idx:]
        return new_path

    def skip(self, node):
        """
        SKIP
        """
        idx = self.data.index(node)
        self.data[idx + 1:] = self.data[:idx:-1]

    def rewind(self, node):
        """
        Move back many steps.
        """
        idx = self.data.index(node)
        self.data[:] = self.data[:idx + 1]

    def reverse(self):
        """
        FLIP.
        """
        self.data[:] = self.data[::-1]

    def back(self):
        """
        Pop last node in sequence.
        """
        return self.data.pop()

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f'{self.data}'
