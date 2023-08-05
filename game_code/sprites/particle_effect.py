import pygame
from game_code.sprites.basic_sprite import BasicSprite
from game_code.constants import *


class ParticleEffect(BasicSprite):
    def __init__(self, pos, surf, groups, layer, duration=150):
        super().__init__(pos, surf, groups, layer)
        self.start_time = pygame.time.get_ticks()
        self.duration = duration

        # white surface
        mask_surf = pygame.mask.from_surface(self.image)
        new_surf = mask_surf.to_surface()
        new_surf.set_colorkey((0,0,0))
        self.image = new_surf
    

    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_time > self.duration:
            self.kill()
