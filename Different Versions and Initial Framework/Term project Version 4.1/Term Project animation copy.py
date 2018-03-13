#Kamyar Ghiam 15-112 Term Project "Deciduo" Animation Framework

#from TermProjectFinalMath import *
import pygame
import random
import string
from Supporting_Documents.Shift_Letters import findShift
from Databases.Final_Databases.SQL_Database.SQL_Support import *


#runExercise()
#runFood()

#The framework for pygame taken from the GitHub offered by the 112 TA's
#Code within the framework is original
class PygameGame(object):
    pygame.font.init()
    titlefont = pygame.font.Font('fonts/Capture_it.ttf', 200)
    smalltitlefont = pygame.font.Font('fonts/Capture_it.ttf', 60)
    smallerfont = pygame.font.Font('fonts/Capture_it.ttf', 20)
    def init(self):
    ###this is all for the startpage##
        self.image_number = 1
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
        self.volumeSlider = 820+self.volume*100
        self.titlesurface = (PygameGame.titlefont).render('Deciduo', False, (236, 34, 243))
        self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.blueFont)
        self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.blueFont)
        self.versionSurface = (PygameGame.smallerfont).render('Version 4.1 By Kamyar Ghiam', False, (255,255,255))
        self.volumeSurface = (PygameGame.smallerfont).render('Volume :', False, (255,255,255))
        #This is an excerpt from "Acres"-Same Gellaitry-(Purchased from Amazon)
        pygame.mixer.music.load("Music&Sounds/AcresEdited.wav")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(self.volume)
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
    #########################
        self.mode = "Startscreen"
        self.gray = (250,250,250)
        self.buttonColor = self.gray
        self.buttonColor1 = self.gray
        #highlights the diologue box
        self.highlightBox = -1
        self.diologueBox1 = DialogueBox(500, 300, 500,400, (238,41,241), "Username", 10, 10, "Password", "Confirm ^","Name", "Age", "Weight",textsize = 20, boxshifty = 5, whiteboxnumber = 6, highlightBox = self.highlightBox)
        self.diologueBox2 = DialogueBox(500, 200, 500,300, (238,41,241), "Username", 10, 10, "Password",textsize = 20, boxshifty = 5, whiteboxnumber = 2, highlightBox = self.highlightBox)
        # for new user
        self.complete = True
        self.passwordsMatch = True
        #for log in 
        self.username = True
        self.password = True
        
    def mousePressed(self, x, y):
        if self.mode == "Startscreen":
            self.isLeft = False
            self.isRight = False
            if y > self.height//2:
                if x < self.width//2:
                    self.isLeft = True
                    self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.greenFont)
                    self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.blueFont)
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
                else: 
                    self.isRight = True
                    self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.greenFont)
                    self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.blueFont)
                    #I made this recording myself
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
                
            else:
                self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.blueFont)
                self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.blueFont)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/NonClick.wav"))
        elif self.mode == "Log in":
            if self.back.isCollide():
                self.buttonColor= self.greenFont
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
            elif self.submit1.isCollide():
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
                if self.diologueBox2.accessDatabase() == "password":
                    self.buttonColor1=self.redFont
                    self.username = True
                    self.password = False
                elif self.diologueBox2.accessDatabase() == "username":
                    self.buttonColor1=self.redFont
                    self.password = True
                    self.username = False
                else:
                    self.password = True
                    self.username = True
                    self.buttonColor1= self.greenFont
                    self.profile = self.diologueBox2.accessDatabase()

        elif self.mode == "New User":
            if self.back.isCollide():
                self.buttonColor= self.greenFont
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
            elif self.submit.isCollide():
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
                if self.diologueBox1.addToDatabase() == "complete":
                    self.buttonColor1= self.greenFont
                    self.complete = True
                    self.passwordsMatch = True
                    self.mode = "Log in"
                    screen = pygame.display.set_mode((self.width, self.height))
                    self.redrawAll(screen)
                else:
                    self.buttonColor1=self.redFont
                    if self.diologueBox1.addToDatabase() == "passwords":
                        self.complete = True
                        self.passwordsMatch = False
                    if self.diologueBox1.addToDatabase() == "incomplete":
                        self.passwordsMatch = True
                        self.complete = False
                
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
                if self.diologueBox2.whiteboxX <= self.mousex <=self.diologueBox2.whiteboxX+self.diologueBox2.endX:
                    if self.diologueBox2.whiteboxY + 20 >= self.mousey:
                        
                        for i in range(2):
                            if 30*(i-1) <= self.diologueBox2.whiteboxY- self.mousey <= 30*i:
                                self.highlightBox = i
                                self.diologueBox2.highlightBox = i 
                    else: 
                        self.highlightBox = -1
                        self.diologueBox2.highlightBox = -1
                else: 
                    self.highlightBox = -1
                    self.diologueBox2.highlightBox = -1
        elif self.mode == "New User":
            if self.back.isCollide():
                self.buttonColor = self.gray
                self.buttonColor1 = self.gray
                self.mode = "Startscreen"
            else:
                #for the dialogue box 
                if self.diologueBox1.whiteboxX <= self.mousex <=self.diologueBox1.whiteboxX+self.diologueBox1.endX:
                    if self.diologueBox1.whiteboxY + 20 >= self.mousey:
                        for i in range(6):
                            if 30*(i-1) <= self.diologueBox1.whiteboxY- self.mousey <= 30*i:
                                self.highlightBox = i
                                self.diologueBox1.highlightBox = i 
                    else: 
                        self.highlightBox = -1
                        self.diologueBox1.highlightBox = -1
                else: 
                    self.highlightBox = -1
                    self.diologueBox1.highlightBox = -1

    def mouseMotion(self, x, y):
        self.mousex = x
        self.mousey = y
        if self.mode == "Startscreen":
            self.drawSparks()
        #Mouse hovering over startscreen
            if y > self.height//2:
                if x < self.width//2:
                    self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.highlightFont)
                    self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.blueFont)
                else: 
                    self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.highlightFont)
                    self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.blueFont)
            else:
                self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.blueFont)
                self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.blueFont)
            
    
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

    def mouseDrag(self, x, y):
        if self.mode == "Startscreen":
            #this is for setting the volume on the slider
            if 1000 >= x >= 700 and y < 45:
                if x< 820:
                    self.volumeSlider = 820
                elif x> 920:
                    self.volumeSlider = 920
                else: self.volumeSlider = x
                volume = (self.volumeSlider-820)/100
                pygame.mixer.music.set_volume(volume)

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
                self.diologueBox1.deleteWriting(5-self.highlightBox)
            elif code == "tab" or code == "return" or code == "down" or code == "right":
                self.highlightBox -= 1
                self.diologueBox1.highlightBox -= 1
            elif code == "up" or code == "left":
                self.highlightBox += 1
                self.diologueBox1.highlightBox += 1
            if pygame.key.name(keyCode) not in string.printable:
                return
            self.diologueBox1.addWriting(letter,5- self.highlightBox)
        elif self.mode == "Log in":
            code = (pygame.key.name(keyCode))
            if self.highlightBox == -1:
                return 
            #these are the shifts
            if modifier == 1 or modifier == 2:
                letter = findShift(code)
            else: letter = (code)
            if (code) == "backspace":
                self.diologueBox2.deleteWriting(1-self.highlightBox)
            elif code == "tab" or code == "return" or code == "down" or code == "right":
                self.highlightBox -= 1
                self.diologueBox2.highlightBox -= 1
            elif code == "up" or code == "left":
                self.highlightBox += 1
                self.diologueBox2.highlightBox += 1
            if pygame.key.name(keyCode) not in string.printable:
                return
            self.diologueBox2.addWriting(letter,1- self.highlightBox)

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
    def redrawAll(self, screen):
        if self.mode == "Startscreen":
            screen.blit(self.image, (self.width/10,self.height/2))
            screen.blit(self.image, (11*self.width/20,self.height/2))
            screen.blit(self.titlesurface,(130,120))
            screen.blit(self.exerciseSurface,(self.text1,self.textHeight))
            screen.blit(self.foodSurface,(self.text2,self.textHeight))
            screen.blit(self.versionSurface,(350,310))
            screen.blit(self.volumeSurface,(700,20))
            for sparks in self.nonMouseSparks:
                if sparks[1][1] < 0:
                    continue
                pygame.draw.rect(screen, sparks[0],sparks[1])
            self.volumeButton = Slider(screen, 100, 820, 33,self.volumeSlider)
            self.volumeButton.drawSlider()
            for spark in self.sparks:
                pygame.draw.rect(screen, spark[0],spark[1])

        elif self.mode == "Log in":
            self.back = Button(100, 50, 100,70, self.buttonColor, "Back",23, 0)
            self.back.drawBox(screen)
            self.diologueBox2.drawBox(screen)
            self.submit1 = Button(100, 50, 500,330, self.buttonColor1, "Submit",10, 0)
            self.submit1.drawBox(screen)
            self.diologueBox2.drawText(screen, "Log in", -3,160,-25, PygameGame.smalltitlefont, (255,255,255))
            if self.password == False:
                self.diologueBox2.drawText(screen, "Password is incorrect", 3,150,-25)
            elif self.username == False:
                self.diologueBox2.drawText(screen, "Username does not exist", 3,140,-25)
        elif self.mode == "New User":
            self.back = Button(100, 50, 100,70, self.buttonColor, "Back",23, 0)
            self.back.drawBox(screen)
            self.diologueBox1.drawBox(screen)
            self.submit = Button(100, 50, 500,500, self.buttonColor1, "Submit",10, 0)
            self.submit.drawBox(screen)
            self.back.drawBox(screen)
            self.diologueBox2.drawText(screen, "New User", -3,100,-25, PygameGame.smalltitlefont, (255,255,255))
            if self.passwordsMatch == False:
                self.diologueBox1.drawText(screen, "Passwords don't match!", 7,140,-25)
            elif self.complete == False:
                self.diologueBox1.drawText(screen, "Entries not complete!", 7,150,-25)
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
        playing = True
        while playing:
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
                    playing = False
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
    
class Slider(object):
    def __init__(self, screen, length, startx, starty,boxLocation):
        self.screen = screen
        self.length = length
        self.startx = startx
        self.starty = starty
        self.color = (255,255,255)
        self.color1 = (170,170,170)
        self.boxLocation = boxLocation
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
        
class Button(object):
    def __init__(self,lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, textsize = 27, textcolor = (0,0,0)):
        self.font = pygame.font.Font('fonts/TitilliumWeb-Regular.ttf', textsize)
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

class DialogueBox(Button):
    def __init__(self, lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, *args, textsize = 27, textcolor = (0,0,0), boxshiftx=0, boxshifty=0, whiteboxnumber = 1, highlightBox= -1):
        super().__init__(lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, textsize, textcolor)
        self.boxshiftx = boxshiftx
        self.boxshifty = boxshifty
        self.whiteboxnumber = whiteboxnumber
        self.othertext = args
        self.highlightBox = highlightBox
        self.writingText = [[""],[""],[""],[""],[""],[""]]
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
            self.drawText(screen, text, count)
        count = 0
        for writing in range(len(self.writingText)):
            text = self.writingText[writing][0]
            if writing == 1 or writing == 2:
                self.drawText(screen, "*"*len(text), count, self.textlength +30, -1)
            else:
                self.drawText(screen, text, count, self.textlength +30, -1)
            count +=1
    def addWriting(self, text, place):
        if len(self.writingText[place][0]) > 28:
            return
        self.writingText[place][0] = self.writingText[place][0] + text

    def deleteWriting(self, place):
        self.writingText[place][0] = self.writingText[place][0][:-1]

    def addToDatabase(self):
        complete = True
        for entry in self.writingText:
            if entry[0] == "":
                complete = False
        if complete == False:
            return "incomplete"
        elif self.writingText[1][0] != self.writingText[2][0]:
            return "passwords"
        #this adds entries to database
        addNewEntry(self.writingText[0][0],self.writingText[1][0],\
        self.writingText[2][0], self.writingText[3][0], self.writingText[4][0])
        return "complete"
    def accessDatabase(self):
        username = self.writingText[0][0]
        password = self.writingText[1][0]
        dataList = accessData()
        for entry in dataList:
            if username == entry[1]:
                if password == entry[2]:
                    return self.writingText[0][0]
                else: return "password"
        return "username"
          
def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()