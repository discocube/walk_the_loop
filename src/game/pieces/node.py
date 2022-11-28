"""
Nodes and Edges classes
"""
import os
import pygame.sprite
from pygame import gfxdraw
from random import randint

from src.game.settings import COLORS
from src.game.definitions import ICONS_DIR
from src.game.utils import scale_point


class NodeSprite(pygame.sprite.Sprite):
    """
    Node class sprite.
    """
    def __init__(self, scale=1, center=None, group=None, data=None, player_id=0, radius=1, numbered=True, screen=None, screen_rect=None):
        super().__init__(group)
        self._surface = None
        self.scale = scale
        self.node_rect = scale_point((22, 22), self.scale)
        self.node_center = scale_point(self.node_rect, .5, intd=True)
        self.screen_rect = scale_point(screen_rect, self.scale)
        self.width = self.screen_rect[0]
        self.height = self.screen_rect[-1]
        self.center = scale_point(center, self.scale)

        self.group = group
        self.data = data
        self.player_id = player_id
        self.radius = int(radius * self.scale)
        self.numbered = numbered
        self.screen = screen
        self.style = 'inactive'
        self.fp_inactive = os.path.join(ICONS_DIR, 'node_inactive_hires.png')
        hires_surface = pygame.image.load(self.fp_inactive)
        self.surface = pygame.transform.scale(hires_surface, self.node_rect)
        self.rect = self.surface.get_rect(center=self.center)
        self.set_color()

    def set_color(self, style='inactive'):
        """
        Set color based on style.
        """
        self.style = style
        self.draw_circle()
        if self.numbered:
            self.add_label()
        if style == 'origin':
            self.draw_border(style, player=True)
        elif style == 'head':
            self.draw_border(style, player=True)

    def draw_circle(self, radius=None, color=None):
        """
        Draw aa-circle
        """
        gfxdraw.aacircle(self.surface, *self.node_center, radius or self.radius, color or COLORS[f'active_{self.player_id}' if self.style == 'active' else self.style])
        gfxdraw.filled_circle(self.surface, *self.node_center, radius or self.radius, color or COLORS[f'active_{self.player_id}' if self.style == 'active' else self.style])

    def add_label(self):
        """
        Get label
        """
        text = pygame.font.SysFont('Oswald', 16).render(str(self.data), True, (255, 0, 255))
        self.surface.blit(text, text.get_rect(center=(self.radius, self.radius - 1)))

    def draw_border(self, style, player=False, radius=8):   # noqa
        """
        Draw white ring in node denoting player head.
        """
        self.draw_circle(radius=self.radius, color=None)

    def set_winning(self):
        """
        Color nodes red for winning.
        """
        pygame.draw.circle(
            surface=self.surface,
            color=(randint(0, 255), randint(0, 255), randint(0, 255)),
            center=self.node_center,
            radius=self.radius
        )


class Node(NodeSprite):
    """
    Node class.
    """
    def __init__(self, A=None, scale=1, center=None, group=None, data=None, player_id=0, players=None, paths=None, radius=10, numbered=True, screen=None, screen_rect=None): # noqa
        super().__init__(scale=scale, center=center, group=group, data=data, player_id=player_id, radius=radius, numbered=numbered, screen=screen, screen_rect=screen_rect)  # noqa
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
