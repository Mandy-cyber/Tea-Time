import pygame
from game_code.constants import *
from game_code.utils.utils import Utils
from game_code.utils.game_timer import GameTimer
from random import choice


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group, collision_sprites, tree_bush_sprites, interaction_sprites, soil_layer):
        super().__init__(group)

        # character images and animation assets
        self.load_assets()
        self.player_state = 'down_idle'
        self.state_index = 0

        # general
        self.image = self.animations[self.player_state][self.state_index]
        self.rect = self.image.get_rect(center = pos)
        self.z = LAYERS['player']
        self.sleeping = False

        # movement
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = PLAYER_SPEED

        # collisions + interactions
        self.collision_sprites = collision_sprites
        self.hitbox = self.rect.copy().inflate((-126, -70))
        self.tree_bush_sprites = tree_bush_sprites
        self.interaction_sprites = interaction_sprites
        self.soil_layer = soil_layer

        # tools
        self.tools = ['shears', 'hoe', 'water']
        self.tool_index = 0
        self.current_tool = self.tools[self.tool_index]

        # herbs
        self.herbs = ['lavender', 'chamomile', 'hibiscus', 'basil']
        self.herb_index = 0
        self.current_herb = self.herbs[self.herb_index]

        # other items
        self.items = ['glass_bottle', 'journal']
        self.item_index = 0
        self.current_item = self.items[self.item_index]

        # timers
        self.timers = {
            'use_tool': GameTimer(300, self.use_tool),
            'change_tool': GameTimer(200),
            'use_herb': GameTimer(300, self.plant_herb),
            'change_herb': GameTimer(200),
            'use_item': GameTimer(300, self.use_item),
            'change_item': GameTimer(200)
        }

        # currency (aka hearts)
        self.hearts = 100

        # inventories
        self.full_inventory = {
            'lavender': 0,
            'chamomile': 0,
            'hibiscus': 0,
            'basil': 0,
            'glass_bottle': 0,
            'journal': 0,
            'lavender_tea': 0,
            'chamomile_tea': 0,
            'hibiscus_tea': 0,
            'basil_tea': 0
        }

        self.herb_inventory = {
            'lavender': 10,
            'chamomile': 10,
            'hibiscus': 10,
            'basil': 10
        }

        self.tea_inventory = {
            'lavender_tea': 0,
            'chamomile_tea': 0,
            'hibiscus_tea': 0,
            'basil_tea': 0
        }

        self.item_inventory = {
            'glass_bottle': 0,
            'journal': 0
        }



    def load_assets(self):
        self.animations = {
            'up': [], 'down': [], 'left': [], 'right': [],
            'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [],
            'right_hoe': [], 'left_hoe': [], 'up_hoe': [], 'down_hoe': [],
            'right_shears': [], 'left_shears': [], 'up_shears': [], 'down_shears': [],
            'right_water': [], 'left_water': [], 'up_water': [], 'down_water': []
        }

        for animation_name in self.animations.keys():
            animation_path = 'assets/images/player/' + animation_name
            image_surfs = Utils.folder_to_surf_list(animation_path)
            scaled_image_surfs = [pygame.transform.scale(image, IMG_SIZE) for image in image_surfs]
            self.animations[animation_name] = scaled_image_surfs


    def use_tool(self):
        if self.current_tool == 'hoe':
            self.soil_layer.hit_soil(self.target_pos)

        elif self.current_tool == 'shears':
            for bush in self.tree_bush_sprites.sprites():
                if bush.rect.collidepoint(self.target_pos):
                    bush.damage()

        elif self.current_tool == 'water':
            self.soil_layer.water_soil(self.target_pos)


    def plant_herb(self):
        if self.herb_inventory[self.current_herb] > 0:
            self.soil_layer.plant_herb(self.target_pos, self.current_herb)
            self.herb_inventory[self.current_herb] -= 1


    def use_item(self):
        if self.current_item == 'journal':
            print(choice(AFFIRMATIONS))


    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['use_tool'].active and not self.sleeping:

            # MOVEMENT INPUT
            #----------------------
            # vertical
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.direction.y = -1
                self.player_state = 'up'
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.direction.y = 1
                self.player_state = 'down'
            else:
                self.direction.y = 0

            # horizontal
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.direction.x = -1
                self.player_state = 'left'
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.direction.x = 1
                self.player_state = 'right'
            else:
                self.direction.x = 0


            # TOOL INPUT
            #----------------------
            # change tool
            if keys[pygame.K_1]:
                self.timers['change_tool'].activate()
                self.change_tool()

            # use tool
            elif keys[pygame.K_t]:
                self.timers['use_tool'].activate()
                self.direction = pygame.math.Vector2()
                self.state_index = 0

            
            # HERB INPUT
            #----------------------
            # change herb
            if keys[pygame.K_2]:
                self.timers['change_herb'].activate()
                self.change_herb()

            # plant herb
            elif keys[pygame.K_q]:
                self.timers['use_herb'].activate()
                self.direction = pygame.math.Vector2()
                self.state_index = 0

            
            # ITEM INPUT (e.g. bottle)
            #--------------------------
            # change item
            if keys[pygame.K_3]:
                self.timers['change_item'].activate()
                self.change_item()

            # use item
            if keys[pygame.K_l]:
                self.timers['use_item'].activate()
                self.direction = pygame.math.Vector2()
                self.state_index = 0


    def get_target_pos(self):
        self.target_pos = self.rect.center + TOOL_OFFSET[self.player_state.split('_')[0]]


    def change_tool(self):
        self.tool_index += 1
        self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
        self.current_tool = self.tools[self.tool_index]

    
    def change_herb(self):
        self.herb_index += 1
        self.herb_index = self.herb_index if self.herb_index < len(self.herbs) else 0
        self.current_herb = self.herbs[self.herb_index]

    
    def change_item(self):
        self.item_index += 1
        self.item_index = self.item_index if self.item_index < len(self.items) else 0
        self.current_item = self.items[self.item_index]


    def animate(self, dt):
        self.state_index += 4 * dt

        if self.state_index >= len(self.animations[self.player_state]): self.state_index = 0
        self.image = self.animations[self.player_state][int(self.state_index)]


    def change_player_state(self):
        # stationary (i.e. idle)
        if self.direction.magnitude() == 0:
            self.player_state = self.player_state.split('_')[0] + '_idle'

        # tool use
        if self.timers['use_tool'].active:
            self.player_state = self.player_state.split('_')[0] + '_' + self.current_tool


    def move(self, dt):
        # normalizing so diagonals aren't faster moving than other directions
        if self.direction.magnitude() > 0: # can't normalize vector of length lte 0
            self.direction = self.direction.normalize()

        # horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.hitbox.centerx = round(self.pos.x)
        self.rect.centerx = self.hitbox.centerx
        # self.collide('h)

        # vertical movement
        self.pos.y += self.direction.y * self.speed * dt
        self.hitbox.centery = round(self.pos.y)
        self.rect.centery = self.hitbox.centery
        # self.collide('v')


    def update_timers(self):
        for timer in self.timers.values():
            timer.update()


    def update(self, dt):
        self.input()
        self.change_player_state()
        self.update_timers()
        self.get_target_pos()
        self.move(dt)
        self.animate(dt)



