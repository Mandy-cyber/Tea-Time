import pygame
from game_code.constants import *
from pytmx.util_pygame import load_pygame
from game_code.camera import Camera
from game_code.utils.utils import Utils

from game_code.sprites.basic_sprite import BasicSprite, Interaction
from game_code.sprites.water import Water
from game_code.sprites.wild_plant import WildPlant
from game_code.sprites.bush import Bush
from game_code.sprites.overlay import Overlay
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
        self.overlayer = Overlay(self.player)


    def load_map(self):
        tmx = load_pygame('game_map/map.tmx')

        # buildings layer
        for obj in tmx.get_layer_by_name('Buildings'):
            BasicSprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # water layer
        water_animations = Utils.folder_to_surf_list('assets/images/water')
        for x, y, surf in tmx.get_layer_by_name('Water').tiles():
            Water((x * TILESIZE, y * TILESIZE), water_animations, self.all_sprites)

        # wild plants
        for x, y, surf in tmx.get_layer_by_name('WildPlants').tiles():
            WildPlant((x * TILESIZE, y * TILESIZE), surf, [self.all_sprites, self.collision_sprites])

        # bushes and trees
        for obj in tmx.get_layer_by_name('Trees'):
            if obj.name == None: # aka regular background trees
                BasicSprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])
            else: # actually useful trees and bushes
                Bush(
                    pos = (obj.x, obj.y),
                    surf = obj.image,
                    groups = [self.all_sprites, self.collision_sprites, self.tree_bush_sprites],
                    name = obj.name,
                    update_inventory_func = self.update_inventory_func
                )

        # borders
        for x, y, surf in tmx.get_layer_by_name('Borders').tiles():
            BasicSprite((x * TILESIZE, y * TILESIZE), pygame.Surface((TILESIZE, TILESIZE)), self.collision_sprites) 


        # player layer
        for obj in tmx.get_layer_by_name('Player'):

            if obj.name == 'Start':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    group = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    tree_bush_sprites = self.tree_bush_sprites,
                    interaction_sprites = self.interaction_sprites
                    # TODO: add soil layer and shop toggle
                )

            if obj.name == 'WelcomeMat':
                Interaction(
					pos = (obj.x, obj.y),
					size = (obj.width, obj.height),
					groups = self.interaction_sprites,
					name = obj.name
				)

            if obj.name == 'ShopKeeper' or obj.name == 'ShopKeeperTile':
                Interaction(
					pos = (obj.x, obj.y),
					size = (obj.width, obj.height),
					groups = self.interaction_sprites,
					name = 'ShopKeeper'
				)

        # map 'floor'
        BasicSprite(
            pos = (0, 0),
            surface = pygame.image.load('game_map/ground.png').convert_alpha(),
            groups = self.all_sprites,
            layer = LAYERS['earth']
        )
            


    
    def update_inventory_func(self, item):
        self.player.item_inventory[item] += 1


    def run(self, dt):
        """Runs the game with frame-independence (hence dt -- deltatime)"""

        # drawing sprites
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)

        self.all_sprites.update(dt)

        self.overlayer.display()


