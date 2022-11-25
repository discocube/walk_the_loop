"""
Players class.
"""
from typing import Optional

from game.pieces.player import Player
from game.utils import unpack


class Players:
    """
    Players class to deal with many Players.
    Combine, separate, create Players.
    """

    def __init__(self, G, nodes=None):
        self.G = G
        self.A = self.G['A']
        self.ORD = len(self.A)
        self.data = {}
        self.current_idx = None
        self.nodes = nodes

    @property
    def stepped(self):
        """
        Nodes which have been stepped.
        """
        return {*unpack([player.path.data for player in self.data.values()])}

    @property
    def unstepped(self):
        """
        Nodes not taken.
        """
        return {*range(self.ORD)}.difference(self.stepped)

    @property
    def ends(self):
        """
        All the ends of all Players.
        """
        return {*unpack([(player.path.data[0], player.path.data[-1]) for player in self.data.values()])}

    @property
    def current(self):
        """
        Current path.
        """
        return self.data[self.current_idx]

    @property
    def new_key(self):
        """
        Figure out which keys have been discarded, or make new if all are used.
        """
        if self.current_idx is None:
            return 0
        return min({*range(max(self.data.keys()) + 2)}.difference(self.data.keys()))

    def add_player(self, data: Optional[list[int]] = None) -> None:
        """
        Add new path.
        """
        self.current_idx = self.new_key
        self.data[self.current_idx] = Player(A=self.G['A'], data=data, player_id=self.current_idx, players=self)

    def __len__(self):
        """
        Return length of self.data.keys()
        """
        return len(self.data.keys())
