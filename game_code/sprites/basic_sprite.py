import pygame
from ..constants import *

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surface, groups, layer = LAYERS['player']):
        super().__init__(groups)

        self.image = surface
        self.rect = self.image.get_rect(topleft = pos)
        # self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.2)
        self._layer = layer