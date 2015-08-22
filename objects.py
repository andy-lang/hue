import pygame
from pygame.locals import *

class Hugh(pygame.sprite.DirtySprite):
	"""Representation of moveable player."""

	def __init__(self, screen, x, y, radius = 20):
		# Call parent class sprite constructor
		pygame.sprite.DirtySprite.__init__(self)

		# self.screen = screen
		self.radius = radius
		self.screen = pygame.Surface((4*self.radius, 4*self.radius), flags=SRCALPHA) # create screen for the sprite. SRCALPHA means that it'll be transparent where nothing's drawn to it
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
		
		self.x += xMove
		self.y += yMove

	def draw(self):
		pygame.draw.circle(self.screen, (255,0,0), (2*self.radius, 2*self.radius), self.radius)
		self.upperScreen.blit(self.screen, (self.x, self.y))
	
