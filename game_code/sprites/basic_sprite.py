import pygame
from game_code.constants import *


class BasicSprite(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, layer = LAYERS['player']):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.2)
        self._layer = layer



class Interaction(BasicSprite):
    def __init__(self, pos, size, groups, name):
        surf = pygame.Surface(size) # not concerned with actually seeing this surface
        super().__init__(pos, surf, groups)
        self.name = name