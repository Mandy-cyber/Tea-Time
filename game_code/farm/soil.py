import pygame
from game_code.constants import *
from game_code.farm.herb import Herb
from game_code.sprites.water import WaterTile
from game_code.utils.utils import Utils
from pytmx.util_pygame import load_pygame
from random import choice


class Soil(pygame.sprite.Sprite):
    def __init__(self, pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS['soil']



class SoilLayer:
    def __init__(self, all_sprites, collision_sprites):
        # groups
        self.all_sprites = all_sprites
        self.collision_sprites = collision_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()
        self.herb_sprites = pygame.sprite.Group()

        # assets
        self.soil_surfs = Utils.folder_to_surf_dict('assets/images/soil')
        self.water_surfs = Utils.folder_to_surf_list('assets/graphics/wet_soil')

        self.create_soil_grid()
        self.generate_hitboxes()
        

    def create_soil_grid(self):
        ground = pygame.image.load('game_map/ground.png')
        h_tiles, v_tiles = ground.get_width() // TILESIZE, ground.get_height() // TILESIZE
        
        self.grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, __ in load_pygame('game_map/map.tmx').get_layer_by_name('FarmLand').tiles():
            self.grid[y][x].append('F')

    
    def generate_hitboxes(self):
        self.hit_rects = []
        for y_idx, row in enumerate(self.grid):
            for x_idx, cell in enumerate(row):
                if 'F' in cell:
                    x = x_idx * TILESIZE
                    y = y_idx * TILESIZE
                    rect = pygame.Rect(x, y, TILESIZE, TILESIZE)
                    self.hit_rects.append(rect)


    def hit_soil(self, point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                x = rect.x // TILESIZE
                y = rect.y // TILESIZE
                grid_spot = self.grid[y][x]

                if 'F' in grid_spot:
                    grid_spot.append('X')
                    self.create_soil_tiles()
                    if self.raining:
                        self.water_all()


    def water_soil(self, target_pos):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILESIZE
                y = soil_sprite.rect.y // TILESIZE
                self.grid[y][x].append('W')
                
                WaterTile(
                    pos = soil_sprite.rect.topleft,
                    surf = choice(self.water_surfs),
                    groups = [self.all_sprites, self.water_sprites]
                )


    def water_all(self):
        for y_idx, row in enumerate(self.grid):
            for x_idx, cell in enumerate(row):
                if 'X' in cell and 'W' not in cell:
                    cell.append('W')
                    x = x_idx * TILESIZE
                    y = y_idx * TILESIZE
                    WaterTile((x, y), choice(self.water_surfs), [self.all_sprites, self.water_sprites])


    def clear_water(self):
        # removing water tiles
        for water_sprite in self.water_sprites.sprites():
            water_sprite.kill()

        # removing water tiles from grid
        for row in self.grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')


    def is_watered(self, pos):
        x = pos[0] // TILESIZE
        y = pos[1] // TILESIZE
        cell = self.grid[y][x]
        is_watered = 'W' in cell
        return is_watered
    

    def plant_herb(self, target_pos, herb):
        for soil_sprite in self.soil_sprites.sprites():
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILESIZE
                y = soil_sprite.rect.y // TILESIZE
                grid_spot = self.grid[y][x]

                if 'H' not in grid_spot:
                    grid_spot.append('H')
                    Herb(
                        herb_type = herb,
                        groups = [self.all_sprites, self.herb_sprites, self.collision_sprites],
                        soil = soil_sprite,
                        check_watered = self.is_watered
                    )


    def update_herbs(self):
        for herb in self.herb_sprites.sprites():
            herb.grow()


    def gen_soil_tiles(self):
        self.soil_sprites.empty()
        for y_idx, row in enumerate(self.grid):
            for x_idx, cell in enumerate(row):
                if 'X' in cell:

                    # tile options (check what tiles are in the diff directions)
                    top = 'X' in self.grid[y_idx - 1][x_idx]
                    bottom = 'X' in self.grid[y_idx + 1][x_idx]
                    right = 'X' in row[x_idx + 1]
                    left = 'X' in row[x_idx - 1]
                    tile_type = 'o' # default tile type

                    # all sides
                    if all((top, bottom, right, left)): tile_type = 'x'

                    # horizontal tiles only
                    if left and not any((top, right, bottom)): tile_type = 'r'
                    if right and not any((top, left, bottom)): tile_type = 'l'
                    if left and right and not any((top, bottom)): tile_type = 'lr'

                    # vertical tiles only
                    if top and not any((bottom, left, right)): tile_type = 'b'
                    if bottom and not any((top, left, right)): tile_type = 't'
                    if top and bottom and not any((left, right)): tile_type = 'tb'

                    # corners
                    if left and bottom and not any((top, right)): tile_type = 'tr'
                    if right and bottom and not any((top, left)): tile_type = 'tl'
                    if left and top and not any((bottom, right)): tile_type = 'br'
                    if right and top and not any((bottom, left)): tile_type = 'bl'

                    # t-shapes
                    if all((top, bottom, right)) and not left: tile_type = 'tbr'
                    if all((top, bottom, left)) and not right: tile_type = 'tbl'
                    if all((top, left, right)) and not bottom: tile_type = 'lrb'
                    if all((bottom, left, right)) and not top: tile_type = 'lrt'

                    Soil(
                        pos = (x_idx * TILESIZE, y_idx * TILESIZE), 
                        surf = self.soil_surfs[tile_type], 
                        groups = [self.all_sprites, self.soil_sprites]
                    )