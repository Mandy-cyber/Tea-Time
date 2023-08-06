from game_code.sprites.particle_effect import ParticleEffect
import pygame
from game_code.sprites.basic_sprite import BasicSprite
from game_code.constants import *
from random import choice, randint

class Bush(BasicSprite):
    """represents hibiscus trees, basil bushes, and lavender/chamomile bushes"""

    def __init__(self, pos, surf, groups, name, update_inventory_func):
        super().__init__(pos, surf, groups)

        self.name = name
        if self.name == None: self.name = 'ChamomileBush'

        self.update_inventory = update_inventory_func
        self.alive = True

        # drops
        print(self.name)
        self.num_drops = randint(0, WILD_HERBS[self.name])
        self.drop_surf = self.get_drop_surf()
        
        if self.herb != 'basil':
            self.drop_positions = WILD_HERBS_POS[self.name]
            self.drop_sprites = pygame.sprite.Group()

        self.add_bush_items()


    def add_bush_items(self):
        # all herbs (except basil) have designated 'items' to be added to a plant
        if self.herb != 'basil':
            for pos in self.drop_positions:
                if randint(0, 10) < 3:
                    x = pos[0] + self.rect.left
                    y = pos[1] + self.rect.top

                    BasicSprite(
                        pos = (x, y),
                        surface = self.drop_surf,
                        groups = [self.drop_sprites, self.groups()[0]],
                        layer = LAYERS['bush_herbs']
                    )


    def get_drop_surf(self):
        """gets the correct image for this tree/bush to have on it"""
        if self.name == 'ChamomileBush':
            herb = 'chamomile'
        elif self.name == 'BasilBush':
            herb = 'basil'
        elif self.name == 'HibiscusTree':
            herb = 'hibiscus'
        elif self.name == 'LavenderBush':
            herb = 'lavender'
        
        self.herb = herb
        drop_surf = pygame.transform.scale(pygame.image.load(f'assets/images/overlays/{herb}.png'), IMG_SIZE)
        return drop_surf
    


    def damage(self):
        self.num_drops -= 1

        # remove drop
        if self.herb != 'basil':
            if len(self.drop_sprites.sprites()) > 0:
                # this next 2 lines i took right from the internet because i was having such a janky error xD
                sprites_without_particles = [
                    sprite for sprite in self.drop_sprites.sprites() if not isinstance(sprite, ParticleEffect)
                ]

                if sprites_without_particles:
                    drop = choice(sprites_without_particles)
                    ParticleEffect(
                        pos = drop.rect.topleft,
                        surf = drop.image,
                        groups = self.groups()[0],
                        layer = LAYERS['bush_herbs']
                    )
                    self.update_inventory(self.herb)
                    drop.kill()

        else:
            # TODO: maybe make custom particle effect for basil since no 'drops' given (?) 
            ParticleEffect(
                pos = self.rect.topleft,
                surf = self.image,
                groups = self.groups()[0],
                layer = LAYERS['bush_herbs'],
                duration = 100
            )



    def check_drops_left(self):
        if self.num_drops <= 0:
            ParticleEffect(
                pos = self.rect.topleft,
                surf = self.image,
                groups = self.groups()[0],
                layer = LAYERS['bush_herbs'],
                duration = 250
            )
        
        if self.herb == 'basil': self.image = pygame.transform.scale(pygame.image.load('assets/images/wild_plants/basil_bush_empty.png'), IMG_SIZE)
        self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
        self.alive = False


    def update(self, dt):
        if self.alive:
            self.check_drops_left()
        