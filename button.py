"""
	API:
		`@class Button` specifically for level editor not for menu in game.
"""
import pygame 

class Button():
	"""
		Class specifically for level editor not for menu in game.
		API:
			`@init_method button = Button(x, y, image, scale)` creats instant of the class
   			`@method button.Draw(screen)` draws button on the screen.
	"""
	def __init__(self,x, y, image, scale):
		"""
  			Creats instant of the class
    	"""
		width = image.get_width()
		height = image.get_height()
		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def Draw(self, surface):
		"""
			Draws button on the screen and tells if the button was clicked.
    	"""
		action = False

		#get mouse position
		pos = pygame.mouse.get_pos()

		#check mouseover and clicked conditions
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				action = True
				self.clicked = True

		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False

		#draw button
		surface.blit(self.image, (self.rect.x, self.rect.y))

		return action