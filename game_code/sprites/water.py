from game_code.sprites.basic_sprite import BasicSprite
from ..constants import *

class Water(BasicSprite):
    def __init__(self, pos, animation_frames, groups):
        self.frames = animation_frames
        self.frame_index = 0
        super().__init__(pos, self.frames[self.frame_index], groups, LAYERS['water'])


    def animate(self, dt):
        self.frame_index += 7 * dt
        if self.frame_index >= len(self.frames): self.frame_index = 0
        self.image = self.frames[int(self.frame_index)] # bc frame index can be a decimal

    
    def update(self, dt):
        self.animate(dt)