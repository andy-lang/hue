import pygame
from pygame.locals import *

class Hugh(pygame.sprite.DirtySprite):
	"""Representation of moveable player."""

	def __init__(self, screen, x, y, radius = 20):
		# Call parent class sprite constructor
		pygame.sprite.DirtySprite.__init__(self)

		self.screen = screen
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

	def draw(self):
		pygame.draw.circle(self.screen, (255,0,0), (self.x, self.y), self.radius)
	
