import pygame

class Hugh:
	"""Representation of moveable player."""

	def __init__(self, x, y, radius = 30):
		self.radius = radius
		
		self.x = x
		self.y = y

		self.speed = 5

	def move(self, key):
		xMove = yMove = 0
		if key == K_RIGHT:
			xMove = self.speed
		elif key == K_LEFT:
			xMove = -self.speed
		elif key == K_UP:
			yMove = -self.y_dist
		elif key == K_DOWN:
			yMove = self.y_dist
		
		self.x += xMove
		self.y += yMove
	
	

class Game:
	"""Main game logic"""

	def __init__(self, width = 800, height = 600):
		self.width = width
		self.height = height

		self.screen = pygame.display.set_mode((width,height))
		pygame.display.set_caption('Hue')

		self.running = True
		self.framerate = 20
		self.clock = pygame.time.Clock()

		self.hugh = Hugh(self.width/2, self.height/2)

	def main(self):
		while self.running:
			for event in pygame.event.get():
				# events go here
				if event.type == pygame.QUIT:
					self.running = False

			pygame.draw.circle(self.screen, (255,0,0), (self.hugh.x, self.hugh.y), self.hugh.radius)

			pygame.display.flip()
			self.clock.tick(self.framerate)
	
	
window = Game()
window.main()
