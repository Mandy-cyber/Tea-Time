import pygame
from game_code.constants import *
from pytmx.util_pygame import load_pygame
from game_code.camera import Camera
from game_code.sprites.basic_sprite import Generic
from game_code.player import Player

class Game:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = Camera()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_bush_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        # setup
        self.load_map()


    def load_map(self):
        tmx = load_pygame('game_map/map.tmx')

        # buildings layer
        

        # FOR NOW
        # Generic(
        #     pos = (0,0),
        #     surface = pygame.image.load('../game_map/map.png'),
        #     groups = self.all_sprites,
        #     z = LAYERS['player']
        # )

        self.player = Player(
            pos = (500, 500),
            group = self.all_sprites,
            collision_sprites = self.collision_sprites,
            tree_bush_sprites = self.tree_bush_sprites,
            interaction_sprites = self.interaction_sprites
        )


    def run(self, dt):
        """Runs the game with frame-independence (hence dt -- deltatime)"""
        
        # drawing sprites
        # ground = pygame.image.load('game_map/map.png')
        # width, height = ground.get_size()
        # surface = pygame.transform.scale(ground, (width // 2, height // 2))
        # surface_rect = surface.get_rect()

        # self.display_surface.blit(surface, surface_rect)
        # # self.display_surface.fill('black')
        # self.all_sprites.custom_draw(self.player)

        # self.all_sprites.update(dt)

        self.display_surface.fill('black')
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)


