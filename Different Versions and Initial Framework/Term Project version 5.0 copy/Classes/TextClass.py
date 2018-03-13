import pygame
class Text(object):
	def __init__(self,topLeftx, topLefty, text, size, color = (255,255,255)):
		self.topLeftx = topLeftx
		self.topLefty = topLefty
		self.text = text
		self.size = size
		self.color = color
		self.font = pygame.font.Font('fonts/arial.ttf', self.size)
		self.surface = (self.font).render(self.text, False, self.color)
	def write(self,screen):
		screen.blit(self.surface,(self.topLeftx,self.topLefty))

