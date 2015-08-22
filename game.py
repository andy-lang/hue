import pygame
from objects import *
import glob

class Game:
	"""Main game logic"""

	def __init__(self, width = 600, height = 600):
		# initialise pygame
		pygame.init()

		#initilise wall object container
		self.walls = pygame.sprite.Group()
		self.goals = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.all_sprites = pygame.sprite.Group()

		# Set background to white
		self.bg = (255,255,255)

		#Load all maps into a map array
		self.maps = glob.glob('./maps/*.txt')

		# set width and height of game screen
		self.width = width
		self.height = height

		#Set screen to users screen size
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.screen.fill(self.bg)
		self.maskScreen = MaskScreen(self.screen, self.width, self.height)

		# few more window options
		pygame.display.set_caption('Hue')
		pygame.mouse.set_visible(0)

		self.running = True # game will enter loop
		self.framerate = 30
		self.clock = pygame.time.Clock() # timer
		pygame.key.set_repeat(self.framerate) # keypresses hold

		self.hugh = Hugh(self.screen, self.width/2, self.height/2)

		
	# load a map file
	def loadMap(self, fileName):
		try:
			#Open map file
			f = open(fileName, 'r')
			for line in f:
				line = line.split( )

				if(line[0] == "C"):
					self.hugh.x = int(line[1])
					self.hugh.y = int(line[2])
				elif(line[0] == "WB"):
					obj = Object([line[1], line[2]], "./sprites/WB.png")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "WT1"):
					obj = Object([line[1], line[2]], "./sprites/WT1.png")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "WT2"):
					obj = Object([line[1], line[2]], "./sprites/WT2.png")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "WT3"):
					obj = Object([line[1], line[2]], "./sprites/WT3.png")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "WT4"):
					obj = Object([line[1], line[2]], "./sprites/WT4.png")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "G"):
					obj = Object([line[1], line[2]], "./sprites/end.png")
					self.goals.add(obj)
					self.all_sprites.add(obj)				
			pass
		except Exception, e:
			raise e

	def main(self):
		self.loadMap("./maps/map1.txt")
		while self.running:

			# pass all pressed keys to Hugh for processing
			keys = pygame.key.get_pressed()
			self.hugh.move(keys)

			for event in pygame.event.get():
				# press Exit button or ESC key
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.running = False

			self.screen.fill(self.bg)

			#Check object collisions
			for wall in self.walls:
				if(pygame.sprite.collide_mask(wall, self.hugh) != None):
					print "Collision"
					#self.hugh.collision()

			#Draw map
			self.all_sprites.draw(self.screen)

			# draw the masking screen
			self.maskScreen.draw(self.hugh)
			
			# draw Hugh
			self.hugh.draw()
			
			pygame.display.flip()
			self.clock.tick(self.framerate)
	
	
window = Game()
window.main()
