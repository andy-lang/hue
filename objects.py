import pygame
from pygame.locals import *

class Hugh(pygame.sprite.DirtySprite):
	"""Representation of moveable player."""

	def __init__(self, screen, x, y, radius = 20):
		# Call parent class sprite constructor
		pygame.sprite.DirtySprite.__init__(self)

		# self.screen = screen
		self.radius = radius
		self.screen = pygame.Surface((2*self.radius, 2*self.radius), flags=SRCALPHA) # create screen for the sprite. SRCALPHA means that it'll be transparent where nothing's drawn to it
		# self.screen.set_colorkey((0,0,0))
		# self.screen.set_alpha(100)

		self.upperScreen = screen
		# self.screen.fill((self.upperScreen.bg))
		self.x = x
		self.y = y

		self.speed = 5

	def move(self, key):
		xMove = yMove = 0
		if key[pygame.K_RIGHT] or key[pygame.K_d]:
			xMove += self.speed
		if key[pygame.K_LEFT] or key[pygame.K_a]:
			xMove -= self.speed
		if key[pygame.K_UP] or key[pygame.K_w]:
			yMove -= self.speed
		if key[pygame.K_DOWN] or key[pygame.K_s]:
			yMove += self.speed
		
		if 0 <= self.x+xMove <= self.upperScreen.get_width()-2*self.radius:
			self.x += xMove
		if 0 <= self.y+yMove <= self.upperScreen.get_height()-2*self.radius:
			self.y += yMove

	def draw(self):
		pygame.draw.circle(self.screen, (255,0,0), (self.radius, self.radius), self.radius)
		self.upperScreen.blit(self.screen, (self.x, self.y))
	

class MaskScreen:
	"""Screen to mask objects based upon Hugh's position"""

	def __init__(self, upperScreen, width, height):
		self.width = width
		self.height = height

		self.maskColour = (0,0,255)
		self.upperScreen = upperScreen

		self.screen = pygame.Surface((self.width, self.height))
		self.screen.set_colorkey(self.maskColour)

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

		self.rect = self.image.get_rect()
		self.rect.x = int(coord[0])
		self.rect.y = int(coord[1])