"""
Icons for game. Not game pieces.
"""
import os
import pygame

from src.game.definitions import ICONS_DIR
from src.game.pieces.edge import Edge
from src.game.settings import COLORS, G_POLYHEDRA
from src.game.utils import scale_point


class DrawnIcon(pygame.sprite.Sprite):
    """
    small icon.
    """
    def __init__(self, style='WHITE', name=None, screen_rect=(100, 100), center=(900, 100), scale=1, path_obj=None, group=None):
        super().__init__(group)
        self.style = style
        self.name = name
        self.scale = scale
        self.screen_rect = scale_point(screen_rect, self.scale)
        self.center = scale_point(center, self.scale)
        self.width = screen_rect[0]
        self.height = screen_rect[1]
        self.path_obj = path_obj
        self.graph = G_POLYHEDRA[f'{self.name}_3d']
        self.V = [[(v / 10) * self.scale for v in vector] for vector in self.graph['V']]
        self.E = self.graph['E']
        self._surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.edges = {frozenset(e): Edge(thickness=3, group=group, data=e, pm=self.V[e[0]], pn=self.V[e[1]], screen_rect=self.screen_rect, surface=self.surface) for e in self.E}
        self.E = {frozenset(e) for e in self.graph['E']}
        self.points = [self.V[node] for node in self.graph['lines']]
        self.rect = self._surface.get_rect(center=self.center)
        self.draw_lines()

    def draw_lines(self, style='GRAY', points=None, closed=False):
        """
        Draw multiple lines.
        """
        pygame.draw.aalines(
            surface=self._surface,
            color=COLORS[style],
            closed=closed,
            points=points or self.points,
            blend=4,
        )

    @property
    def surface(self):
        """
        Change color based on style.
        """
        if self.path_obj.edges:
            self.draw_lines(style='active', points=[self.V[n] for n in self.path_obj.data])

            active_edges = {frozenset(e) for e in self.path_obj.edges}
            for edge in self.E:
                if edge in active_edges:
                    self.edges[edge].set_color(style='active', thickness=4)
                else:
                    self.edges[edge].set_color(thickness=4)
        return self._surface


class ActionIcon(pygame.sprite.Sprite):
    """
    Graph icon.
    """
    def __init__(self, screen_rect=(100, 100), center=(250, 400), name='DISCO', scale=1, current_graph_type=None, group=None):
        super().__init__(group)
        self.scale = scale
        self.screen_rect = scale_point(screen_rect, self.scale)
        self.center = scale_point(center, self.scale)
        self.current_graph_type = current_graph_type
        self.name = name
        self.high_res_surface = pygame.image.load(os.path.join(ICONS_DIR, f'{self.name}.png'))
        self._surface = pygame.transform.scale(self.high_res_surface, self.screen_rect)
        self.rect = self._surface.get_rect(center=self.center)

    @property
    def surface(self):
        """
        Surface property.
        """
        current = int(self.current_graph_type == self.name) or ""
        self.high_res_surface = pygame.image.load(os.path.join(ICONS_DIR, f'{self.name}{current}.png'))
        self._surface = pygame.transform.scale(self.high_res_surface, self.screen_rect)
        self.rect = self._surface.get_rect(center=self.center)
        return self._surface


class ToggleIcon(pygame.sprite.Sprite):
    """
    Play pause icons.
    """
    def __init__(self, screen_rect=(50, 50), center=(500, 750), name="play&pause", scale=1, group=None, animate_state=False):
        super().__init__(group)
        self.scale = scale
        self.screen_rect = [point * self.scale for point in screen_rect]
        self.center = [point * self.scale for point in center]
        self.name = name

        self.state = animate_state
        self._surface, self.rect = None, None
        self.hires_surface = pygame.image.load(os.path.join(ICONS_DIR, f'{self.name}_{int(not self.state)}.png'))

    @property
    def surface(self):
        """
        High-resolution icon as a _surface.
        """
        hires_surface = pygame.image.load(os.path.join(ICONS_DIR, f'{self.name}_{int(not self.state)}.png'))
        self._surface = pygame.transform.scale(hires_surface, self.screen_rect)
        self.rect = self._surface.get_rect(center=self.center)
        return self._surface

    def switch(self):
        """
        Switch from play to pause.
        """
        self.state = int(not self.state)
        self.scale_hires()

    def scale_hires(self):
        """
        Draw icon.
        """
        self._surface = pygame.transform.scale(self.hires_surface, self.screen_rect)
        self.rect = self._surface.get_rect(center=self.center)
        return self._surface, self.rect
