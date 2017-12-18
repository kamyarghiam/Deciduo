from Databases.Final_Databases.SQL_Database.SQL_Support import *
import random
import pygame
class MyButton(object):
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



#creates an interactive dialogue box to write in and access the data
class DialogueBox(MyButton):
	def __init__(self, lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, *args, textsize = 27, textcolor = (0,0,0), boxshiftx=0, boxshifty=0, whiteboxnumber = 1, highlightBox= -1, isPassword = True, extendedBox = False, dateBox = False, numBox = False):
		super().__init__(lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, textsize, textcolor)
		self.boxshiftx = boxshiftx
		self.boxshifty = boxshifty
		self.whiteboxnumber = whiteboxnumber
		self.othertext = args
		self.highlightBox = highlightBox
		self.writingText = [[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""]]
		self.isPassword = isPassword
		self.extendedBox = extendedBox
		self.dateBox = dateBox
		self.numBox = numBox

	#draws the white box where the user writes 
	def drawWhiteBox(self, shift, typing = False, screen = None):
		#where the white box should be
		self.whiteboxX = self.startx + self.textsize + self.shiftx + self.textlength + self.boxshiftx
		self.whiteboxY = self.starty + self.shifty + self.boxshifty + shift
		self.endX = self.lengthx - (self.textsize + self.shiftx+self.textlength)-20 
		if typing == True:
			color = (0,183,245)
		else: color = (255,255,255)
		location = (self.whiteboxX,self.whiteboxY, self.endX, 20)
		pygame.draw.rect(screen, color,location)
	
	#draws the pink box around the dialogue box 
	def drawBox(self, screen):
		super().drawBox(screen)
		for i in range(self.whiteboxnumber):
			if self.highlightBox == self.whiteboxnumber-1-i:
				self.drawWhiteBox(i*30, True,screen)
				self.drawShadow(screen, self.whiteboxX, self.whiteboxY, self.endX, 20)
			else: self.drawWhiteBox(i*30,False,screen)
		count = 0
		for text in self.othertext:
			count +=1
			self.drawText(screen, text, count, 0 ,2)
		count = 0
		for writing in range(len(self.writingText)):
			text = self.writingText[writing][0]
			if self.isPassword:
				if writing == 1 or writing == 2:
					self.drawText(screen, "*"*len(text), count, self.textlength +30, 5)
				else:
					self.drawText(screen, text, count, self.textlength +30, 3)
			elif self.whiteboxnumber ==1:
				self.drawText(screen, text, count, self.textlength +30, 5)
			else: self.drawText(screen, text, count, self.textlength +30, 3)
			count +=1
	
	#adds the correct writing (with correct limits) to where it is stored
	def addWriting(self, text, place):
		if self.extendedBox:
			if len(self.writingText[place][0]) > 46:
				return
		elif self.dateBox:
			if len(self.writingText[place][0]) > 9:
				return
		elif self.numBox:
			if len(self.writingText[place][0]) > 3:
				return
		else:
			if len(self.writingText[place][0]) > 28:
				return
		self.writingText[place][0] = self.writingText[place][0] + text

	#deletes writing from where the text is stored 
	def deleteWriting(self, place):
		self.writingText[place][0] = self.writingText[place][0][:-1]

	#checks if you can add a new user to database (if everything was properly entered). If yes, it adds them
	def addToDatabase(self):
		complete = True
		for entry in range(6):
			if self.writingText[entry][0] == "":
				complete = False
		if complete == False:
			return "incomplete"
		elif self.writingText[1][0] != self.writingText[2][0]:
			return "passwords"
		try:
			int(self.writingText[4][0])
			int(self.writingText[5][0])
		except: return "age"
		#this adds entries to database
		addNewEntry(self.writingText[0][0],hashFunction(self.writingText[1][0]),\
		self.writingText[3][0], self.writingText[4][0], self.writingText[5][0])
		return "complete"

	#sees if passowrd and username are valid 
	def accessDatabase(self):
		username = self.writingText[0][0]
		password = self.writingText[1][0]
		dataList = accessData()
		for entry in dataList:
			if username == entry[1]:
				if hashFunction(password) == entry[2]:
					return entry
				else: return "password"
		return "username"

	#finds the parameters of another user 
	def findOtherUser(self):
		name = self.writingText[0][0]
		dataList = accessData()
		for entry in dataList:
			if name == entry[3]:
				return [entry[6],entry[7], entry[3],entry[1]]
		return "No User"
#hash function to hash passwords
def hashFunction(password):
	random.seed(0)
	newPassword = []
	for letter in password:
		newPassword += [str(abs((ord(letter)-random.randrange(26)))%26)]
	return "".join(newPassword)

