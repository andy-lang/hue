import pygame

class Game:
	"""Main game logic"""

	def __init__(self, width = 800, height = 600):
		self.width = width
		self.height = height

		self.screen = pygame.display.set_mode((width,height))
		pygame.display.set_caption('Hue')

		self.running = True
		self.framerate = 20

	def main(self):
		while self.running:
			for event in pygame.event.get():
				# events go here
				if event.type == pygame.QUIT:
					self.running = False

		pygame.display.flip()

		self.clock.tick(self.framerate)
	
	
window = Game()
window.main()
