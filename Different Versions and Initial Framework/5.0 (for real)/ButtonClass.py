import pygame
class Button(object):
	def __init__(self,lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, textsize = 27, textcolor = (0,0,0)):
		self.font = pygame.font.Font('fonts/arial.ttf', textsize)
		self.textsize = textsize
		self.startx = centerx-lengthx//2
		self.starty = centery-lengthy//2
		self.centerx = centerx
		self.centery= centery
		self.lengthx = lengthx
		self.lengthy = lengthy
		self.originalColor = color
		self.color = color 
		self.textcolor = textcolor
		#black text color default
		self.titlesurface = (self.font).render(text, False, textcolor)
		#self.text is inherited for the dialogue box
		self.textlength = len(text)*10
		self.width = 3
		self.shiftx = textshiftx
		self.shifty = textshifty
	def drawRectangle(self, screen):
		pygame.draw.rect(screen, self.color,(self.startx,self.starty,self.lengthx, self.lengthy))
	def drawShadow(self, screen, startx = None, starty = None, lengthx = None, lengthy = None):
		if startx == None:
			startx = self.startx
			starty = self.starty
			lengthx = self.lengthx
			lengthy = self.lengthy
		pygame.draw.rect(screen, (153,153,153),(startx, starty + lengthy-self.width,lengthx, self.width))
		pygame.draw.rect(screen, (153,153,153),(startx+lengthx-self.width, starty,self.width, lengthy))
	def drawText(self, screen, titlesurface = None, shift = 0, shiftx = 0, shifty = 0, font = None, color = None):
		if font == None:
			font = self.font
		if color == None:
			color = self.textcolor
		if titlesurface == None:
			titlesurface = self.titlesurface
		else: titlesurface = (font).render(titlesurface, False, color)
		screen.blit(titlesurface,(self.startx+self.shiftx+shiftx,self.starty+self.shifty +shifty + shift*30))
	def drawBox(self,screen):
		self.drawRectangle(screen)
		self.drawShadow(screen)
		self.drawText(screen)
	def isCollide(self):
		#sees if mouse collides with button
		mousex = pygame.mouse.get_pos()[0]
		mousey = pygame.mouse.get_pos()[1]
		return abs(mousex-self.centerx) < self.lengthx//2 and\
		abs(mousey-self.centery) < self.lengthy//2

