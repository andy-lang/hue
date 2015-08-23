import pygame
import math
from pygame.locals import *

class Hugh(pygame.sprite.DirtySprite):
	"""Representation of moveable player."""

	def __init__(self, screen, x, y, radius = 20):
		# Call parent class sprite constructor
		pygame.sprite.DirtySprite.__init__(self)

		self.x = x
		self.y = y

		#set prev variable to store previous positions
		self.prevX = x
		self.prevY = y

		self.radius = radius
		self.speed = 2

		#load dummy image
		self.image = pygame.image.load("./sprites/hugh.png").convert_alpha()

		self.screen = pygame.Surface((2*self.radius, 2*self.radius), flags=SRCALPHA) # create screen for the sprite. SRCALPHA means that it'll be transparent where nothing's drawn to it
		self.upperScreen = screen # parent surface of this one

		self.maxDist = self.distance(0, 0, self.upperScreen.get_width(), self.upperScreen.get_height()) # max distance that Hugh could possibly be from a thing

		# self.mask = pygame.mask.Mask((self.screen.get_width(), self.screen.get_height()))


	# Move method. keys should be an array of keypresses, returned by pygame.key.get_pressed().
	# pygame.event.get() could also be used for this, but would not allow for diagonal movement.
	def move(self, keys):
		xMove = yMove = 0
		if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
			xMove += self.speed
		if keys[pygame.K_LEFT] or keys[pygame.K_a]:
			xMove -= self.speed
		if keys[pygame.K_UP] or keys[pygame.K_w]:
			yMove -= self.speed
		if keys[pygame.K_DOWN] or keys[pygame.K_s]:
			yMove += self.speed
		
		# ensures that Hugh doesn't move if about to go off the screen
		if 0 <= self.x+xMove <= self.upperScreen.get_width()-2*self.radius:
			self.prevX = self.x
			self.x += xMove
		if 0 <= self.y+yMove <= self.upperScreen.get_height()-2*self.radius:
			self.prevY = self.y
			self.y += yMove

		self.rect = pygame.Rect(self.x, self.y, 2*self.radius, 2*self.radius)


	# Draw Hugh's circle onto this screen and blit to the parent screen
	# param objects is a list of objects in the world to check Hugh's position against, to check for colour
	def draw(self, objects):
		pygame.draw.circle(self.screen, (255,0,0), (self.radius, self.radius), self.radius)

		for i in range(2*self.radius):
			for j in range(2*self.radius):
				if self.screen.get_at((i,j))[3] > 0:
					pixelPos = [self.x - self.radius + i, self.y - self.radius + j]
					newColour = [0,0,0,255]
					for obj in objects:
						dist = ((pixelPos[0] - obj.rect.x) ** 2 + (pixelPos[1] - obj.rect.y) ** 2) ** 0.5 / self.maxDist
						#dist = (abs(pixelPos[0] - obj.rect.x) + abs(pixelPos[1] - obj.rect.y)) / self.maxDist
						intensity = (dist-1)**4
						if obj.objtype == "goal":
							newColour[1] += 255 * intensity
							if(newColour[1] > 255):
								newColour[1] = 255
						elif obj.objtype == "enemy":
							newColour[0] += 255 * intensity
							if(newColour[0] > 255):
								newColour[0] = 255
					self.screen.set_at((i,j), newColour)

		self.mask = pygame.mask.from_surface(self.image) # update mask
		self.upperScreen.blit(self.screen, (self.x, self.y))

	def collision(self):
		self.x = self.prevX
		self.y = self.prevY

	def distance(self, x1, y1, x2, y2):
		return ((x1-x2)**2 + (y1-y2)**2)**0.5
	
	

class MaskScreen:
	"""Screen to mask objects based upon Hugh's position.
	Creates a viewport in effect that forces the player to only be able to see a certain amount of the screen. """

	def __init__(self, upperScreen, width, height):
		self.width = width
		self.height = height

		self.maskColour = (0,0,255)
		self.upperScreen = upperScreen # parent surface of this one

		self.screen = pygame.Surface((self.width, self.height))
		self.screen.set_colorkey(self.maskColour) # set transparent if blue

	# fill screen with white, then draw a viewport around Hugh's position. Then blit to the parent screen
	def draw(self, hugh):
		self.screen.fill((255,255,255))
		pygame.draw.circle(self.screen, self.maskColour, (hugh.x+hugh.radius, hugh.y+hugh.radius), int(2.2*hugh.radius))
		self.upperScreen.blit(self.screen, (0,0))
	
		
class Object(pygame.sprite.DirtySprite):
	"""Representation of a wall block."""

	def __init__(self, coord, image, objtype):
		pygame.sprite.DirtySprite.__init__(self)

		self.image = pygame.image.load(image).convert_alpha()
		self.image.set_colorkey((255, 255, 255))

		self.mask = pygame.mask.from_surface(self.image)
		self.objtype = objtype

		self.rect = self.image.get_rect()
		self.rect.x = int(coord[0])
		self.rect.y = int(coord[1])

class Enemy(pygame.sprite.DirtySprite):
	"""Representation of ememy"""

	def __init__(self, coord, direction, speed, screen, image, objtype):
		pygame.sprite.DirtySprite.__init__(self)

		self.image = pygame.image.load(image).convert_alpha()
		self.image.set_colorkey((255,255,255))

		self.mask = pygame.mask.from_surface(self.image)

		self.rect = self.image.get_rect()
		self.rect.x = int(coord[0])
		self.rect.y = int(coord[1])
	
		self.objtype = objtype

		self.direction = int(direction) * math.pi / 180
		self.speed = int(speed)

		self.screen = screen
		self.radius = 10

	def move(self):
		moveX = math.sin(self.direction)*self.speed
		moveY = math.cos(self.direction)*self.speed

		if 0 <= self.rect.x+moveX <= self.screen.get_width()-2*self.radius:
			self.rect.x += moveX
		if 0 <= self.rect.y+moveY <= self.screen.get_height()-2*self.radius:
			self.rect.y += moveY

	def collision(self):
		if(self.direction == 0):
			self.direction = math.pi
		elif(self.direction == math.pi/2):
			self.direction = 3*math.pi/2
		elif(self.direction == math.pi):
			self.direction = 0
		elif(self.direction == 3*math.pi/2):
			self.direction = math.pi/2
		self.move()
