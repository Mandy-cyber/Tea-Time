import pygame
from game_code.constants import *
from game_code.utils.utils import Utils
from game_code.sprites.basic_sprite import BasicSprite
from random import randint, choice


class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.day = [255, 255, 255]
        self.night = (55, 65, 69)

    
    def display(self, dt):
        # changing sky color
        for idx, value in enumerate(self.night):
            if self.day[idx] > value:
                self.day[idx] -= 0.5 * dt

        # displaying change in sky color
        self.full_surf.fill(self.day)
        self.display_surface.blit(self.full_surf, (0,0), special_flags=pygame.BLEND_RGBA_MULT)



#----------------------------------------------------------------------------------------------


class RainDrop(BasicSprite):
    def __init__(self, pos, surf, groups, moving, z):
        super().__init__(pos, surf, groups, z)

        # time
        self.duration = randint(300, 550)
        self.start_time = pygame.time.get_ticks()

        # 'movement'
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2, 4)
            self.speed = randint(200, 250)


    def update(self, dt):
        # moving rain drops
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = (round(self.pos.x), round(self.pos.y))

        # updating time
        if pygame.time.get_ticks() - self.start_time > self.duration:
            self.kill()



#----------------------------------------------------------------------------------------------


class Rain:
    def __init__(self, all_sprites):
        self.all_sprites = all_sprites
        self.rain_drops = Utils.folder_to_surf_list('assets/images/rain/drops')
        self.rain_floor = Utils.folder_to_surf_list('assets/images/rain/floor')
        self.floor_w, self.floor_h = pygame.image.load('game_map/attempt2/ground.png').get_size()

    
    def create_floor(self):
        RainDrop(
            pos = (randint(0, self.floor_w), randint(0, self.floor_h)),
            surf = pygame.transform.scale(choice(self.rain_floor), (32, 32)),
            groups = self.all_sprites,
            moving = False,
            z = LAYERS['ground_rain']
        )

    def create_drops(self):
        RainDrop(
            pos = (randint(0, self.floor_w), randint(0, self.floor_h)),
            surf = pygame.transform.scale(choice(self.rain_drops), (48, 48)),
            groups = self.all_sprites,
            moving = True,
            z = LAYERS['rain_drops']
        )


    def update(self):
        self.create_floor()
        self.create_drops()