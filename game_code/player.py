import pygame
from game_code.constants import *
from game_code.utils.utils import Utils


class Player(pygame.sprite.Sprite):

    def __init__(self, pos, group, collision_sprites, tree_bush_sprites, interaction_sprites):
        super().__init__(group)

        # character images and animation assets
        self.load_assets()
        self.player_state = 'down_idle'
        self.state_index = 0

        # general
        self.image = self.animations[self.player_state][self.state_index]
        self.rect = self.image.get_rect(center = pos)
        self._layer = LAYERS['player']
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

        # tools
        self.tools = ['shears', 'hoe', 'water']
        self.tool_index = 0
        self.current_tool = self.tools[self.tool_index]

        # herbs
        self.herbs = ['lavender', 'chamomile', 'hibiscus', 'basil']
        self.herb_index = 0
        self.current_herb = self.herbs[self.herb_index]


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
            self.animations[animation_name] = Utils.folder_to_surf_list(animation_path)


    def input(self):
        keys = pygame.key.get_pressed()

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


    def animate(self, dt):
        self.state_index += 4 * dt

        if self.state_index >= len(self.animations[self.player_state]): self.state_index = 0
        self.image = self.animations[self.player_state][int(self.state_index)]


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


    def update(self, dt):
        self.input()
        self.move(dt)
        self.animate(dt)