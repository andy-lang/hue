import pygame
import glob

class Game:
	"""Main game logic"""

	def __init__(self, width = 800, height = 600):
		pygame.init()

		infoObject = pygame.display.Info()

		#Get user screen width and height
		self.width = infoObject.current_w
		self.height = infoObject.current_h

		#Load all maps into a map array
		self.maps = glob.glob('./maps/*.txt')

		#Set screen to users screen size
		self.screen = pygame.display.set_mode((800, 600))
		pygame.display.set_caption('Hue')

		self.running = True
		self.framerate = 20

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

		pygame.display.flip()

		self.clock.tick(self.framerate)


window = Game()
window.main()