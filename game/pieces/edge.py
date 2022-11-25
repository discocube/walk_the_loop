"""
Edge class
"""
from math import sqrt
import pygame

from game.settings import colors


class Point:
    """
    Point class for making dotted lines.
    """
    def __init__(self, point_t=(0, 0)):
        self.x = float(point_t[0])
        self.y = float(point_t[1])

    @property
    def vectors(self):
        """
        Get x, y values as tuple.
        """
        return self.x, self.y

    def __add__(self, b):
        return Point((self.x + b.x, self.y + b.y))

    def __sub__(self, b):
        return Point((self.x - b.x, self.y - b.y))

    def __mul__(self, n):
        return Point((self.x * n, self.y * n))

    def __truediv__(self, n):
        return Point((self.x / n, self.y / n))

    def __len__(self):
        return int(sqrt(self.x**2 + self.y**2))


class Edge(pygame.sprite.Sprite):
    """
    Edge class.
    """
    def __init__(self, center=None, style='inactive', group=None, data=None, pm=None, pn=None, player_id=0, screen_rect=None):
        super(Edge, self).__init__(group)

        self.width = screen_rect[0]
        self.height = screen_rect[1]
        self.thickness = 6
        self.center = center
        self.pm, self.pn = pm, pn
        self.player_id = player_id
        self.style = style
        self.group = group
        self.data = data
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        pygame.draw.line(self.surface, colors[self.style], self.pm, self.pn, width=self.thickness)

    def set_color(self, style='inactive'):
        """
        Change color based on style.
        """
        self.style = style
        pygame.draw.line(
            surface=self.surface,
            color=colors[f'active_{self.player_id}' if self.style == 'active' else self.style],
            start_pos=self.pm,
            end_pos=self.pn,
            width=self.thickness
        )

    def draw_dashed(self, style='active', dash_length=10):
        """
        Draw dashed edge.
        """
        origin, target = Point(self.pm), Point(self.pn)
        slope = (displacement := target - origin) / (length := len(displacement))
        for index in range(0, length // dash_length, 2):
            start = origin + (slope * index * dash_length)
            end = origin + (slope * (index + 1) * dash_length)
            pygame.draw.line(
                surface=self.surface,
                color=colors[f'active_{self.player_id}' if style == 'active' else style],
                start_pos=start.vectors,
                end_pos=end.vectors,
                width=self.thickness - 4)
