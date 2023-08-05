from game_code.sprites.basic_sprite import BasicSprite
from ..constants import *

class WildPlant(BasicSprite):
    def __init__(self, pos, surf, groups):
        super().__init__(pos, surf, groups, LAYERS['player'])
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)