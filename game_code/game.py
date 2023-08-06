import pygame
from random import randint
from game_code.constants import *
from pytmx.util_pygame import load_pygame
from game_code.camera import Camera
from game_code.farm.soil import SoilLayer
from game_code.gui.shop_menu import Shop
from game_code.sprites.particle_effect import ParticleEffect
from game_code.utils.transition import Transition
from game_code.utils.utils import Utils

from game_code.sprites.basic_sprite import BasicSprite, Interaction
from game_code.sprites.water import Water
from game_code.sprites.wild_plant import WildPlant
from game_code.sprites.bush import Bush
from game_code.sprites.overlay import Overlay
from game_code.player import Player
from game_code.weather import *

class Game:

    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        # sprite groups
        self.all_sprites = Camera()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_bush_sprites = pygame.sprite.Group()
        self.interaction_sprites = pygame.sprite.Group()

        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)

        # setup
        self.load_map()
        self.overlayer = Overlay(self.player)
        self.night_transition = Transition(self.restart_day, self.player)

        # weather
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0, 10) > 2
        self.soil_layer.raining = self.raining
        self.sky = Sky()

        # shop
        self.shop_menu = Shop(self.player, self.shop)
        self.shop_open = False


    def load_map(self):
        tmx = load_pygame('game_map/attempt2/map.tmx')

        # water layer
        water_animations = Utils.folder_to_surf_list('assets/images/water')
        scaled_water = []
        for animation in water_animations:
            scaled_water.append(pygame.transform.scale(animation, IMG_SIZE))
            
        for x, y, surf in tmx.get_layer_by_name('Water').tiles():
            Water((x * TILESIZE, y * TILESIZE), water_animations, self.all_sprites)

        # wild plants
        for obj in tmx.get_layer_by_name('Wildlife'):
            WildPlant((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # harvestable bushes and trees
        for obj in tmx.get_layer_by_name('HarvestableWildlife'):
            Bush(
                pos = (obj.x, obj.y),
                surf = obj.image,
                groups = [self.all_sprites, self.collision_sprites, self.tree_bush_sprites],
                name = obj.name,
                update_inventory_func = self.update_inventory_func
            )
        
        # regular trees
        for obj in tmx.get_layer_by_name('Forrest'):
            BasicSprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

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
                    interaction_sprites = self.interaction_sprites,
                    soil_layer = self.soil_layer,
                    shop = self.shop
                )

            if obj.name == 'WelcomeMat':
                Interaction(
					pos = (obj.x, obj.y),
					size = (obj.width, obj.height),
					groups = self.interaction_sprites,
					name = obj.name
				)

            if obj.name == 'WelcomeRug':
                BasicSprite((obj.x, obj.y), obj.image, self.all_sprites)


            if obj.name == 'House':
                BasicSprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])


            if obj.name == 'ShopKeeper':
                Interaction(
					pos = (obj.x, obj.y),
					size = (obj.width, obj.height),
					groups = self.interaction_sprites,
					name = 'ShopKeeper'
				)

            if obj.name == 'Keeper':
                BasicSprite((obj.x, obj.y), obj.image, [self.all_sprites, self.collision_sprites])

        # map 'floor'
        BasicSprite(
            pos = (0, 0),
            surface = pygame.image.load('game_map/attempt2/ground.png').convert_alpha(),
            groups = self.all_sprites,
            layer = LAYERS['earth']
        )

    
    def shop(self):
        self.shop_open = not self.shop_open

    def wild_plant_collisions(self):
        if self.soil_layer.herb_sprites:
            for herb in self.soil_layer.herb_sprites.sprites():
                if herb.harvestable and herb.rect.colliderect(self.player.hitbox):
                    # remove herb if player collides with it
                    self.update_inventory_func(herb.herb_type)
                    herb.kill()

                    # particle effect
                    ParticleEffect(herb.rect.topleft, herb.image, self.all_sprites, LAYERS['player'])

                    # claning up
                    row = herb.rect.centery // TILESIZE
                    col = herb.rect.centerx // TILESIZE
                    self.soil_layer.grid[row][col].remove('H')

    
    def update_inventory_func(self, item):
        self.player.full_inventory[item] += 1
        if item in self.player.herb_inventory.keys(): self.player.herb_inventory[item] += 1
        if item in self.player.item_inventory.keys(): self.player.item_inventory[item] += 1


    def restart_day(self):
        # herbs & soil
        self.soil_layer.update_herbs()
        self.soil_layer.clear_water()

        # rain
        self.raining = randint(0, 10) > 2
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

        # trees and bushes
        for bush in self.tree_bush_sprites.sprites():
            bush_sprites = bush.drop_sprites.sprites()
            # remove old drops
            if bush_sprites:
                for drop in bush_sprites:
                    drop.kill()
            # add new drops
            bush.add_bush_items()

        # sky
        self.sky.day = [255, 255, 255]


    def run(self, dt):
        """Runs the game with frame-independence (hence dt -- deltatime)"""

        # drawing sprites
        self.display_surface.fill('black')
        self.all_sprites.custom_draw(self.player)

        if self.shop_open:
            self.shop_menu.update()
        else:
            self.all_sprites.update(dt)
            self.wild_plant_collisions()

        self.overlayer.display()

        # rain
        if self.raining: self.rain.update()
        
        # day/night cycle
        self.sky.display(dt)
        if self.player.sleeping:
            self.night_transition.run()

