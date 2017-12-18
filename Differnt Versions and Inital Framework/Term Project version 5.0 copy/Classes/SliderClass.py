from ButtonClass import *
class Slider(object):
	def __init__(self, screen, length, startx, starty,boxLocation=None):
		self.screen = screen
		self.length = length
		self.startx = startx
		self.starty = starty
		self.color = (255,255,255)
		self.color1 = (170,170,170)
		if boxLocation == None:
			self.boxLocation = startx
		else: self.boxLocation = boxLocation
	def drawRectangle(self):
		pygame.draw.rect(self.screen, self.color,(self.startx,self.starty,self.length, 2))
	def drawButton(self):
		self.button = Button(20, 20, self.boxLocation, self.starty, self.color1, "",0,0)
		self.button.drawBox(self.screen)
	def drawSlider(self):
		self.drawRectangle()
		self.drawButton()
	def isCollide(self):
		#sees if mouse collides with button
		return self.button.isCollide()
	def getRatio(self):
		return ((self.boxLocation - self.startx) /self.length)*10 + 1
		