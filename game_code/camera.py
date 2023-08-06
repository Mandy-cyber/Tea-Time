import pygame
from game_code.constants import *

class Camera(pygame.sprite.Group):

	def __init__(self):
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.offset = pygame.math.Vector2()


	def custom_draw(self, player):
		# shifting to make it look like a camera
		self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
		self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

		# draw layers in correct order
		for layer_idx in LAYERS.values():
			for sprite in self.sprites():
				if sprite.z == layer_idx:
					offset_rect = sprite.rect.copy()
					offset_rect.center -= self.offset
					self.display_surface.blit(sprite.image, offset_rect)