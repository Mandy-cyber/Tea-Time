import pygame, sys
from game_code.game import Game
from game_code.utils.constants import *


class TeaTime:
	def __init__(self):
		pygame.init()
		self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
		pygame.display.set_caption('Tea Time')
		self.clock = pygame.time.Clock()
		self.game = Game()

	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

			dt = self.clock.tick() / 1000
			self.level.run(dt)
			pygame.display.update()



if __name__ == '__main__':
	game = TeaTime()
	game.run()
