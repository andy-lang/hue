import pygame
from objects import *
import glob

class Music:
	"""Mixer for music depending on Hugh's location to enemies and goal"""

	def __init__(self, upperscreen):
		pygame.mixer.init()

		self.NEAR_MUSIC_MAX = 0.2
		self.FAR_MUSIC_MAX = 1.0
		self.nearMusic = pygame.mixer.Sound('sound/near.ogg')
		self.nearMusic.set_volume(0)

		self.farMusic = pygame.mixer.Sound('sound/far.ogg')
		self.farMusic.set_volume(0)

		# self.nearMusic.play(-1)
		self.farMusic.play(-1)

		self.maxDist = (upperscreen.get_width() ** 2 + upperscreen.get_height() ** 2)**0.5

	def update(self, hugh, goal, enemies):
		goal = goal.sprites()
		enemies = enemies.sprites()
		hughPos = [hugh.x, hugh.y]
		newFarVol = self.farMusic.get_volume()
		newNearVol = self.nearMusic.get_volume()

		if len(goal) > 0:
			goalPos = [goal[0].rect.x+10, goal[0].rect.y+10]
			goalDist = ((hugh.x - goal[0].rect.x)**2 + (hugh.y - goal[0].rect.y)**2)**0.5 / self.maxDist
			intensity = (goalDist - 1) ** 2
			newFarVol = self.FAR_MUSIC_MAX * intensity
			# self.farMusic.set_volume(newFarVol)
		else:
			newFarVol = 0

		if len(enemies) > 0:
			minDist = ((hugh.x - enemies[0].rect.x)**2 + (hugh.y - enemies[0].rect.y)**2)**0.5
			minEn = enemies[0]
			for e in enemies:
				dist = ((hugh.x - e.rect.x)**2 + (hugh.y - e.rect.y)**2)**0.5
				if dist < minDist:
					minEn = e

			minDist /= self.maxDist
			intensity = (minDist - 1) ** 2
			newNearVol = self.NEAR_MUSIC_MAX * intensity
		else:
			newNearVol = 0

		if newFarVol > 0 or newNearVol > 0:
			total = newFarVol + newNearVol

			self.farMusic.set_volume(newFarVol/total)
			if self.nearMusic.get_volume() == 0 and newNearVol > 0:
				print "HERE"
				self.nearMusic.play(-1, fade_ms = 5000)
			self.nearMusic.set_volume(newNearVol/total)
		else:
			# neither enemy nor goal. So just play the nice one
			self.nearMusic.fadeout(5000) # fade out the old if it's there
			self.farMusic.set_volume(self.FAR_MUSIC_MAX)


class Game:
	"""Main game logic"""

	def __init__(self, width = 600, height = 600):
		# initialise pygame
		pygame.init()

		#initialise wall object container
		self.walls = pygame.sprite.Group()
		self.goals = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.all_sprites = pygame.sprite.Group()

		# Set background to white
		self.bg = (255,255,255)

		#Load all maps into a map array
		self.maps = sorted(glob.glob('./maps/*.txt'))
		#Set the level to 0
		self.level = 0

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

		self.music = Music(self.screen)

		
	# load a map file
	def loadMap(self, fileName):
		try:
			#Open map file
			f = open(fileName, 'r')
			for line in f:
				line = line.split( )

				if(line[0] == "#"):
					pass
				elif(line[0] == "C"):
					self.hugh.x = int(line[1])
					self.hugh.y = int(line[2])
				elif(line[0] == "E"):
					obj = Enemy([line[1], line[2]], line[3], line[4], self.screen, "./sprites/E.png", "enemy")
					self.enemies.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "WB"):
					obj = Object([line[1], line[2]], "./sprites/WB.png", "wall")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "WT1"):
					obj = Object([line[1], line[2]], "./sprites/WT1.png", "wall")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "WT2"):
					obj = Object([line[1], line[2]], "./sprites/WT2.png", "wall")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "WT3"):
					obj = Object([line[1], line[2]], "./sprites/WT3.png", "wall")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "WT4"):
					obj = Object([line[1], line[2]], "./sprites/WT4.png", "wall")
					self.walls.add(obj)
					self.all_sprites.add(obj)
				elif(line[0] == "G"):
					obj = Object([line[1], line[2]], "./sprites/end.png", "goal")
					self.goals.add(obj)
					self.all_sprites.add(obj)				
			pass
		except Exception, e:
			raise e

	def resetLevel(self):
		self.walls.empty()
		self.goals.empty()
		self.enemies.empty()
		self.all_sprites.empty()

		self.screen.fill(self.bg)

	def main(self):
		self.loadMap(self.maps[self.level])

		while self.running:

			# pass all pressed keys to Hugh for processing
			keys = pygame.key.get_pressed()
			self.hugh.move(keys)

			for event in pygame.event.get():
				# press Exit button or ESC key
				if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					self.running = False

			self.screen.fill(self.bg)

			#Move/check enemy collisions
			for e in self.enemies:
				e.move()
				for w in self.walls:
					if(pygame.sprite.collide_mask(w, e) != None):
						e.collision()

			#Check wall collisions
			for wall in self.walls:
				if(pygame.sprite.collide_mask(wall, self.hugh) != None):
					self.hugh.collision()

			#Check Hugh and enemy collisions
			for e in self.enemies:
				if(pygame.sprite.collide_mask(e, self.hugh) != None):
					self.resetLevel()
					self.loadMap(self.maps[self.level])
			
			#Check if Hugh is at the end of the level
			for goal in self.goals:
				if(pygame.sprite.collide_mask(goal, self.hugh) != None):
					#attempt to load the next level map
					try:
						self.resetLevel()
						self.level += 1
						self.loadMap(self.maps[self.level])
					except Exception, e:
						#No more maps condition !!END GAME!!
						raise e

			# draw map
			self.all_sprites.draw(self.screen)

			# draw the masking screen
			self.maskScreen.draw(self.hugh)
			
			# draw Hugh
			self.hugh.draw(self.goals.sprites() + self.enemies.sprites())
			
			self.music.update(self.hugh, self.goals, self.enemies)
			pygame.display.flip()
			self.clock.tick(self.framerate)
	
	
window = Game()
window.main()
