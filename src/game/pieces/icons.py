"""
Icons for game. Not game pieces.
"""
import os
import pygame

from src.game.definitions import ICONS_DIR


class Icon(pygame.sprite.Sprite):
    """
    small icon.
    """
    def __init__(self, screen_rect=(100, 100), center=(900, 100), name='DISCO', group=None):
        super().__init__(group)
        self.screen_rect = screen_rect
        self.name = name
        self.high_res_surface = pygame.image.load(os.path.join(ICONS_DIR, f'{self.name}_s.png'))
        self.surface = pygame.transform.scale(self.high_res_surface, self.screen_rect)
        self.center = center
        self.rect = self.surface.get_rect(center=self.center)


class GraphIcon(pygame.sprite.Sprite):
    """
    Graph icon.
    """
    def __init__(self, screen_rect=(100, 100), center=(250, 400), name='DISCO', group=None):
        super().__init__(group)
        self.screen_rect = screen_rect
        self.name = name
        self.high_res_surface = pygame.image.load(os.path.join(ICONS_DIR, f'{self.name}.png'))
        self.surface = pygame.transform.scale(self.high_res_surface, self.screen_rect)
        self.center = center
        self.rect = self.surface.get_rect(center=self.center)
