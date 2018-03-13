from TermProjectFinalMath import *
import pygame
import random

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
        self.volume = 0.2
        self.volumeSlider = 820+self.volume*100
        self.titlesurface = (PygameGame.titlefont).render('Deciduo', False, (236, 34, 243))
        self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.blueFont)
        self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.blueFont)
        self.versionSurface = (PygameGame.smallerfont).render('Version 3.1 By Kamyar Ghiam', False, (255,255,255))
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
                self.buttonColor1= self.greenFont
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
                
            else:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/NonClick.wav"))
        elif self.mode == "New User":
            if self.back.isCollide():
                self.buttonColor= self.greenFont
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
            elif self.submit.isCollide():
                self.buttonColor1= self.greenFont
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
                
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
        elif self.mode == "New User":
            if self.back.isCollide():
                self.buttonColor = self.gray
                self.buttonColor1 = self.gray
                self.mode = "Startscreen"

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
        pass

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
            self.back = Button(screen,100, 50, 100,70, self.buttonColor, "Back",23, 0)
            self.back.drawBox()
            self.diologueBox2 = DialogueBox(screen, 500, 200, 500,300, (238,41,241), "Username", 10, 10, "Password",textsize = 20, boxshifty = 5, whiteboxnumber = 2)
            self.diologueBox2.drawBox()
            self.submit1 = Button(screen,100, 50, 500,330, self.buttonColor1, "Submit",10, 0)
            self.submit1.drawBox()

        elif self.mode == "New User":
            self.back = Button(screen,100, 50, 100,70, self.buttonColor, "Back",23, 0)
            self.back.drawBox()
            self.diologueBox1 = DialogueBox(screen, 500, 300, 500,400, (238,41,241), "Username", 10, 10, "Password", "Confirm ^","Name", "Age", "Weight",textsize = 20, boxshifty = 5, whiteboxnumber = 6)
            self.diologueBox1.drawBox()
            self.submit = Button(screen,100, 50, 500,500, self.buttonColor1, "Submit",10, 0)
            self.submit.drawBox()
            self.back.drawBox()

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
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
        self.button = Button(self.screen, 20, 20, self.boxLocation, self.starty, self.color1, "",0,0)
        self.button.drawBox()
    def drawSlider(self):
        self.drawRectangle()
        self.drawButton()
    def isCollide(self):
        #sees if mouse collides with button
        return self.button.isCollide()
        
class Button(object):
    def __init__(self, screen, lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, textsize = 27, textcolor = (0,0,0)):
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
        self.screen = screen
        self.textcolor = textcolor
        #black text color default
        self.titlesurface = (self.font).render(text, False, textcolor)
        #self.text is inherited for the dialogue box
        self.textlength = len(text)*10
        self.width = 3
        self.shiftx = textshiftx
        self.shifty = textshifty
    def drawRectangle(self):
        pygame.draw.rect(self.screen, self.color,(self.startx,self.starty,self.lengthx, self.lengthy))
    def drawShadow(self):
        pygame.draw.rect(self.screen, (153,153,153),(self.startx, self.starty + self.lengthy-self.width,self.lengthx, self.width))
        pygame.draw.rect(self.screen, (153,153,153),(self.startx+self.lengthx-self.width, self.starty,self.width, self.lengthy))
    def drawText(self, titlesurface = None, shift = 0):
        if titlesurface ==None:
            titlesurface = self.titlesurface
        else: titlesurface = (self.font).render(titlesurface, False, self.textcolor)
        self.screen.blit(titlesurface,(self.startx+self.shiftx,self.starty+self.shifty + shift*30))
    def drawBox(self):
        self.drawRectangle()
        self.drawShadow()
        self.drawText()
    def isCollide(self):
        #sees if mouse collides with button
        mousex = pygame.mouse.get_pos()[0]
        mousey = pygame.mouse.get_pos()[1]
        return abs(mousex-self.centerx) < self.lengthx//2 and\
        abs(mousey-self.centery) < self.lengthy//2

class DialogueBox(Button):
    def __init__(self, screen, lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, *args, textsize = 27, textcolor = (0,0,0), boxshiftx=0, boxshifty=0, whiteboxnumber = 1):
        super().__init__(screen, lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, textsize, textcolor)
        self.boxshiftx = boxshiftx
        self.boxshifty = boxshifty
        self.whiteboxnumber = whiteboxnumber
        self.othertext = args
    def drawWhiteBox(self, shift):
        #where the white box should be 
        location = (self.startx + self.textsize + self.shiftx + self.textlength + self.boxshiftx, self.starty + self.shifty + self.boxshifty + shift, self.lengthx - (self.textsize + self.shiftx+self.textlength)-20, 20)
        pygame.draw.rect(self.screen, (255,255,255),location)
    def drawBox(self):
        super().drawBox()
        for i in range(self.whiteboxnumber):
            self.drawWhiteBox(i*30)
        count = 0
        for text in self.othertext:
            count +=1
            self.drawText(text, count)


def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()