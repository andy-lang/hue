import pygame
from pygame.locals import *

class Hugh(pygame.sprite.DirtySprite):
	"""Representation of moveable player."""

	def __init__(self, screen, x, y, radius = 20):
		# Call parent class sprite constructor
		pygame.sprite.DirtySprite.__init__(self)

		self.x = x
		self.y = y
		self.radius = radius
		self.speed = 5

		#load dummy image
		self.image = pygame.image.load("./sprites/hugh.png").convert_alpha()

		self.screen = pygame.Surface((2*self.radius, 2*self.radius), flags=SRCALPHA) # create screen for the sprite. SRCALPHA means that it'll be transparent where nothing's drawn to it
		self.upperScreen = screen # parent surface of this one

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
			self.x += xMove
		if 0 <= self.y+yMove <= self.upperScreen.get_height()-2*self.radius:
			self.y += yMove

		self.rect = pygame.Rect(self.x, self.y, 2*self.radius, 2*self.radius)


	# Draw Hugh's circle onto this screen and blit to the parent screen
	def draw(self):
		pygame.draw.circle(self.screen, (255,0,0), (self.radius, self.radius), self.radius)
		self.mask = pygame.mask.from_surface(self.image) # update mask
		self.upperScreen.blit(self.screen, (self.x, self.y))
	

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
		pygame.draw.circle(self.screen, self.maskColour, (hugh.x+hugh.radius, hugh.y+hugh.radius), 3*hugh.radius)
		self.upperScreen.blit(self.screen, (0,0))
	
		
class Object(pygame.sprite.DirtySprite):
	"""Representation of a wall block."""

	def __init__(self, coord, image):
		pygame.sprite.DirtySprite.__init__(self)

		self.image = pygame.image.load(image).convert_alpha()
		self.image.set_colorkey((255, 255, 255))

		self.mask = pygame.mask.from_surface(self.image)

		self.rect = self.image.get_rect()
		self.rect.x = int(coord[0])
		self.rect.y = int(coord[1])
