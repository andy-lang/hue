import pygame
from objects import *
import glob

class Game:
	"""Main game logic"""

	def __init__(self, width = 800, height = 600):
		pygame.init()

		infoObject = pygame.display.Info()

		#Get user screen width and height
		self.width = infoObject.current_w
		self.height = infoObject.current_h

		# Set background to white
		self.bg = (255,255,255)

		#Load all maps into a map array
		self.maps = glob.glob('./maps/*.txt')

		#Set screen to users screen size
		self.screen = pygame.display.set_mode((800, 600))
		self.screen.fill(self.bg)
		pygame.display.set_caption('Hue')

		self.running = True # game will enter loop
		self.framerate = 30
		self.clock = pygame.time.Clock() # timer
		pygame.key.set_repeat(self.framerate) # keypresses hold

		self.hugh = Hugh(self.screen, self.width/2, self.height/2)

		

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

			keys = pygame.key.get_pressed()
			self.hugh.move(keys)
			for event in pygame.event.get():
				# events go here
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.running = False
						
				# elif event.type == pygame.KEYDOWN:
				# 	self.hugh.move(event.key)

				
			

			self.screen.fill(self.bg)
			
			# draw Hugh
			self.hugh.draw()

			pygame.display.flip()
			self.clock.tick(self.framerate)
	
	
window = Game()
window.main()
