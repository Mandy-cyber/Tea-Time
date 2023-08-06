import pygame
from game_code.constants import *

class Transition:
    def __init__(self, reset_func, player):
        # setup
        self.display_surface = pygame.display.get_surface()
        self.reset = reset_func
        self.player = player

        # overlay image
        self.image = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.color = 255
        self.speed = -0.5

    
    def run(self):
        self.color += self.speed
        if self.color <= 0:
            # 1. reset game
            self.speed *= -1
            self.color = 0
            self.reset()
        elif self.color > 255:
            # 2. wake up player
            self.color = 255
            self.player.sleep = False
            self.speed = -0.5

        self.image.fill((self.color, self.color, self.color))
        self.display_surface.blit(self.image, (0,0), special_flags=pygame.BLEND_RGBA_MULT)