#Kamyar Ghiam 15-112 Term Project "Deciduo" Animation Framework

from TermProjectFinalMath import *
import pygame
import random
import string
from Supporting_Documents.Shift_Letters import findShift
from Databases.Final_Databases.SQL_Database.SQL_Support import *
#Food Database
import Databases.Final_Databases.FoodDatabase as FOOD
import Databases.Final_Databases.Exercise_Database_Final as EXERCISE
#this is to reload the databases
import importlib as imp
from Classes.TextClass import *
from ButtonClass import *
from DialogueBoxClass import *
from Classes.SliderClass import *
from Classes.DictionaryFunctions import *
from Supporting_Documents.Machine_learning_Compenent import * 

#taken from 15-112 course website
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))

#The framework for pygame taken from the GitHub offered by the 112 TA's
#Code within the framework is original
class PygameGame(object):
	pygame.font.init()
	titlefont = pygame.font.Font('fonts/Capture_it.ttf', 200)
	smalltitlefont = pygame.font.Font('fonts/Capture_it.ttf', 60)
	smallerfont = pygame.font.Font('fonts/Capture_it.ttf', 20)
	def init(self, mode = "Startscreen", profile = None,LeftWord = "Log in",RightWord = "New User"):
		self.image_number = 1
		self.mode = mode
		#gif taken from https://giphy.com/gifs/wallpaper-3o6vXTpomeZEyxufGU
		self.image = pygame.image.load('image/background-%d (dragged).tiff' %\
		self.image_number).convert()
		self.scale = 1.5 #how to resize image 
		self.w,self.h = self.image.get_size() #size fo the image
		self.highlightFont = (227,211,0)
		self.blueFont = (0, 157, 245)
		self.greenFont = (0, 255, 0)
		self.redFont = (240, 0, 0)
		self.volume = 0.2
		self.volumeSlider = 840
		##Optional Parameters
		self.LeftWord = LeftWord
		self.RightWord = RightWord
		#currently logged in 
		self.profile = profile
		##
		if self.mode == "Startscreen":
			self.titlesurface = (PygameGame.titlefont).render('Deciduo', False, (236, 34, 243))
			self.versionSurface = (PygameGame.smallerfont).render('Version 6.0 By Kamyar Ghiam', False, (255,255,255))
			#This is an excerpt from "Acres"-Same Gellaitry-(Purchased from Amazon)
			pygame.mixer.music.load("Music&Sounds/AcresEdited.wav")
			pygame.mixer.music.play(loops=-1)
			pygame.mixer.music.set_volume(self.volume)
		if self.mode == "Math":
				self.name = self.profile[3]
				self.titlesurface = (PygameGame.smalltitlefont).render('Welcome %s' %self.name, False, (236, 34, 243))
		self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.blueFont)
		self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.blueFont)
		self.volumeSurface = (PygameGame.smallerfont).render('Volume :', False, (255,255,255))

		#these are for the sparks
		self.sparks = []
		self.mousex = pygame.mouse.get_pos()[0]
		self.mousey = pygame.mouse.get_pos()[1]

		self.nonMouseSparks = []
		#speed of sparks
		self.speed = 1
		#exercise/login button and food/new user button
		self.text1 = 190
		self.text2 = 590
		self.textHeight = 550
		self.isLeft = False
		self.isRight = False

		self.gray = (250,250,250)
		self.buttonColor = self.gray
		self.buttonColor1 = self.gray
		self.buttonColor2 = self.gray
		self.buttonColor3 = self.gray
		self.foodSearchSubmitColor = self.gray
		self.manualButton = self.gray
		#highlights the dialogue box
		self.highlightBox = -1
		self.dialogueBox1 = DialogueBox(500, 300, 500,400, (238,41,241), "Username", 10, 10, "Password", "Confirm ^","First Name", "Age", "Weight",textsize = 20, boxshifty = 5, whiteboxnumber = 6, highlightBox = self.highlightBox)
		self.dialogueBox2 = DialogueBox(500, 200, 500,300, (238,41,241), "Username", 10, 10, "Password",textsize = 20, boxshifty = 5, whiteboxnumber = 2, highlightBox = self.highlightBox)
		self.caloriesDialogue = DialogueBox(100,70, 540, 200, (238,41,241), "", 0, 0, "",textsize = 20, boxshifty = 5, whiteboxnumber = 2, highlightBox = self.highlightBox, isPassword = False)
		self.ExerciseCaloriesDialogue = DialogueBox(100,30, 540, 200, (238,41,241), "", 0, 0, "",textsize = 20, boxshifty = 5, whiteboxnumber = 1, highlightBox = self.highlightBox, isPassword = False)
		self.foodSearch = DialogueBox(500,40, 550, 200, (238,41,241), "", 0, 0, "",textsize = 20, boxshifty = 8, whiteboxnumber = 1, highlightBox = self.highlightBox, isPassword = False, extendedBox = True)
		self.nameOfFood = DialogueBox(400,100, 725, 246, (238,41,241), "", 0, 0, "", "","",textsize = 20, boxshifty = 8, whiteboxnumber = 3, highlightBox = self.highlightBox, isPassword = False, extendedBox = True)
		self.priceOfFood = DialogueBox(125,40, self.width//2, 300, (238,41,241), "$", 5, 2, "",textsize = 25, boxshifty = 8, whiteboxnumber = 1, highlightBox = self.highlightBox, isPassword = False)
		self.exerciseSearch = DialogueBox(500,40, 590, 200, (238,41,241), "", 0, 0, "",textsize = 20, boxshifty = 8, whiteboxnumber = 1, highlightBox = self.highlightBox, isPassword = False, extendedBox = True)
		self.exerciseManualDialogue = DialogueBox(350,70, 770, 225, (238,41,241), "", 0, 0, "",textsize = 20, boxshifty = 5, whiteboxnumber = 2, highlightBox = self.highlightBox, isPassword = False, extendedBox = True)
		self.desiredTimeDialogue = DialogueBox(125,40, self.width//2, 650, (238,41,241), "", 5, 2, "",textsize = 25, boxshifty = 8, whiteboxnumber = 1, highlightBox = self.highlightBox, isPassword = False)
		# for new user
		self.complete = True
		self.passwordsMatch = True
		self.age = True

		#for log in 
		self.username = True
		self.password = True
		#for log out
		self.logOutButtonColor = self.gray
		#for the food
		self.healthySliderLocation = self.width//3
		self.healthySliderNumber = 0
		self.satisfiedSliderLocation = self.width//3
		self.satisfiedSliderNumber = 0
		self.discrete = None
		self.foodSubmitColor = self.gray
		self.caloriesInteger = True
		self.moneyInteger = True
		self.discreteAnswer = True
		#food search
		self.sorry = False 
		self.suggestions = None
		self.foods = []
		#food manual
		self.foodSliderstart = 570
		self.foodSliderLocation = self.foodSliderstart
		self.foodSliderNumber = 0
		self.foodManualSubmitColor = self.gray
		self.foodHappySubmitColor = self.gray
		self.manualIncomplete = True
		self.manualCalories = True
		self.manualServing = True
		self.happy = []
		self.moneyAmount = []
		#food results
		self.foodHappySliderStart = self.width //2 -200
		self.foodHappySliderLocation = self.foodHappySliderStart
		self.foodHappySliderNumber = 0
		self.moneyNotInteger = False
		self.starSliderstart = 400
		self.starSliderLocation = self.starSliderstart
		self.starSliderNumber = 0 
		self.mainMenuButtonColor = self.gray
		#exercise
		self.exercises = []
		self.happyExercise = []
		self.exerciseSubmitColor = self.gray
		self.exerciseResultsSubmitcolor = self.gray
		self.notValidNumber = False
		self.timeError = False
		self.exerciseResultsText = ""


	def mousePressed(self, x, y):
		if self.mode == "Startscreen":
			self.isLeft = False
			self.isRight = False
			if y > self.height//2:
				if x < self.width//2:
					self.isLeft = True
					self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.greenFont)
					self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.blueFont)
					pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				else: 
					self.isRight = True
					self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.greenFont)
					self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.blueFont)
					#I made this recording myself
					pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				
			else:
				self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.blueFont)
				self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.blueFont)
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/NonClick.wav"))
		elif self.mode == "Log in":
			if self.back.isCollide():
				self.buttonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			elif self.submit1.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				if self.dialogueBox2.accessDatabase() == "password":
					self.buttonColor1=self.redFont
					self.username = True
					self.password = False
				elif self.dialogueBox2.accessDatabase() == "username":
					self.buttonColor1=self.redFont
					self.password = True
					self.username = False
				else:
					self.password = True
					self.username = True
					self.buttonColor1= self.greenFont
					self.profile = self.dialogueBox2.accessDatabase()
					self.init("Math", self.profile, "Exercise", "Food")
		elif self.mode == "Math":
			if self.logOut.isCollide():
				self.logOutButtonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			self.isLeft = False
			self.isRight = False
			if y > self.height//2:
				if x < self.width//2:
					self.isLeft = True
					self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.greenFont)
					self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.blueFont)
					pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				else: 
					self.isRight = True
					self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.greenFont)
					self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.blueFont)
					#I made this recording myself
					pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				
			else:
				self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.blueFont)
				self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.blueFont)
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/NonClick.wav"))

		elif self.mode == "Food":
			if self.back.isCollide():
				self.buttonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			if self.yesButton.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				self.buttonColor2 = self.greenFont
				self.buttonColor3 = self.gray
				self.discrete = True 
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			elif self.noButton.isCollide():
				self.buttonColor3 = self.greenFont
				self.buttonColor2 = self.gray
				self.discrete = False 
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			if self.foodSubmit.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				if self.isLegalSubmit() == "complete":
					self.foodSubmitColor= self.greenFont
					self.foodMath()
					self.mode = "FoodSearch"
				elif self.isLegalSubmit() == "caloriesInteger":
					self.foodSubmitColor= self.redFont
					self.caloriesInteger = False
				elif self.isLegalSubmit() == "discreteAnswer": 
					self.foodSubmitColor= self.redFont
					self.discreteAnswer = False
		elif self.mode == "FoodSearch":
			self.foodSearchSubmitColor = self.gray
			if self.back.isCollide():
				self.buttonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			if self.submitFoodSearch.isCollide():
				self.sorry = False
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				if self.normalDictionary(self.foodSearch.writingText[0][0]) == False or len(self.foodSearch.writingText[0][0])<2:
					self.sorry = True 
					self.foodSearchSubmitColor = self.redFont
					self.getDictionaryResults(self.foodSearch.writingText[0][0])
				else: 
					self.foodSearchSubmitColor = self.greenFont	
			#lets you select a food item
			if  78 <= x <=600:
				if y >= 400:
					for i in range(len(self.foodList)):
						if 400 + 30*(i) <= self.mousey <= 400 + 30*(i+1):
							pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
							self.foods.append(self.temporaryFoods[i])	
							self.sorry = False 	
							self.foodSearchSubmitColor = self.greenFont
							self.mode = "HowHappyFood"
			
			if self.manual.isCollide():
				self.manualButton= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
		elif self.mode == "ExerciseSearch":
			if self.back.isCollide():
				self.buttonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			if self.submitExerciseSearch.isCollide():
				self.sorry = False
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				if self.normalExerciseDictionary(self.foodSearch.writingText[0][0]) == False or len(self.exerciseSearch.writingText[0][0])<2:
					self.sorry = True 
					self.exerciseSubmitColor = self.redFont
					self.exerciseGetDictionaryResults(self.foodSearch.writingText[0][0])
				else: 
					self.exerciseSubmitColor = self.greenFont
					self.mode = "HowHappyExercise"
			try:
				if self.exerciseResultsbutton.isCollide():
					pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
					self.mode = "ExerciseResults"
			except: pass

			#lets you select a food item
			if  78 <= x <=600:
				if y >= 400:
					for i in range(len(self.exerciseList)):
						if 400 + 30*(i) <= self.mousey <= 400 + 30*(i+1):
							pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
							self.exercises.append(self.temporaryExercise[i])	
							self.sorry = False 	
							self.exerciseSubmitColor = self.greenFont
							self.mode = "HowHappyExercise"
			
			if self.exerciseManual.isCollide(): 
				self.manualButton= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				self.mode = "ManualExercise"
		elif self.mode == "ManualExercise":
			if self.back.isCollide():
				self.buttonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			if self.manualSubmit.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				if self.isLegalManualSubmitExercise() == True:
					self.foodManualSubmitColor= self.greenFont
					self.addToExerciseDictionary()
					name = self.exerciseManualDialogue.writingText[0][0]
					calories = int(self.exerciseManualDialogue.writingText[1][0])
					self.exercises.append([name,calories/60])
					self.mode = "HowHappyExercise"
				else:
					self.foodManualSubmitColor= self.redFont
					self.notValidNumber = True

		elif self.mode == "FoodManual":
			if self.back.isCollide():
				self.buttonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			if self.manualSubmit.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				if self.isLegalManualSubmit() == True:
					self.foodManualSubmitColor= self.greenFont
					self.manualIncomplete = True
					self.manualServing = True
					self.manualCalories = True
					self.addToDictionary()
					name = self.nameOfFood.writingText[0][0]
					calories = self.nameOfFood.writingText[1][0]
					servings = self.nameOfFood.writingText[2][0]
					healthy = self.foodSlider.getRatio()
					serving_word = ""
					for letter in range(len(servings)):
						if servings[letter] in string.ascii_letters:
							serving_number = int(servings[0:letter-1])
							serving_word = servings[letter:]
							break
					food_entry = [name, (calories, serving_word, serving_number,healthy)]
					self.foods.append(food_entry)
					self.mode = "HowHappyFood"
				elif self.isLegalManualSubmit() == "incomplete":
					self.foodManualSubmitColor= self.redFont
					self.manualIncomplete = False
					self.manualServing = True
					self.manualCalories = True
				elif self.isLegalManualSubmit() == "calories":
					self.foodManualSubmitColor= self.redFont
					self.manualCalories = False
					self.manualIncomplete = True
					self.manualServing = True
				elif self.isLegalManualSubmit() == "serving": 
					self.foodManualSubmitColor= self.redFont
					self.manualServing = False
					self.manualIncomplete = True
					self.manualCalories = True
		elif self.mode == "Exercise":
			if self.back.isCollide():
				self.buttonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			elif self.yesButton.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				self.buttonColor2 = self.greenFont
				self.buttonColor3 = self.gray
				self.discrete = True 
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			elif self.noButton.isCollide():
				self.buttonColor3 = self.greenFont
				self.buttonColor2 = self.gray
				self.discrete = False 
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			
			if self.exerciseSubmit.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				if self.isLegalExerciseSubmit() == "complete":
					self.foodSubmitColor= self.greenFont
					self.exerciseMath()
					self.mode = "ExerciseSearch"
				elif self.isLegalExerciseSubmit() == "caloriesInteger":
					self.foodSubmitColor= self.redFont
					self.caloriesInteger = False
				elif self.isLegalExerciseSubmit() == "discreteAnswer": 
					self.foodSubmitColor= self.redFont
					self.discreteAnswer = False

		elif self.mode == "New User":
			if self.back.isCollide():
				self.buttonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
			elif self.submit.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				if self.dialogueBox1.addToDatabase() == "complete":
					self.buttonColor1= self.greenFont
					self.complete = True
					self.passwordsMatch = True
					self.mode = "Log in"
					screen = pygame.display.set_mode((self.width, self.height))
					self.redrawAll(screen)
				else:
					self.buttonColor1=self.redFont
					if self.dialogueBox1.addToDatabase() == "passwords":
						self.complete = True
						self.passwordsMatch = False
						self.age = True
					if self.dialogueBox1.addToDatabase() == "incomplete":
						self.passwordsMatch = True
						self.complete = False
						self.age = True
					if self.dialogueBox1.addToDatabase() == "age":
						self.passwordsMatch = True
						self.complete = True
						self.age = False

		elif self.mode == "HowHappyFood":
			if self.foodHappySubmit.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				try: 
					self.moneyAmount.append(int(self.priceOfFood.writingText[0][0]))
					self.moneyNotInteger = False
				except:
					self.moneyNotInteger = True
					self.foodHappySubmitColor= self.redFont
					return
				self.happy.append(self.foodHappySlider.getRatio())
				self.foodHappySubmitColor= self.greenFont
				self.mode = "FoodSearch"
				if len(self.foods) ==2:
					self.mode = "FoodResults"	

		elif self.mode == "HowHappyExercise":
			if self.exerciseHappySubmit.isCollide():
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				self.happyExercise.append(self.exerciseHappySlider.getRatio())
				self.foodHappySubmitColor= self.greenFont
				self.mode = "ExerciseSearch"
				if len(self.exercises) == 5:
					self.mode = "ExerciseResults"
			self.foodSearchSubmitColor = self.gray
			self.exerciseSubmitColor = self.gray
		elif self.mode == "ExerciseResults":
			try:
				if self.exerciseResultsSubmit.isCollide():
					self.exerciseResultsSubmitcolor = self.greenFont
					pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
					parameter = self.profile[7]
					self.exerciseResultsText = runExerciseForAnimation(self.information,parameter,self.exercises, self.happyExercise, int(self.desiredTimeDialogue.writingText[0][0]))
					self.splitResults = splitLinesOfSentence(self.exerciseResultsText)
					self.mainMenuButton = Button(170, 50, 170,350, self.buttonColor, "Main Menu",20, 7)
					self.starQuestion = Text(self.starSliderstart-250, 385, "How helpful was this? (from 0 to 5)", 20)
				else: 
					self.exerciseResultsSubmitcolor = self.gray
			except: pass
					



	def mouseReleased(self, x, y):
		if self.mode == "Startscreen":
			if self.isLeft == True:
				self.mode = "Log in"
			elif self.isRight == True: 
				self.mode = "New User"
		elif self.mode == "Log in":
			if self.back.isCollide():
				self.buttonColor = self.gray
				self.buttonColor1 = self.gray
				self.mode = "Startscreen"
			else:
				#for the dialogue box 
				if self.dialogueBox2.whiteboxX <= self.mousex <=self.dialogueBox2.whiteboxX+self.dialogueBox2.endX:
					if self.dialogueBox2.whiteboxY + 20 >= self.mousey:
						
						for i in range(2):
							if 30*(i-1) <= self.dialogueBox2.whiteboxY- self.mousey <= 30*i:
								self.highlightBox = i
								self.dialogueBox2.highlightBox = i 
					else: 
						self.highlightBox = -1
						self.dialogueBox2.highlightBox = -1
				else: 
					self.highlightBox = -1
					self.dialogueBox2.highlightBox = -1
		elif self.mode == "New User":
			if self.back.isCollide():
				self.buttonColor = self.gray
				self.buttonColor1 = self.gray
				self.mode = "Startscreen"
			else:
				#for the dialogue box 
				if self.dialogueBox1.whiteboxX <= self.mousex <=self.dialogueBox1.whiteboxX+self.dialogueBox1.endX:
					if self.dialogueBox1.whiteboxY + 20 >= self.mousey:
						for i in range(6):
							if 30*(i-1) <= self.dialogueBox1.whiteboxY- self.mousey <= 30*i:
								self.highlightBox = i
								self.dialogueBox1.highlightBox = i 
					else: 
						self.highlightBox = -1
						self.dialogueBox1.highlightBox = -1
				else: 
					self.highlightBox = -1
					self.dialogueBox1.highlightBox = -1
		elif self.mode == "Math":
			if self.isLeft == True:
				self.mode = "Exercise"
			elif self.isRight == True: 
				self.mode = "Food"
			try:
				if self.logOut.isCollide():
					self.logOutButtonColor = self.gray
					self.init()
			except: pass
		elif self.mode == "Food":
			try:
				if self.back.isCollide():
					self.buttonColor = self.gray
					self.buttonColor1 = self.gray
					self.mode = "Math"
				if self.caloriesDialogue.whiteboxX <= self.mousex <=self.caloriesDialogue.whiteboxX+self.caloriesDialogue.endX:
					if self.caloriesDialogue.whiteboxY + 20 >= self.mousey:
						for i in range(2):
							if 30*(i-1) <= self.caloriesDialogue.whiteboxY- self.mousey <= 30*i:
									self.highlightBox = i
									self.caloriesDialogue.highlightBox = i 
					else: 
						self.highlightBox = -1
						self.caloriesDialogue.highlightBox = -1
				else: 
						self.highlightBox = -1
						self.caloriesDialogue.highlightBox = -1
			except: pass
		elif self.mode == "FoodSearch":
			try:
				if self.back.isCollide():
					self.buttonColor = self.gray
					self.mode = "Food"
				#for the dialogue box 
				if self.foodSearch.whiteboxX <= self.mousex <=self.foodSearch.whiteboxX+self.foodSearch.endX:
					if self.foodSearch.whiteboxY + 20 >= self.mousey:
						if -30 <= self.foodSearch.whiteboxY- self.mousey <= 0:
							self.highlightBox = 0
							self.foodSearch.highlightBox = 0
					else: 
						self.highlightBox = -1
						self.foodSearch.highlightBox = -1
				else: 
					self.highlightBox = -1
					self.foodSearch.highlightBox = -1
				if self.manual.isCollide():
					self.manualButton = self.gray
					self.mode = "FoodManual"
			except: pass
		elif self.mode == "FoodManual":
			try:
				if self.back.isCollide():
					self.buttonColor = self.gray
					self.buttonColor1 = self.gray
					self.mode = "FoodSearch"
				if self.nameOfFood.whiteboxX <= self.mousex <=self.nameOfFood.whiteboxX+self.nameOfFood.endX:
					if self.nameOfFood.whiteboxY + 20 >= self.mousey:
						for i in range(3):
							if 30*(i-1) <= self.nameOfFood.whiteboxY- self.mousey <= 30*i:
									self.highlightBox = i
									self.nameOfFood.highlightBox = i 
					else: 
						self.highlightBox = -1
						self.nameOfFood.highlightBox = -1
				else: 
					self.highlightBox = -1
					self.nameOfFood.highlightBox = -1
			except: pass
		elif self.mode == "HowHappyFood":
			try:
				if self.priceOfFood.whiteboxX <= self.mousex <=self.priceOfFood.whiteboxX+self.priceOfFood.endX:
					if self.priceOfFood.whiteboxY + 20 >= self.mousey:
						if 30*(-1) <= self.priceOfFood.whiteboxY- self.mousey <= 30:
								self.highlightBox = 0
								self.priceOfFood.highlightBox = 0
					else: 
						self.highlightBox = -1
						self.priceOfFood.highlightBox = -1
				else: 
						self.highlightBox = -1
						self.priceOfFood.highlightBox = -1
			except: pass
		elif self.mode == "Exercise":
			if self.back.isCollide():
				self.buttonColor = self.gray
				self.buttonColor1 = self.gray
				self.mode = "Math"
			try:
				if self.ExerciseCaloriesDialogue.whiteboxX <= self.mousex <=self.ExerciseCaloriesDialogue.whiteboxX+self.ExerciseCaloriesDialogue.endX:
					if self.ExerciseCaloriesDialogue.whiteboxY + 20 >= self.mousey:
						if 30*(-1) <= self.ExerciseCaloriesDialogue.whiteboxY- self.mousey <= 30:
								self.highlightBox = 0
								self.ExerciseCaloriesDialogue.highlightBox = 0
					else: 
						self.highlightBox = -1
						self.ExerciseCaloriesDialogue.highlightBox = -1
				else: 
						self.highlightBox = -1
						self.ExerciseCaloriesDialogue.highlightBox = -1
			except: pass
		elif self.mode == "FoodResults":
			if self.mainMenuButton.isCollide():
				self.mainMenuButtonColor= self.greenFont
				pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
				lastStars = self.profile[8]
				lastOperation = self.profile[10]
				star = (self.starSlider.getRatio()-1)/2
				currParameter = self.profile[6]
				newResults = parameterChange(star,lastStars,currParameter, lastOperation)	
				newParameter = newResults[0]
				newOperation = newResults[1]
				editParameter("FoodParameter",self.profile[1], newParameter)
				editStringParameter("LastFoodOperation", self.profile[1], newOperation)
				editParameter("LastFoodStars", self.profile[1], float(star))
				self.init("Math", self.profile, "Exercise", "Food")
		elif self.mode == "ExerciseSearch":
			if self.back.isCollide():
				self.mode = "Exercise"
			try:
				#for the dialogue box 
				if self.exerciseSearch.whiteboxX <= self.mousex <=self.exerciseSearch.whiteboxX+self.exerciseSearch.endX:
					if self.exerciseSearch.whiteboxY + 20 >= self.mousey:
						if -30 <= self.exerciseSearch.whiteboxY- self.mousey <= 0:
							self.highlightBox = 0
							self.exerciseSearch.highlightBox = 0
					else: 
						self.highlightBox = -1
						self.exerciseSearch.highlightBox = -1
				else: 
					self.highlightBox = -1
					self.exerciseSearch.highlightBox = -1
			except: pass
		elif self.mode == "ManualExercise":
			try:
				if self.back.isCollide():
					self.buttonColor = self.gray
					self.buttonColor1 = self.gray
					self.mode = "ExerciseSearch"
				if self.exerciseManualDialogue.whiteboxX <= self.mousex <=self.exerciseManualDialogue.whiteboxX+self.exerciseManualDialogue.endX:
					if self.exerciseManualDialogue.whiteboxY + 20 >= self.mousey:
						for i in range(3):
							if 30*(i-1) <= self.exerciseManualDialogue.whiteboxY- self.mousey <= 30*i:
									self.highlightBox = i
									self.exerciseManualDialogue.highlightBox = i 
					else: 
						self.highlightBox = -1
						self.exerciseManualDialogue.highlightBox = -1
				else: 
					self.highlightBox = -1
					self.exerciseManualDialogue.highlightBox = -1
			except: pass
		elif self.mode == "ExerciseResults":
			try:
				if self.desiredTimeDialogue.whiteboxX <= self.mousex <=self.desiredTimeDialogue.whiteboxX+self.desiredTimeDialogue.endX:
					if self.desiredTimeDialogue.whiteboxY + 20 >= self.mousey:
						if 30*(-1) <= self.desiredTimeDialogue.whiteboxY- self.mousey <= 30:
								self.highlightBox = 0
								self.desiredTimeDialogue.highlightBox = 0
					else: 
						self.highlightBox = -1
						self.desiredTimeDialogue.highlightBox = -1
				else: 
						self.highlightBox = -1
						self.desiredTimeDialogue.highlightBox = -1
			except: pass
			try:
				if self.mainMenuButton.isCollide():
					self.mainMenuButtonColor= self.greenFont
					pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
					lastStars = self.profile[9]
					lastOperation = self.profile[11]
					star = (self.exerciseStarSlider.getRatio()-1)/2
					currParameter = self.profile[7]
					newResults = parameterChange(star,lastStars,currParameter, lastOperation)	
					newParameter = newResults[0]
					newOperation = newResults[1]
					editParameter("ExerciseParameter",self.profile[1], newParameter)
					editStringParameter("LastExerciseOperation", self.profile[1], newOperation)
					editParameter("LastExerciseStars", self.profile[1], float(star))
					self.init("Math", self.profile, "Exercise", "Food")
			except: pass


	def mouseMotion(self, x, y):
		self.mousex = x
		self.mousey = y
		if self.mode == "Startscreen":
			self.drawSparks()
		#Mouse hovering over startscreen
			if y > self.height//2:
				if x < self.width//2:
					self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.highlightFont)
					self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.blueFont)
				else: 
					self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.highlightFont)
					self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.blueFont)
			else:
				self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.blueFont)
				self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.blueFont)
			
	
		elif self.mode == "Log in":
			#the following code highlights the button colors 
			try:
				if self.back.isCollide():
					self.buttonColor= self.highlightFont
				else: self.buttonColor= self.gray
			except: pass
			try:
				if self.submit1.isCollide():
					self.buttonColor1= self.highlightFont
				else: self.buttonColor1= self.gray
			except: pass
		elif self.mode == "Math":
			try:
				if self.logOut.isCollide():
					self.logOutButtonColor= self.highlightFont
				else: self.logOutButtonColor= self.gray
			except: pass
			self.drawSparks()
		#Mouse hovering over startscreen
			if y > self.height//2:
				if x < self.width//2:
					self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.highlightFont)
					self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.blueFont)
				else: 
					self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.highlightFont)
					self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.blueFont)
			else:
				self.exerciseSurface = (PygameGame.smalltitlefont).render(self.LeftWord, False, self.blueFont)
				self.foodSurface = (PygameGame.smalltitlefont).render(self.RightWord, False, self.blueFont)

		elif self.mode == "New User":
			#the following code highlights the button colors 
			try:
				if self.back.isCollide():
					self.buttonColor= self.highlightFont
				else: self.buttonColor= self.gray
			except: pass
			try:
				if self.submit.isCollide():
					self.buttonColor1= self.highlightFont
				else: self.buttonColor1= self.gray
			except: pass
		elif self.mode == "Exercise":
			try:
				if self.back.isCollide():
					self.buttonColor= self.highlightFont
				else: self.buttonColor= self.gray
			except: pass
		elif self.mode == "Food":
			try:
				if self.back.isCollide():
					self.buttonColor= self.highlightFont
				else: self.buttonColor= self.gray
			except: pass
			try:
				if self.foodSubmit.isCollide():
					self.foodSubmitColor= self.highlightFont
				else: self.foodSubmitColor= self.gray
			except: pass
		elif self.mode == "FoodSearch":
			try:
				if self.back.isCollide():
					self.buttonColor= self.highlightFont
				else: self.buttonColor= self.gray
			except: pass
			self.foodSearchSubmitColor = self.gray
			try:
				if self.manual.isCollide():
					self.manualButton= self.highlightFont
				else: self.manualButton= self.gray
			except: pass
		elif self.mode == "FoodManual":
			try:
				if self.back.isCollide():
					self.buttonColor= self.highlightFont
				else: self.buttonColor= self.gray
			except: pass
			try:
				if self.manualSubmit.isCollide():
					self.foodManualSubmitColor= self.highlightFont
				else: self.foodManualSubmitColor= self.gray
			except: pass
		elif self.mode == "HowHappyFood":
			try:
				if self.foodHappySubmit.isCollide():
					self.foodHappySubmitColor= self.highlightFont
				else: self.foodHappySubmitColor= self.gray
			except: pass
		elif self.mode == "FoodResults":
			if self.mainMenuButton.isCollide():
				self.mainMenuButtonColor= self.highlightFont
			else: self.mainMenuButtonColor= self.gray
		elif self.mode == "FoodSearch":
			try:
				if self.back.isCollide():
					self.buttonColor= self.highlightFont
				else: self.buttonColor= self.gray
			except: pass
			self.foodSearchSubmitColor = self.gray
			try:
				if self.exerciseManual.isCollide():
					self.manualButton= self.highlightFont
				else: self.manualButton= self.gray
			except: pass
		elif self.mode == "HowHappyExercise":
			try:
				if self.exerciseHappySubmit.isCollide():
					self.exerciseSubmitColor= self.highlightFont
				else: self.exerciseSubmitColor= self.gray
			except: pass

	def mouseDrag(self, x, y):
		if self.mode == "Startscreen" or self.mode == "Math":
			#this is for setting the volume on the slider
			if 1000 >= x >= 700 and y < 45:
				if x< 820:
					self.volumeSlider = 820
				elif x> 920:
					self.volumeSlider = 920
				else: self.volumeSlider = x
				volume = (self.volumeSlider-820)/100
				pygame.mixer.music.set_volume(volume)
		elif self.mode == "Food":
			try:
				if self.healthySlider.startx -50 <= x <= self.healthySlider.startx + self.healthySlider.length+50:
					if self.healthySlider.starty -50 <= y <= self.healthySlider.starty + 50:
						if x< self.healthySlider.startx:
							self.healthySliderLocation = self.healthySlider.startx
							self.healthySliderNumber = 0
						elif x> self.healthySlider.startx + self.healthySlider.length:
							self.healthySliderLocation = self.healthySlider.startx + self.healthySlider.length
							self.healthySliderNumber = 10.0
						else: 
							self.healthySliderLocation = x
							self.healthySliderNumber = self.healthySlider.getRatio()-1
				if self.satsfiedSlider.startx -50 <= x <= self.satsfiedSlider.startx + self.satsfiedSlider.length+50:
					if self.satsfiedSlider.starty -50 <= y <= self.satsfiedSlider.starty + 50:
						if x< self.satsfiedSlider.startx:
							self.satisfiedSliderLocation = self.satsfiedSlider.startx
							self.satisfiedSliderNumber = 0
						elif x> self.satsfiedSlider.startx + self.satsfiedSlider.length:
							self.satisfiedSliderLocation = self.satsfiedSlider.startx + self.satsfiedSlider.length
							self.satisfiedSliderNumber = 10.0
						else: 
							self.satisfiedSliderLocation = x
							self.satisfiedSliderNumber = self.satsfiedSlider.getRatio()-1
			except: pass
		elif self.mode == "FoodManual":
			try:
				if self.foodSlider.startx -50 <= x <= self.foodSlider.startx + self.foodSlider.length+50:
					if self.foodSlider.starty -50 <= y <= self.foodSlider.starty + 50:
						if x< self.foodSlider.startx:
							self.foodSliderLocation = self.foodSlider.startx
							self.foodSliderNumber = 0
						elif x> self.foodSlider.startx + self.foodSlider.length:
							self.foodSliderLocation = self.foodSlider.startx + self.foodSlider.length
							self.foodSliderNumber = 10.0
						else: 
							self.foodSliderLocation = x
							self.foodSliderNumber = self.foodSlider.getRatio()-1
			except: pass
		elif self.mode == "HowHappyFood":
			try:
				if self.foodHappySlider.startx -50 <= x <= self.foodHappySlider.startx + self.foodHappySlider.length+50:
					if self.foodHappySlider.starty -50 <= y <= self.foodHappySlider.starty + 50:
						if x< self.foodHappySlider.startx:
							self.foodHappySliderLocation = self.foodHappySlider.startx
							self.foodHappySliderNumber = 0
						elif x> self.foodHappySlider.startx + self.foodHappySlider.length:
							self.foodHappySliderLocation = self.foodHappySlider.startx + self.foodHappySlider.length
							self.foodHappySliderNumber = 10.0
						else: 
							self.foodHappySliderLocation = x
							self.foodHappySliderNumber = self.foodHappySlider.getRatio()-1
			except: pass
		elif self.mode == "FoodResults":
			try:
				if self.starSlider.startx -50 <= x <= self.starSlider.startx + self.starSlider.length+50:
					if self.starSlider.starty -50 <= y <= self.starSlider.starty + 50:
						if x< self.starSlider.startx:
							self.starSliderLocation = self.starSlider.startx
							self.starSliderNumber = 0
						elif x> self.starSlider.startx + self.starSlider.length:
							self.starSliderLocation = self.starSlider.startx + self.starSlider.length
							self.starSliderNumber = 5.0
						else: 
							self.starSliderLocation = x
							self.starSliderNumber = (self.starSlider.getRatio()-1)/2
			except: pass
		elif self.mode == "Exercise":
			try:
				if self.healthySlider.startx -50 <= x <= self.healthySlider.startx + self.healthySlider.length+50:
					if self.healthySlider.starty -50 <= y <= self.healthySlider.starty + 50:
						if x< self.healthySlider.startx:
							self.healthySliderLocation = self.healthySlider.startx
							self.healthySliderNumber = 0
						elif x> self.healthySlider.startx + self.healthySlider.length:
							self.healthySliderLocation = self.healthySlider.startx + self.healthySlider.length
							self.healthySliderNumber = 10.0
						else: 
							self.healthySliderLocation = x
							self.healthySliderNumber = self.healthySlider.getRatio()-1
			except: pass
		elif self.mode == "HowHappyExercise":
			try:
				if self.exerciseHappySlider.startx -50 <= x <= self.exerciseHappySlider.startx + self.exerciseHappySlider.length+50:
					if self.exerciseHappySlider.starty -50 <= y <= self.exerciseHappySlider.starty + 50:
						if x< self.exerciseHappySlider.startx:
							self.exerciseHappySlider = self.exerciseHappySlider.startx
							self.foodHappySliderNumber = 0
						elif x> self.exerciseHappySlider.startx + self.exerciseHappySlider.length:
							self.foodHappySliderLocation = self.exerciseHappySlider.startx + self.exerciseHappySlider.length
							self.foodHappySliderNumber = 10.0
						else: 
							self.foodHappySliderLocation = x
							self.foodHappySliderNumber = self.exerciseHappySlider.getRatio()-1
			except: pass
		elif self.mode == "ExerciseResults":
			try:
				if self.exerciseStarSlider.startx -50 <= x <= self.exerciseStarSlider.startx + self.exerciseStarSlider.length+50:
					if self.exerciseStarSlider.starty -50 <= y <= self.exerciseStarSlider.starty + 50:
						if x< self.exerciseStarSlider.startx:
							self.starSliderLocation = self.exerciseStarSlider.startx
							self.starSliderNumber = 0
						elif x> self.exerciseStarSlider.startx + self.exerciseStarSlider.length:
							self.starSliderLocation = self.exerciseStarSlider.startx + self.exerciseStarSlider.length
							self.starSliderNumber = 5.0
						else: 
							self.starSliderLocation = x
							self.starSliderNumber = (self.exerciseStarSlider.getRatio()-1)/2
			except: pass

	def keyPressed(self, keyCode, modifier):
		if self.mode == "New User":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = (code)
			if (code) == "backspace":
				self.dialogueBox1.deleteWriting(5-self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.dialogueBox1.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.dialogueBox1.highlightBox += 1
			elif code == "space":
				self.dialogueBox1.addWriting(" ",5- self.highlightBox)
			if pygame.key.name(keyCode) not in string.printable:
				return
			self.dialogueBox1.addWriting(letter,5- self.highlightBox)
		elif self.mode == "Log in":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = (code)
			if (code) == "backspace":
				self.dialogueBox2.deleteWriting(1-self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.dialogueBox2.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.dialogueBox2.highlightBox += 1
			elif code == "space":
				self.dialogueBox2.addWriting(" ",1- self.highlightBox)
			if pygame.key.name(keyCode) not in string.printable:
				return
			self.dialogueBox2.addWriting(letter,1- self.highlightBox)
		elif self.mode == "Food":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = code
			if (code) == "backspace":
				self.caloriesDialogue.deleteWriting(1-self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.caloriesDialogue.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.caloriesDialogue.highlightBox += 1
			elif code == "space":
				self.caloriesDialogue.addWriting(" ",1- self.highlightBox)
			if pygame.key.name(keyCode) not in string.printable:
				return
			if len(self.caloriesDialogue.writingText[1-self.highlightBox][0]) < 4:
				self.caloriesDialogue.addWriting(letter,1-self.highlightBox)
		elif self.mode == "FoodSearch":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = (code)
			if (code) == "backspace":
				self.foodSearch.deleteWriting(self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.foodSearch.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.foodSearch.highlightBox += 1
			elif code == "space":
				self.foodSearch.addWriting(" ",0)
			if pygame.key.name(keyCode) not in string.printable:
				return
			if len(self.foodSearch.writingText[self.highlightBox][0]) < 46:
				self.foodSearch.addWriting(letter,self.highlightBox)
		elif self.mode == "FoodManual":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = (code)
			if (code) == "backspace":
				self.nameOfFood.deleteWriting(2-self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.nameOfFood.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.nameOfFood.highlightBox += 1
			elif code == "space":
				self.nameOfFood.addWriting(" ",2- self.highlightBox)
			if pygame.key.name(keyCode) not in string.printable:
				return
			if len(self.nameOfFood.writingText[2- self.highlightBox][0]) < 39:
				self.nameOfFood.addWriting(letter,2-self.highlightBox)
		elif self.mode == "HowHappyFood":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = code
			if (code) == "backspace":
				self.priceOfFood.deleteWriting(self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.priceOfFood.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.priceOfFood.highlightBox += 1
			elif code == "space":
				self.priceOfFood.addWriting(" ",self.highlightBox)
			if pygame.key.name(keyCode) not in string.printable:
				return
			if len(self.priceOfFood.writingText[self.highlightBox][0]) < 4:
				self.priceOfFood.addWriting(letter,self.highlightBox)
		elif self.mode == "Exercise":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = code
			if (code) == "backspace":
				self.ExerciseCaloriesDialogue.deleteWriting(self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.ExerciseCaloriesDialogue.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.ExerciseCaloriesDialogue.highlightBox += 1
			elif code == "space":
				self.ExerciseCaloriesDialogue.addWriting(" ",self.highlightBox)
			if pygame.key.name(keyCode) not in string.printable:
				return
			if len(self.ExerciseCaloriesDialogue.writingText[self.highlightBox][0]) < 4:
				self.ExerciseCaloriesDialogue.addWriting(letter,self.highlightBox)
		elif self.mode == "ExerciseSearch":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = (code)
			if (code) == "backspace":
				self.exerciseSearch.deleteWriting(self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.exerciseSearch.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.exerciseSearch.highlightBox += 1
			elif code == "space":
				self.foodSearch.addWriting(" ",0)
			if pygame.key.name(keyCode) not in string.printable:
				return
			if len(self.exerciseSearch.writingText[self.highlightBox][0]) < 46:
				self.exerciseSearch.addWriting(letter,self.highlightBox)
		elif self.mode == "ManualExercise":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = code
			if (code) == "backspace":
				self.exerciseManualDialogue.deleteWriting(1-self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.exerciseManualDialogue.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.exerciseManualDialogue.highlightBox += 1
			elif code == "space":
				self.exerciseManualDialogue.addWriting(" ",1- self.highlightBox)
			if pygame.key.name(keyCode) not in string.printable:
				return
			if len(self.exerciseManualDialogue.writingText[1-self.highlightBox][0]) < 30:
				self.exerciseManualDialogue.addWriting(letter,1-self.highlightBox)
		elif self.mode == "ExerciseResults":
			code = (pygame.key.name(keyCode))
			if self.highlightBox == -1:
				return 
			#these are the shifts
			if modifier == 1 or modifier == 2:
				letter = findShift(code)
			else: letter = code
			if (code) == "backspace":
				self.desiredTimeDialogue.deleteWriting(self.highlightBox)
			elif code == "tab" or code == "return" or code == "down" or code == "right":
				self.highlightBox -= 1
				self.desiredTimeDialogue.highlightBox -= 1
			elif code == "up" or code == "left":
				self.highlightBox += 1
				self.desiredTimeDialogue.highlightBox += 1
			elif code == "space":
				self.desiredTimeDialogue.addWriting(" ",self.highlightBox)
			if pygame.key.name(keyCode) not in string.printable:
				return
			if len(self.desiredTimeDialogue.writingText[self.highlightBox][0]) < 4:
				self.desiredTimeDialogue.addWriting(letter,self.highlightBox)

	def keyReleased(self, keyCode, modifier):
		pass

	def timerFired(self, dt):
		if self.mode == "Startscreen":
			self.drawNonMouseSparks()
			#changes location of the sparks
			for location in self.nonMouseSparks:
				if location[1][1] <0 or location[1][0] <0:
					self.nonMouseSparks.remove(location)
				direction = random.choice([1,3])
				directionx = random.randint(1,3)
				location[1][1] -= self.speed*direction
				location[1][0] -= self.speed*directionx
		#this is all for the startscreen background
			maxNumberOfPhotos = 31 #there are only 31 photos
			self.image_number+=1
			if self.image_number == maxNumberOfPhotos:
				self.image_number = 1
			self.image = pygame.image.load('image/background-%d (dragged).tiff' %\
			self.image_number).convert()
			self.w,self.h = self.image.get_size() #size fo the image
			self.image = pygame.transform.scale(self.image, (int(self.w/self.scale),int(self.h/self.scale)))
			#this is a random time we choose to pop off the sparks
			if self.time%2 ==0:
				if len(self.sparks) > 0:
					#we leave a certain amount of sparks on the board
					while len(self.sparks) >60:
						self.sparks.pop(0)
		elif self.mode == "Math":
			self.drawNonMouseSparks()
			#changes location of the sparks
			for location in self.nonMouseSparks:
				if location[1][1] <0 or location[1][0] <0:
					self.nonMouseSparks.remove(location)
				direction = random.choice([1,3])
				directionx = random.randint(1,3)
				location[1][1] -= self.speed*direction
				location[1][0] -= self.speed*directionx
		#this is all for the startscreen background
			maxNumberOfPhotos = 31 #there are only 31 photos
			self.image_number+=1
			if self.image_number == maxNumberOfPhotos:
				self.image_number = 1
			self.image = pygame.image.load('image/background-%d (dragged).tiff' %\
			self.image_number).convert()
			self.w,self.h = self.image.get_size() #size fo the image
			self.image = pygame.transform.scale(self.image, (int(self.w/self.scale),int(self.h/self.scale)))
			#this is a random time we choose to pop off the sparks
			if self.time%2 ==0:
				if len(self.sparks) > 0:
					#we leave a certain amount of sparks on the board
					while len(self.sparks) >60:
						self.sparks.pop(0)
	def redrawAll(self, screen):
		if self.mode == "Startscreen" or self.mode == "Math":
			screen.blit(self.volumeSurface,(700,20))
			self.volumeButton = Slider(screen, 100, 820, 33,self.volumeSlider)
			self.volumeButton.drawSlider()
		if self.mode == "Startscreen":
			screen.blit(self.image, (self.width/10,self.height/2))
			screen.blit(self.image, (11*self.width/20,self.height/2))
			screen.blit(self.titlesurface,(130,120))
			screen.blit(self.exerciseSurface,(self.text1,self.textHeight))
			screen.blit(self.foodSurface,(self.text2,self.textHeight))
			screen.blit(self.versionSurface,(350,310))
			for sparks in self.nonMouseSparks:
				if sparks[1][1] < 0:
					continue
				pygame.draw.rect(screen, sparks[0],sparks[1])
			for spark in self.sparks:
				pygame.draw.rect(screen, spark[0],spark[1])

		elif self.mode == "Log in":
			self.back = Button(100, 50, 100,70, self.buttonColor, "Back",20, 7)
			self.back.drawBox(screen)
			self.dialogueBox2.drawBox(screen)
			self.submit1 = Button(100, 50, 500,330, self.buttonColor1, "Log in",13, 6)
			self.submit1.drawBox(screen)
			self.dialogueBox2.drawText(screen, "Log in", -3,160,-25, PygameGame.smalltitlefont, (255,255,255))
			if self.password == False:
				self.dialogueBox2.drawText(screen, "Password is incorrect", 3,150,-25)
			elif self.username == False:
				self.dialogueBox2.drawText(screen, "Username does not exist", 3,140,-25)
		elif self.mode == "New User":
			self.back = Button(100, 50, 100,70, self.buttonColor, "Back",20, 7)
			self.back.drawBox(screen)
			self.dialogueBox1.drawBox(screen)
			self.submit = Button(100, 50, 500,500, self.buttonColor1, "Submit",7, 6)
			self.submit.drawBox(screen)
			self.back.drawBox(screen)
			self.dialogueBox2.drawText(screen, "New User", -3,100,-25, PygameGame.smalltitlefont, (255,255,255))
			if self.passwordsMatch == False:
				self.dialogueBox1.drawText(screen, "Passwords don't match!", 7,140,-25)
			elif self.complete == False:
				self.dialogueBox1.drawText(screen, "Entries not complete!", 7,150,-25)
			elif self.age == False:
				self.dialogueBox1.drawText(screen, "Age and weight must be numbers!", 7,110,-25)
		elif self.mode == "Math":
			self.logOut = Button(115, 50, 500,270, self.logOutButtonColor, "Log Out",11, 7)
			self.logOut.drawBox(screen)
			screen.blit(self.image, (self.width/10,self.height/2))
			screen.blit(self.image, (11*self.width/20,self.height/2))
			screen.blit(self.titlesurface,(self.width//2-161 - 17*(len(self.name)),170))
			screen.blit(self.exerciseSurface,(self.text1-35,self.textHeight))
			screen.blit(self.foodSurface,(self.text2+70,self.textHeight))
			for sparks in self.nonMouseSparks:
				if sparks[1][1] < 0:
					continue
				pygame.draw.rect(screen, sparks[0],sparks[1])
			for spark in self.sparks:
				pygame.draw.rect(screen, spark[0],spark[1])
		elif self.mode == "Food":
			self.back = Button(100, 50, 100,70, self.buttonColor, "Back",20, 7)
			self.back.drawBox(screen)
			calories = Text(100,165, "How many calories are you willing to eat?", 20)
			money = Text(100,200, "How much money do you want to spend?", 20)
			calories.write(screen)
			money.write(screen)
			self.caloriesDialogue.drawBox(screen)
			self.healthySlider = Slider(screen, 200, self.width//3, 355, self.healthySliderLocation)
			self.healthySlider.drawSlider()
			healthy = Text(100,300, "How important is it for you to be healthy in this meal? (10 being very important)", 20)
			healthy.write(screen)
			healthyNumber = Text(self.width//3-50, 345, "%0.1f" % self.healthySliderNumber, 20)
			healthyNumber.write(screen)

			self.satsfiedSlider = Slider(screen, 200, self.width//3, 485, self.satisfiedSliderLocation)
			self.satsfiedSlider.drawSlider()
			satisfied = Text(100,430, "How important is it for you to feel satisfied from this meal? (10 being very important) ", 20)
			satisfied.write(screen)
			satsfiedNumber = Text(self.width//3-50, 475, "%0.1f" % self.satisfiedSliderNumber, 20)
			satsfiedNumber.write(screen)

			discrete = Text(100,550, "Is your food divisble? (i.e. do you want some of each food?)", 20)
			discrete.write(screen)
			self.yesButton = Button(100,50,350,625,self.buttonColor2,"Yes", 25, 8)
			self.yesButton.drawBox(screen)
			self.noButton = Button(100,50,460,625,self.buttonColor3,"No", 25, 8)
			self.noButton.drawBox(screen)

			self.foodSubmit = Button(100, 50, self.width//2,725, self.foodSubmitColor, "Submit",8, 6)
			self.foodSubmit.drawBox(screen)

			if self.caloriesInteger == False:
				calorieError = Text(self.width//2-200, self.height-45, "Calories must be an integer between 0 and 9999!", 20)
				calorieError.write(screen)
			elif self.moneyInteger == False:
				moneyError = Text(self.width//2 -190, self.height-45, "Money must be an integer between 0 and 9999!", 20)
				moneyError.write(screen)
			elif self.discreteAnswer == False:
				discreteError = Text(self.width//2 - 160, self.height-45, "Please select if it is discrete or not.", 20)
				discreteError.write(screen)

		elif self.mode == "Exercise":

			self.back = Button(100, 50, 100,70, self.buttonColor, "Back",20, 7)
			self.back.drawBox(screen)
			calories = Text(100,185, "How many calories do you want to burn?", 20)
			calories.write(screen)
			self.ExerciseCaloriesDialogue.drawBox(screen)

			self.healthySlider = Slider(screen, 200, self.width//3, 355, self.healthySliderLocation)
			self.healthySlider.drawSlider()
			healthy = Text(100,300, "How important is it for you to enjoy this workout? (10 being very important)", 20)
			healthy.write(screen)
			healthyNumber = Text(self.width//3-50, 345, "%0.1f" % self.healthySliderNumber, 20)
			healthyNumber.write(screen)

			discrete = Text(70,450, "Do you want to do multiple workouts? (meaning, do you want to split your time between workouts?)", 20)
			discrete.write(screen)
			self.yesButton = Button(100,50,350,525,self.buttonColor2,"Yes", 25, 8)
			self.yesButton.drawBox(screen)
			self.noButton = Button(100,50,460,525,self.buttonColor3,"No", 25, 8)
			self.noButton.drawBox(screen)

			self.exerciseSubmit = Button(100, 50, self.width//2,725, self.foodSubmitColor, "Submit",8, 6)
			self.exerciseSubmit.drawBox(screen)
			
			if self.caloriesInteger == False:
				calorieError = Text(self.width//2-200, self.height-45, "Calories must be an integer between 0 and 9999!", 20)
				calorieError.write(screen)
			elif self.discreteAnswer == False:
				discreteError = Text(self.width//2 - 160, self.height-45, "Please select if it is discrete or not.", 20)
				discreteError.write(screen)				



		elif self.mode == "FoodSearch":
			self.manual = Button(200, 50, self.width//2+40,270, self.manualButton, "Enter Manually",12, 7)
			self.manual.drawBox(screen)
			self.back = Button(100, 50, 100,70, self.buttonColor, "Back",20, 7)
			self.foodSearch.drawBox(screen)
			self.back.drawBox(screen)
			foodSearch = Text(110, 185, "Search for a food:", 20)
			foodSearch.write(screen)
			self.submitFoodSearch = Button(100, 50, 870,200, self.foodSearchSubmitColor, "Submit",7, 6)
			self.submitFoodSearch.drawBox(screen)
			foodnumbers = (len(self.foods)+1)
			if foodnumbers ==3:
				foodnumbers = 2
			titleOfScreen = Text(430, 100, "Food item %d" % foodnumbers, 40)
			titleOfScreen.write(screen)
			if self.sorry:
				sorry = Text(80, 300, "Please type out name completely. If not listed below, enter it manually. (We will store it for next time). ", 20)
				sorry.write(screen)
			if self.getDictionaryResults(self.foodSearch.writingText[0][0]) == False:
				mean = Text(80, 350, "Suggestions (click one): ", 20)
				mean.write(screen) 
				noresults = Text(80, 400, "No results. Please enter manually.", 20)
				noresults.write(screen)
				return
			mean = Text(80, 350, "Suggestions (click one):  ", 20)
			mean.write(screen)
			food = self.getDictionaryResults(self.foodSearch.writingText[0][0])
			self.foodList = []
			self.temporaryFoods = []
			if len(food) > 12:
				food = food[:24:2]
			for entry in food:
				self.foodList.append("%0.1f %s of %s, %d calories" % (entry[1][2], entry[1][1],entry[0], entry[1][0]))
				self.temporaryFoods.append(entry)
			self.suggestionsText = []
			for writing in range(len(self.foodList)):
				self.suggestionsText += [Text(80,400 + 30*writing,self.foodList[writing], 20, (0,183,245))]
			for theword in self.suggestionsText:
				theword.write(screen)

		elif self.mode == "ExerciseSearch":
			self.exerciseManual = Button(200, 50, self.width//2+70,270, self.manualButton, "Enter Manually",12, 7)
			self.exerciseManual.drawBox(screen)
			self.back = Button(100, 50, 100,70, self.buttonColor, "Back",20, 7)
			self.exerciseSearch.drawBox(screen)
			self.back.drawBox(screen)
			exerciseSearch = Text(110, 185, "Search for an exercise:", 20)
			exerciseSearch.write(screen)
			self.submitExerciseSearch = Button(100, 50, 910,200, self.exerciseSubmitColor, "Submit",7, 6)
			self.submitExerciseSearch.drawBox(screen)
			
			exercisenumbers = (len(self.exercises)+1)
			if exercisenumbers ==6:
				exercisenumbers = 2
			if exercisenumbers >= 3:
				showResults = Text(180, 70, "Click here if you don't want to add any more items-->", 20)
				showResults.write(screen)
				self.exerciseResultsbutton = Button(200, 50, 775,70, self.greenFont, "Final Step",20, 7)
				self.exerciseResultsbutton.drawBox(screen)
			titleOfScreen = Text(430, 100, "Exercise item %d" % exercisenumbers, 40)
			titleOfScreen.write(screen)
			if self.sorry:
				sorry = Text(80, 300, "Please type out name completely. If not listed below, enter it manually. (We will store it for next time). ", 20)
				sorry.write(screen)
			if self.exerciseGetDictionaryResults(self.exerciseSearch.writingText[0][0]) == False:
				mean = Text(80, 350, "Suggestions (click one): ", 20)
				mean.write(screen) 
				noresults = Text(80, 400, "No results. Please enter manually.", 20)
				noresults.write(screen)
				return
			mean = Text(80, 350, "Suggestions (click one):  ", 20)
			mean.write(screen)
			exercise = self.exerciseGetDictionaryResults(self.exerciseSearch.writingText[0][0])
			self.exerciseList = []
			self.temporaryExercise = []
			if len(exercise) > 12:
				exercise = exercise[:24:2]
			weight = self.profile[5]
			#these are numbers profivded by the database
			if weight <155:
				weightIndex = 0
			elif weight < 180:
				weightIndex = 1
			elif weight < 205:
				weightIndex = 2
			else: weightIndex = 3
			for entry in exercise:
				self.exerciseList.append("%s, %d calories per hour" % (entry[0], entry[1][weightIndex]))
				self.temporaryExercise.append([entry[0],entry[1][weightIndex]/60])
			self.suggestionsText = []
			for writing in range(len(self.exerciseList)):
				self.suggestionsText += [Text(80,400 + 30*writing,self.exerciseList[writing], 20, (0,183,245))]
			for theword in self.suggestionsText:
				theword.write(screen)

		elif self.mode == "FoodManual":
			self.back = Button(100, 50, 100,70, self.buttonColor, "Back",20, 7)
			self.back.drawBox(screen)
			name = Text(80,200, "What is the name of your food item?:",20)
			name.write(screen)
			self.nameOfFood.drawBox(screen)
			calories = Text(80,230, "How many calories are in one serving?:",20)
			calories.write(screen)
			serving = Text(80,260, "How big is one serving? (e.g. 1 cup or 1 piece):",20)
			serving.write(screen)
			self.foodSlider = Slider(screen, 200, self.foodSliderstart, 385, self.foodSliderLocation)
			self.foodSlider.drawSlider()
			foodNumber = Text(self.foodSliderstart-50, 375, "%0.1f" % self.foodSliderNumber, 20)
			foodNumber.write(screen)
			howHealthy = Text(self.foodSliderstart-275, 375, "How healthy is it?:", 20)
			howHealthy.write(screen)
			title = Text(self.width//2 -180, 125, "Enter Manually", 50, (0,183,245))
			title.write(screen)
			self.manualSubmit = Button(100, 50, 500,500, self.foodManualSubmitColor, "Submit",7, 6)
			self.manualSubmit.drawBox(screen)
			if self.manualCalories == False:
				calorieError = Text(self.width//2-200, self.height//2+150, "Calories must be an integer between 0 and 9999!", 20)
				calorieError.write(screen)
			elif self.manualServing == False:
				moneyError = Text(self.width//2 -190, self.height//2+150, "Serving has to be in the form 'Digit + Measure', like 1 oz.", 20)
				moneyError.write(screen)
			elif self.manualIncomplete == False:
				discreteError = Text(self.width//2 - 160, self.height//2+150, "Entries not complete! ", 20)
				discreteError.write(screen)

		elif self.mode == "HowHappyFood":
			ask = Text(50, self.height//2 +50, "How happy would 1 serving of '%s' make you?" % self.foods[-1][0], 20)
			ask.write(screen)
			self.foodHappySlider = Slider(screen, 200, self.foodHappySliderStart, 535, self.foodHappySliderLocation)
			self.foodHappySlider.drawSlider()
			foodHappyNumber = Text(self.foodHappySliderStart-40, 525, "%0.1f" % self.foodHappySliderNumber, 20)
			foodHappyNumber.write(screen)
			self.foodHappySubmit = Button(100, 50, self.width//2,650, self.foodHappySubmitColor, "Submit",7, 6)
			self.foodHappySubmit.drawBox(screen)
			self.priceOfFood.drawBox(screen)
			cost = Text(50, 200, "How much does 1 serving of '%s' cost?" % self.foods[-1][0], 20)
			cost.write(screen)
			if self.moneyNotInteger:
				error = Text(self.width//2-200, 600, "Money must be an integer between 0 and 9999!", 20)
				error.write(screen)

		elif self.mode == "FoodResults":
			parameter = self.profile[6]
			phrase = runFoodsForAnimation(self.foods,self.information,self.happy,self.moneyAmount, parameter)
			thefirstphrase = Text(100, 100, "%s" % phrase[0], 25)
			thefirstphrase.write(screen)
			thesecondphrase = Text(100, 140, "%s" % phrase[1], 25)
			thesecondphrase.write(screen)
			self.starSlider = Slider(screen, 200, self.starSliderstart, 485, self.starSliderLocation)
			self.starSlider.drawSlider()
			starQuestion = Text(self.starSliderstart-250, 385, "How helpful was this? (from 0 to 5)", 20)
			starQuestion.write(screen)
			starNumber = Text(self.starSliderstart-50, 475, "%0.1f" % self.starSliderNumber, 20)
			starNumber.write(screen)
			self.mainMenuButton = Button(170, 50, self.width//2,self.height-100, self.buttonColor, "Main Menu",20, 7)
			self.mainMenuButton.drawBox(screen)

		elif self.mode == "HowHappyExercise":
			ask = Text(50, self.height//2 +50, "How happy would an hour of '%s' make you?" % self.exercises[-1][0], 20)
			ask.write(screen)
			self.exerciseHappySlider = Slider(screen, 200, self.foodHappySliderStart, 535, self.foodHappySliderLocation)
			self.exerciseHappySlider.drawSlider()
			exerciseHappyNumber = Text(self.foodHappySliderStart-40, 525, "%0.1f" % self.foodHappySliderNumber, 20)
			exerciseHappyNumber.write(screen)
			self.exerciseHappySubmit = Button(100, 50, self.width//2,650, self.exerciseSubmitColor, "Submit",7, 6)
			self.exerciseHappySubmit.drawBox(screen)
		elif self.mode == "ManualExercise":
			self.exerciseManualDialogue.drawBox(screen)
			ask1 = Text(50, 210, "What is the name of your exercise?", 20)
			ask2 = Text(50, 235, "How many calories per hour do you burn with this exercise?", 20)
			ask1.write(screen)
			ask2.write(screen)
			self.manualSubmit = Button(100, 50, self.width//2,350, self.foodManualSubmitColor, "Submit",7, 6)
			self.manualSubmit.drawBox(screen)
			if self.notValidNumber:
				error = Text(80, 435, "Calories must be an integer!", 20)
				error.write(screen)
		elif self.mode == "ExerciseResults":
			mincal = int(self.ExerciseCaloriesDialogue.writingText[0][0])
			maxcalPerMin = 0
			for exercise in self.exercises:
				if exercise[1] > maxcalPerMin:
					maxcalPerMin = exercise[1]
			minimum_time = roundHalfUp(mincal/maxcalPerMin)
			ask = Text(50, self.height//2 +150, "How much time would you like to spend? (Must be larger than %0.1f to meet calorie requirement)" % minimum_time, 20)
			ask.write(screen)
			self.desiredTimeDialogue.drawBox(screen)
			try: int(self.desiredTimeDialogue.writingText[0][0])
			except: 
				if self.desiredTimeDialogue.writingText[0][0] == "":
					return
				else: 
					error = Text(50, 610, "Time must be an integer", 20)
					error.write(screen)
					return
			if self.desiredTimeDialogue.writingText[0][0] == "":
				pass
			elif int(self.desiredTimeDialogue.writingText[0][0]) < minimum_time:
				self.timeError = True 
			else: self.timeError = False 
			if self.timeError:
				error = Text(50, 610, "Time must be an integer greater than %0.1f" % minimum_time, 20)
				error.write(screen)
			else: 
				self.exerciseResultsSubmit = Button(100, 50, self.width//2,750, self.exerciseResultsSubmitcolor, "Submit",7, 6)
				self.exerciseResultsSubmit.drawBox(screen)
			try:
				self.starQuestion.write(screen)
				self.starNumber = Text(self.starSliderstart-50, 475, "%0.1f" % self.starSliderNumber, 20)
				self.starNumber.write(screen)
				self.mainMenuButton.drawBox(screen)
				self.exerciseStarSlider = Slider(screen, 200, self.starSliderstart, 485, self.starSliderLocation)
				self.exerciseStarSlider.drawSlider()
				for sentence in range(len(self.splitResults)):
					phrase = self.splitResults[sentence]
					Text(100,100+20*sentence, phrase, 20).write(screen)
			except: pass
			
		
	def isKeyPressed(self, key):
		return self._keys.get(key, False)

	def __init__(self, width=1000, height=800, fps=80,title="Deciduo Kamyar"):
		self.width = width
		self.height = height
		self.fps = fps
		self.title = title
		self.bgColor = (0, 0, 0)
		pygame.init()

	def run(self):

		clock = pygame.time.Clock()
		screen = pygame.display.set_mode((self.width, self.height))
		# set the title of the window
		pygame.display.set_caption(self.title)

		# stores all the keys currently being held down
		self._keys = dict()

		# call game-specific initialization
		self.init()
		self.playing = True
		while self.playing:
			self.time = clock.tick(self.fps)
			self.timerFired(self.time)
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					self.mousePressed(*(event.pos))
				elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
					self.mouseReleased(*(event.pos))
				elif (event.type == pygame.MOUSEMOTION and
					  event.buttons == (0, 0, 0)):
					self.mouseMotion(*(event.pos))
				elif (event.type == pygame.MOUSEMOTION and
					  event.buttons[0] == 1):
					self.mouseDrag(*(event.pos))
				elif event.type == pygame.KEYDOWN:
					self._keys[event.key] = True
					self.keyPressed(event.key, event.mod)
				elif event.type == pygame.KEYUP:
					self._keys[event.key] = False
					self.keyReleased(event.key, event.mod)
				elif event.type == pygame.QUIT:
					self.playing = False
			screen.fill(self.bgColor)
			self.redrawAll(screen)
			pygame.display.flip()

		pygame.quit()
	#draws the mouse sparks in the home screen
	def drawSparks(self):
		locationx = self.mousex
		locationy = self.mousey
		width = 2
		#random location of spark
		interval = random.randint(0,10)
		#these are the differnet colors (magenta to blue)
		color = (255,215,0)
		self.sparks.append([color, [locationx+width,locationy+interval,width, width]])
		self.sparks.append([color, [locationx-interval,locationy-width,width, width]])
		self.sparks.append([color, [locationx+interval,locationy,width, width]])
		self.sparks.append([color, [locationx,locationy-interval,width, width]])
		self.sparks.append([color, [locationx-interval,locationy-interval,width, width]])
		self.sparks.append([color, [locationx+interval,locationy+interval,width, width]])
	def drawNonMouseSparks(self): 
		locationx = random.randint(self.width//10,9*self.width//10)
		locationy = random.randint(self.height//2, 2*self.height//3)
		width = 2
		#random location of spark
		interval = random.randint(0,10)
		#these are the differnet colors (magenta to blue)
		color1 = random.choice([(190, 6, 159),(89,2,75),(238,41,241),(0,183,245)])
		color2 = random.choice([(190, 6, 159),(89,2,75),(238,41,241),(0,183,245)])
		color3 = random.choice([(190, 6, 159),(89,2,75),(238,41,241),(0,183,245)])
		color4 = random.choice([(190, 6, 159),(89,2,75),(238,41,241),(0,183,245)])
		color5 = random.choice([(190, 6, 159),(89,2,75),(238,41,241),(0,183,245)])
		color6 = random.choice([(190, 6, 159),(89,2,75),(238,41,241),(0,183,245)])
		self.nonMouseSparks.append([color1, [locationx+width,locationy+interval,width, width]])
		self.nonMouseSparks.append([color2, [locationx-interval,locationy-width,width, width]])
		self.nonMouseSparks.append([color3, [locationx+interval,locationy,width, width]])
		self.nonMouseSparks.append([color4, [locationx,locationy-interval,width, width]])
		self.nonMouseSparks.append([color5, [locationx-interval,locationy-interval,width, width]])
		self.nonMouseSparks.append([color6, [locationx+interval,locationy+interval,width, width]])

	def foodMath(self):
		#calories, money, healthy, satisfied, discrete  
		self.information = [self.caloriesDialogue.writingText[0][0],self.caloriesDialogue.writingText[1][0],self.healthySlider.getRatio(),self.satsfiedSlider.getRatio(),self.discrete]
	def exerciseMath(self):
		#note: healthy slider actually represents how happy it makes you
		self.information = [self.ExerciseCaloriesDialogue.writingText[0][0],self.healthySlider.getRatio(),self.discrete]

	def isLegalSubmit(self):
		try: 
			int(self.caloriesDialogue.writingText[0][0])
			self.caloriesInteger = True
		except: 
			return "caloriesInteger"
		try: 
			int(self.caloriesDialogue.writingText[1][0])
			self.moneyInteger = True
		except: return "moneyInteger"
		if self.discrete == None:
			return "discreteAnswer"
		return "complete"

	def isLegalExerciseSubmit(self):
		try: 
			int(self.ExerciseCaloriesDialogue.writingText[0][0])
			self.caloriesInteger = True
		except: 
			return "caloriesInteger"
		if self.discrete == None:
			return "discreteAnswer"
		return "complete"
	def isLegalManualSubmit(self):
		for i in range(3):
			if self.nameOfFood.writingText[i][0] == "":
				return "incomplete" 
		try: int(self.nameOfFood.writingText[1][0])
		except: return "calories"
		if self.nameOfFood.writingText[2][0][0] not in string.digits:
			return "serving"
		onlynumbers = True
		anyspace = True
		for letter in range(len(self.nameOfFood.writingText[2][0])):
			if self.nameOfFood.writingText[2][0][letter] in string.ascii_letters:
				onlynumbers = False
			if self.nameOfFood.writingText[2][0][letter] == " ":
				anyspace = False
		if onlynumbers or anyspace:
			return "serving"
		return True 

	def isLegalManualSubmitExercise(self):
		try: int(self.exerciseManualDialogue.writingText[1][0])
		except: return False
		return True
	#only searches exact results 
	def normalDictionary(self,search):
		search = search.lower()
		results = []
		for food in FOOD.dictionary_of_food:
			if search in food.lower():
				results.append([food, FOOD.dictionary_of_food[food]])
		if results == []:
			return False
		return results

	#only searches exact results 
	def normalExerciseDictionary(self, search):
		search = search.lower()
		results = []
		for exercise in EXERCISE.dictionary_of_exercise:
			if search in exercise.lower():
				results.append([exercise, EXERCISE.dictionary_of_exercise[exercise]])
		if results == []:
			return False
		return results


	def getDictionaryResults(self, search):
		search = search.lower()
		searchWords = []
		results = []
		for food in FOOD.dictionary_of_food:
			if search in food.lower():
				results.append([food, FOOD.dictionary_of_food[food]])
		#search by word 
		for letter in range(len(search)): 
			if search[letter] == " ":
				searchWords += [letter]
		#this looks for the individual words 
		if len(searchWords) >0:
			results.extend(searching(search,searchWords))
		if results == []:
			return False
		else: 
			self.suggestions = True
			return results
	def exerciseGetDictionaryResults(self, search):
		search = search.lower()
		searchWords = []
		results = []
		for exercise in EXERCISE.dictionary_of_exercise:
			if search in exercise.lower():
				results.append([exercise, EXERCISE.dictionary_of_exercise[exercise]])
		#search by word 
		for letter in range(len(search)): 
			if search[letter] == " ":
				searchWords += [letter]
		#this looks for the individual words 
		if len(searchWords) >0:
			results.extend(searching(search,searchWords))
		if results == []:
			return False
		else: 
			self.suggestions = True
			return results

	def addToDictionary(self):
		name = self.nameOfFood.writingText[0][0]
		calories = int(self.nameOfFood.writingText[1][0])
		servings = self.nameOfFood.writingText[2][0]
		healthy = self.foodSlider.getRatio()

		serving_word = ""
		for letter in range(len(servings)):
			if servings[letter] in string.ascii_letters:
				serving_number = int(servings[0:letter-1])
				serving_word = servings[letter:]
				break
		food_entry = [name, (calories, serving_word, serving_number,healthy)]
		self.foods.append(food_entry)
		addToFoodDictionary(food_entry)
	def addToExerciseDictionary(self):
		name= self.exerciseManualDialogue.writingText[0][0]
		calories = int(self.exerciseManualDialogue.writingText[1][0])
		weightCalories = self.createWeightCalories(calories)
		dictElement = [name, tuple(weightCalories)]
		finalAddToExerciseDictionary(dictElement)
		
	def createWeightCalories(self,calories):
		weightCalories = [None,None,None,None]
			#this is weight
		if self.profile[5]<=155:
			weightCalories[0] = calories
		elif self.profile[5] <= 180:
			weightCalories[1] = calories
		elif self.profile[5] <= 205:
			weightCalories[2] = calories
		else: weightCalories[3] = calories
		additional = 40 
		#converts all nones to proper calories
		while None in weightCalories:
			for element in range(len(weightCalories)):
				if weightCalories[element] ==None:
					#edge case first element
					if element == 0:
						if weightCalories[element+1] != None:
							weightCalories[0] = \
							int(weightCalories[element+1]) - additional
					#edge case last element
					elif element == 3:
						if weightCalories[element-1] != None:
							weightCalories[3] = \
							int(weightCalories[element-1]) + additional
					else: 
						if weightCalories[element-1] != None:
							weightCalories[element] = \
							int(weightCalories[element-1]) + additional
						elif weightCalories[element+1] != None:
							weightCalories[element] = \
							int(weightCalories[element+1]) - additional
		return weightCalories

def splitLinesOfSentence(sentence):
	count = 0
	splitSentences = []
	lastIndex = 0
	for letter in range(len(sentence)):
		if sentence[letter] == " ":
			count +=1
		if count == 10:
			splitSentences.append(sentence[lastIndex:letter])
			print(sentence[lastIndex:letter])
			lastIndex = letter
			count = 0
		if letter == len(sentence) -1:
			splitSentences.append(sentence[lastIndex:])
	return splitSentences

def finalAddToExerciseDictionary(exercise):
	#finds where to add it in the dictionary
	with open("Databases/Final_Databases/Exercise_Database_Final.py") as file:  
		data = file.readlines() 
	dictionary = data[1]
	index = data[1].index("{")
	#creates entry
	entryName = exercise[0]
	entryTuple = exercise[1]
	dictionary = data[0]+ dictionary[:index+1] + "'%s':%s," % \
	(str(entryName), str(entryTuple))+ dictionary[index+1:]
	#writes newdictionary
	file = open("Databases/Final_Databases/Exercise_Database_Final.py", "w")
	file.write(dictionary) 
	
	file.close() 
	#reloads dictionary
	imp.reload(EXERCISE)


def main():
	game = PygameGame()
	game.run()

if __name__ == '__main__':
	main()

