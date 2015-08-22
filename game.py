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
		if key == pygame.K_RIGHT or key == pygame.K_d:
			xMove = self.speed
		elif key == pygame.K_LEFT or key == pygame.K_a:
			xMove = -self.speed
		elif key == pygame.K_UP or key == pygame.K_w:
			yMove = -self.speed
		elif key == pygame.K_DOWN or key == pygame.K_s:
			yMove = self.speed
		
		self.x += xMove
		self.y += yMove

	
	

class Game:
	"""Main game logic"""

	def __init__(self, width = 800, height = 600):
		self.width = width
		self.height = height

		self.screen = pygame.display.set_mode((width,height))
		pygame.display.set_caption('Hue')

		self.running = True # game will enter loop
		self.framerate = 20
		self.clock = pygame.time.Clock() # timer
		pygame.key.set_repeat(self.framerate) # keypresses hold

		self.hugh = Hugh(self.width/2, self.height/2)

		

	def main(self):
		while self.running:

			for event in pygame.event.get():
				# events go here
				if event.type == pygame.QUIT:
					self.running = False
				elif event.type == pygame.KEYDOWN:
					self.hugh.move(event.key)

				
			

			self.screen.fill((0,0,0))
			pygame.draw.circle(self.screen, (255,0,0), (self.hugh.x, self.hugh.y), self.hugh.radius)

			pygame.display.flip()
			self.clock.tick(self.framerate)
	
	
window = Game()
window.main()
