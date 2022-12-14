"""
Edge class
"""
from math import sqrt
import pygame

from src.game.defs import COLORS
from src.game.utils import scale_point


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
    def __init__(self, scale=1, thickness=6, style='inactive', group=None, data=None, pm=None, pn=None, player_id=0, screen_rect=None, surface=None):
        super(Edge, self).__init__(group)
        self.scale = scale
        self.screen_rect = scale_point(screen_rect, self.scale, intd=True)
        self.width = screen_rect[0]
        self.height = screen_rect[1]
        self.thickness = int(thickness * self.scale)
        self.pm, self.pn = scale_point(pm, self.scale), scale_point(pn, self.scale)
        self.player_id = player_id
        self.style = style
        self.group = group
        self.data = data
        self.surface = surface or pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        pygame.draw.aaline(self.surface, COLORS[self.style], self.pm, self.pn)

    def set_color(self, style='inactive'):
        """
        Change color based on style.
        """
        self.style = style
        self.thickness = self.thickness
        self.draw_black_line()
        pygame.draw.aaline(
            surface=self.surface,
            color=COLORS[f'active_{self.player_id}' if self.style == 'active' else self.style],
            start_pos=self.pm,
            end_pos=self.pn,
        )

    def draw_black_line(self, thickness=3):
        """
        Change color based on style.
        """
        pygame.draw.line(
            surface=self.surface,
            color=COLORS['BLACK'],
            start_pos=self.pm,
            end_pos=self.pn,
            width=thickness
        )

    def draw_lines(self, points, style='inactive', closed=False):
        """
        Draw multiple lines.
        """
        self.style = style
        pygame.draw.aalines(
            surface=self.surface,
            color=COLORS[f'active_{self.player_id}' if self.style == 'active' else self.style],
            closed=closed,
            points=points,
        )

    def draw_dashed_gen(self, style='active', dash_length=5, origin_node=None):
        """
        Draw dashed edge.
        """
        origin = Point(self.pm) if origin_node == self.data[0] else Point(self.pn)
        target = Point(self.pn) if origin_node == self.data[0] else Point(self.pm)
        slope = (displacement := target - origin) / (length := len(displacement))
        dash_length = int(length / 100) or 1

        for index in range(0, length // dash_length):
            start = origin + (slope * index * dash_length)
            end = origin + (slope * (index + 1) * dash_length)
            yield pygame.draw.aaline(
                    surface=self.surface,
                    color=COLORS[f'active_{self.player_id}' if style == 'active' else style],
                    start_pos=start.vectors,
                    end_pos=end.vectors,
                )

    def draw_dashed(self, style='active', dash_length=8, origin_node=None):
        """
        Draw dashed edge.
        """
        origin = Point(self.pm) if origin_node == self.data[0] else Point(self.pn)
        target = Point(self.pn) if origin_node == self.data[0] else Point(self.pm)
        slope = (displacement := target - origin) / (length := len(displacement))
        for index in range(0, length // dash_length, 2):
            start = origin + (slope * index * dash_length)
            end = origin + (slope * (index + 1) * dash_length)
            pygame.draw.aaline(
                    surface=self.surface,
                    color=COLORS[f'active_{self.player_id}' if style == 'active' else style],
                    start_pos=start.vectors,
                    end_pos=end.vectors,
                )
