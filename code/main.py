import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):

		# general setup
		pygame.init()	
		self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
		pygame.display.set_icon(GAME_ICON)
		pygame.display.set_caption('Naruto')
		self.clock = pygame.time.Clock()
		#create level
		self.level = Level()
	def run(self):
		while True:
			for event in pygame.event.get():
				#out game mouse
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
			#reset game
			if game.level.player.accept_reset:
					#stop lose game sound
					if(game.level.player.lose == True) :
						self.level.lose_sound.stop()
					#stop win game sound
					if(game.level.player.win == True) :
						self.level.win_sound.stop()
					#cook level	
					self.level = ()
					#init again
					self.level = Level()
			#out game keyboard
			if game.level.player.out_game == True:
				pygame.quit()
				sys.exit()
			#run game
			self.screen.fill('black')
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()
