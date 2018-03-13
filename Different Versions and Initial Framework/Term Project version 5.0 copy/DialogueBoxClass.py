import pygame 
import ButtonClass
from Databases.Final_Databases.SQL_Database.SQL_Support import *


class DialogueBox(ButtonClass.Button):
	def __init__(self, lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, *args, textsize = 27, textcolor = (0,0,0), boxshiftx=0, boxshifty=0, whiteboxnumber = 1, highlightBox= -1, isPassword = True, extendedBox = False):
		super().__init__(lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, textsize, textcolor)
		self.boxshiftx = boxshiftx
		self.boxshifty = boxshifty
		self.whiteboxnumber = whiteboxnumber
		self.othertext = args
		self.highlightBox = highlightBox
		self.writingText = [[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""],[""]]
		self.isPassword = isPassword
		self.extendedBox = extendedBox

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
	def addWriting(self, text, place):
		if self.extendedBox == False:
			if len(self.writingText[place][0]) > 28:
				return
			self.writingText[place][0] = self.writingText[place][0] + text
		else:
			if len(self.writingText[place][0]) > 46:
				return
			self.writingText[place][0] = self.writingText[place][0] + text


	def deleteWriting(self, place):
		self.writingText[place][0] = self.writingText[place][0][:-1]

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
		addNewEntry(self.writingText[0][0],self.writingText[1][0],\
		self.writingText[3][0], self.writingText[4][0], self.writingText[5][0])
		return "complete"
	def accessDatabase(self):
		username = self.writingText[0][0]
		password = self.writingText[1][0]
		dataList = accessData()
		for entry in dataList:
			if username == entry[1]:
				if password == entry[2]:
					return entry
				else: return "password"
		return "username"

