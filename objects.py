import pygame
from pygame.locals import *

class Hugh(pygame.sprite.DirtySprite):
	"""Representation of moveable player."""

	def __init__(self, x, y, radius = 20):
		# Call parent class sprite constructor
		pygame.sprite.DirtySprite.__init__(self)

		self.radius = radius
		self.x = x
		self.y = y

		self.speed = 5

	def move(self, key):
		xMove = yMove = 0
		if key[pygame.K_RIGHT] or key[pygame.K_d]:
			xMove = self.speed
		if key[pygame.K_LEFT] or key[pygame.K_a]:
			xMove = -self.speed
		if key[pygame.K_UP] or key[pygame.K_w]:
			yMove = -self.speed
		if key[pygame.K_DOWN] or key[pygame.K_s]:
			yMove = self.speed
		
		self.x += xMove
		self.y += yMove

class Wall(pygame.sprite.DirtySprite):
	"""Representation of a wall block."""

	def __init__(self, coord, image):
		pygame.sprite.DirtySprite.__init__(self)

		self.image = pygame.image.load(image)#.convert_alpha()
		#self.image.set_colorkey((255, 255, 255))

		self.rect = self.image.get_rect()
