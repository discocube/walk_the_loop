"""
Nodes and Edges classes
"""
import pygame.sprite
from random import randint

from game.settings import colors


class NodeSprite(pygame.sprite.Sprite):
    """
    Node class sprite.
    """
    def __init__(self, center=None, group=None, data=None, player_id=0, radius=11, numbered=True, screen=None, screen_rect=None):
        super().__init__(group)
        self.width = screen_rect[0]
        self.height = screen_rect[-1]
        self.center = center
        self.group = group
        self.data = data
        self.player_id = player_id
        self.radius = radius
        self.numbered = numbered
        self.screen = screen
        self.fp_inactive = f'/home/rommelo/Repos/walk_the_loop/game/icons/node_inactive.png'
        self.surface = pygame.image.load(self.fp_inactive).convert_alpha()
        self.rect = self.surface.get_rect(center=self.center)
        self.set_color()
        self.style = 'inactive'

    def set_color(self, style='inactive'):
        """
        Set color based on style.
        """
        self.style = style
        pygame.draw.circle(
            self.surface,
            colors[f'active_{self.player_id}' if self.style == 'active' else self.style],
            (self.radius, self.radius),
            self.radius if self.style == 'active' else 12,
        )
        if self.numbered:
            self.add_label()
        if style == 'origin':
            self.draw_border(style, player=True, radius=8, width=2)
        elif style == 'head':
            self.draw_border(style, player=True)

    def add_label(self):
        """
        Get label
        """
        text = pygame.font.SysFont('Oswald', 16).render(str(self.data), True, (255, 0, 255))
        self.surface.blit(text, text.get_rect(center=(self.radius, self.radius - 1)))

    def draw_border(self, style, player=False, radius=6, width=3):
        """
        Draw white ring in node denoting player head.
        """
        color = colors[('WHITE' if player else 'GRAY') if style == 'head' else ('GREEN' if player else 'GRAY')]
        pygame.draw.circle(
            surface=self.surface,
            color=color,
            center=(self.radius, self.radius),
            radius=radius,
            width=width)

    def set_winning(self):
        """
        Color nodes red for winning.
        """
        pygame.draw.circle(
            surface=self.surface,
            color=(randint(0, 255), randint(0, 255), randint(0, 255)),
            center=(self.radius, self.radius),
            radius=self.radius
        )


class Node(NodeSprite):
    """
    Node class.
    """
    def __init__(self, A=None, center=None, group=None, data=None, player_id=0, players=None, paths=None, radius=11, numbered=True, screen=None, screen_rect=None): # noqa
        super().__init__(center=center, group=group, data=data, player_id=player_id, radius=radius, numbered=numbered, screen=screen, screen_rect=screen_rect)  # noqa
        self.A = A
        self.players = players
        self.paths = paths

    @property
    def neighbors(self):
        """
        Nodes adjacent to node.
        """
        return self.A[self.data]

    @property
    def path(self):
        """
        Path in which the node belongs
        """
        if self.path_id is not None:
            return self.players.data[self.path_id].path.data

    @property
    def path_id(self):
        """
        Path in which the node belongs
        """
        for player_id, player in self.players.data.items():
            if self.data in player.path.data:
                return player_id
        return None

    @property
    def is_butt(self):
        """
        if node is self.path[0].
        """
        return self.data == self.path[0]

    @property
    def is_head(self):
        """
        if node is self.path[-1].
        """
        return self.data == self.path[-1]

    @property
    def is_end(self):
        """
        Is node head or butt?
        """
        if self.path:
            return self.data in (self.path[0], self.path[-1])

    @property
    def is_prev_step(self):
        """
        Last step?
        """
        return self.data == self.path[-2]

    @property
    def is_pivot(self):
        """
        Can I pivot with this node?
        """
        return self.data in self.path[1:-2]

    def is_adjacent(self, node):
        """
        If node is adjacent to head.
        """
        return node in self.neighbors

    @property
    def player(self):
        """
        Player container in which node belongs.
        """
        try:
            return self.players.data[self.player_id]
        except KeyError:
            print(self.players.data.keys(), self.players.data.values())
