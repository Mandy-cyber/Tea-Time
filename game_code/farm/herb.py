import pygame
from game_code.constants import *
from game_code.utils.utils import Utils
from pytmx.util_pygame import load_pygame
from random import choice


class Herb(pygame.sprite.Sprite):
    def __init__(self, herb_type, groups, soil, check_watered):
        super().__init__(groups)
        # setup
        self.herb_type = herb_type
        self.frames = Utils.folder_to_surf_list(f'assets/images/herbs/{herb_type}')
        self.soil = soil
        self.was_watered = check_watered

        # aging/growing
        self.age = 0
        self.harvest_age = len(self.frames) - 1
        self.grow_speed = GROW_SPEED[herb_type]
        self.harvestable = False

        # sprite setup
        self.image = pygame.transform.scale(self.frames[self.age], IMG_SIZE)
        self.y_offset = -10
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))
        self.z = LAYERS['herb_plant']


    def grow(self):
        if self.was_watered(self.rect.center):
            self.age += self.grow_speed

            # old enough to collide with
            if int(self.age) > 0:
                self.z = LAYERS['player']
                self.hitbox = self.rect.copy().inflate(-26, -self.rect.height * 0.4)

            # old enough to harvest
            if self.age >= self.harvest_age:
                self.age = self.harvest_age
                self.harvestable = True

            self.image = self.frames[int(self.age)]
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0, self.y_offset))