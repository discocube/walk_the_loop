"""
Icons for game. Not game pieces.
"""
import pygame


class Icon(pygame.sprite.Sprite):
    """
    small icon.
    """
    def __init__(self, screen_rect=(100, 100), center=(900, 100), name='DISCO', group=None):
        super().__init__(group)
        self.screen_rect = screen_rect
        self.name = name
        self.high_res_surface = pygame.image.load(f'/home/rommelo/Repos/walk_the_loop/game/icons/{self.name}_s.png')
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
        self.high_res_surface = pygame.image.load(f'/home/rommelo/Repos/walk_the_loop/game/icons/{self.name}.png')
        self.surface = pygame.transform.scale(self.high_res_surface, self.screen_rect)
        self.center = center
        self.rect = self.surface.get_rect(center=self.center)
