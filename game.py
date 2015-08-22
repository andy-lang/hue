import pygame
from objects import *
import glob

class Game:
	"""Main game logic"""

	def __init__(self, width = 600, height = 600):
		pygame.init()

		#initilise wall object container
		self.walls = pygame.sprite.Group()

		# Set background to white
		self.bg = (255,255,255)

		#Load all maps into a map array
		self.maps = glob.glob('./maps/*.txt')

		self.width = width
		self.height = height

		#Set screen to users screen size
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.screen.fill(self.bg)

		pygame.display.set_caption('Hue')
		pygame.mouse.set_visible(0)

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
				obj = line.split( )

				if(obj[0] == "WB"):
					wall = Wall([obj[1], obj[2]], "./sprites/WB.png")
					self.walls.add(wall)
				elif(obj[0] == "WT1"):
					wall = Wall([obj[1], obj[2]], "./sprites/WT1.png")
					self.walls.add(wall)
				elif(obj[0] == "WT2"):
					wall = Wall([obj[1], obj[2]], "./sprites/WT2.png")
					self.walls.add(wall)
				elif(obj[0] == "WT3"):
					wall = Wall([obj[1], obj[2]], "./sprites/WT3.png")
					self.walls.add(wall)
				elif(obj[0] == "WT4"):
					wall = Wall([obj[1], obj[2]], "./sprites/WT4.png")
					self.walls.add(wall)

				wall.rect.x = int(obj[1])
				wall.rect.y = int(obj[2])
			pass
		except Exception, e:
			raise e

	def main(self):
		self.loadMap("./maps/map1.txt")
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

			#Draw map
			self.walls.draw(self.screen)
			
			pygame.draw.circle(self.screen, (255,0,0), (self.hugh.x, self.hugh.y), self.hugh.radius)

			pygame.display.flip()
			self.clock.tick(self.framerate)
	
	
window = Game()
window.main()
