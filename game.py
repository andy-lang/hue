import pygame
from objects import *
import glob

class Game:
	"""Main game logic"""

	def __init__(self, width = 600, height = 600):
		pygame.init()

		#Load all maps into a map array
		self.maps = glob.glob('./maps/*.txt')

		self.width = width
		self.height = height

		#Set screen to users screen size
		self.screen = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption('Hue')

		self.running = True # game will enter loop
		self.framerate = 30
		self.clock = pygame.time.Clock() # timer
		pygame.key.set_repeat(self.framerate) # keypresses hold

		self.hugh = Hugh(self.width/2, self.height/2)

		

	def loadMap(self, fileName):
		try:
			#Open map file
			f = open(fileName, 'r')
			for line in f:
				print line
			pass
		except Exception, e:
			raise e

	def main(self):
		while self.running:

			for event in pygame.event.get():
				# events go here
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					self.hugh.move(event.key)

				
			

			self.screen.fill((0,0,0))
			pygame.draw.circle(self.screen, (255,0,0), (self.hugh.x, self.hugh.y), self.hugh.radius)

			pygame.display.flip()
			self.clock.tick(self.framerate)
	
	
window = Game()
window.main()
