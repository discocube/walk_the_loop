"""
Player class.
"""
from game.pieces.path import Path


class Player:
    """
    Player class
    """
    def __init__(self, A=None, data=None, player_id=0, players=None, debug=False):
        self.A = A
        self.ORD = len(self.A.keys())
        self.id = player_id
        self.path = Path(A=A, data=data or [], player_id=self.id)

        self.players = players
        self.debug = debug

    @property
    def max_stepped(self):
        """
        Max number steps taken
        """
        return len(self.players.stepped) == self.ORD

    @property
    def head(self):
        """
        self.path[-1]
        """
        return self.path[-1]

    @property
    def butt(self):
        """
        self.path[0]
        """
        return self.path[0]

    @property
    def ends(self):
        """
        Butt and head.
        """
        return self.head, self.butt

    @property
    def next_steps(self):
        """
        Steps adjacent to head.
        """
        return self.A[self.path[-1]]

    @property
    def is_new(self):
        """
        Check if path is still empty.
        """
        return not len(self.path)

    def in_path(self, node):
        """
        If node in path.
        """
        return node in self.path

    def step(self, node):
        """
        Take a step, record in stepped.
        """
        if node not in self.players.stepped:
            self.path.data.append(node)

    def skip(self, node):
        """
        SKIP
        """
        self.path.skip(node)

    def step_back(self):
        """
        Backtrack and remove last step.
        """
        return self.path.back()

    def switch_head(self):
        """
        Reverse path to reassign head.
        """
        self.path.reverse()

    def __repr__(self):
        """
        Return info on path object.
        """
        return f"{self.path}"
