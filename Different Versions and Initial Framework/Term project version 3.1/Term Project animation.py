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
        self.titlesurface = (PygameGame.titlefont).render('Deciduo', False, (236, 34, 243))
        self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.blueFont)
        self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.blueFont)
        #This is an excerpt from "Acres"-Same Gellaitry-(Purchased from Amazon)
        pygame.mixer.music.load("Music&Sounds/AcresEdited.wav")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.2)
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
        
    def mousePressed(self, x, y):
        if self.mode == "Startscreen":
            if y > self.height//2:
                if x < self.width//2:
                    self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.greenFont)
                    self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.blueFont)
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
                else: 
                    self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.greenFont)
                    self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.blueFont)
                    #I made this recording myself
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
                
            else:
                self.exerciseSurface = (PygameGame.smalltitlefont).render('Log In', False, self.blueFont)
                self.foodSurface = (PygameGame.smalltitlefont).render('New User', False, self.blueFont)
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/NonClick.wav"))
        elif self.mode == "Log in" or self.mode == "New User":
            if self.back.isCollide():
                self.buttonColor= self.greenFont
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/MyRecordingClick.wav"))
            else:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Music&Sounds/NonClick.wav"))
                
    def mouseReleased(self, x, y):
        if self.mode == "Startscreen":
            if y > self.height//2:
                if x < self.width//2:
                    self.mode = "Log in"
                else: 
                    self.mode = "New User"
        elif self.mode == "Log in" or self.mode == "New User":
            if self.back.isCollide():
                self.mode = "Startscreen"

    def mouseMotion(self, x, y):
        self.mousex = x
        self.mousey = y
        if self.mode == "Startscreen":
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
            self.drawSparks()
            
    
        elif self.mode == "Log in" or self.mode == "New User":
            if self.back.isCollide():
                self.buttonColor= self.highlightFont
            else: self.buttonColor= self.gray

    def mouseDrag(self, x, y):
        pass

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
            for spark in self.sparks:
                pygame.draw.rect(screen, spark[0],spark[1])
            for sparks in self.nonMouseSparks:
                if sparks[1][1] < 0:
                    continue
                pygame.draw.rect(screen, sparks[0],sparks[1])
        elif self.mode == "Log in" or self.mode == "New User":
            self.back = Button(screen,100, 50, 100,70, self.buttonColor, "Back",23, 0)
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
    
    def drawDiaglogueBox(self,screen): 
        white = (250,250,250)
        color = (204,204,204)
        width = 200
        height = 20
        #draws the box around it 
        location = (self.width/2- width, self.height/2- height, 2*width, 2*height)
        pygame.draw.rect(screen, color,location)
        #draws the white box wher you type
        location = (self.width/2- width/2, self.height/2- height/2, width, height)
        pygame.draw.rect(screen, white,location)
        
class Button(object):
    def __init__(self, screen, lengthx, lengthy, centerx, centery, color, text,textshiftx,textshifty, textsize = 27, textcolor = (0,0,0)):
        self.font = pygame.font.Font('fonts/TitilliumWeb-Regular.ttf', textsize)
        self.startx = centerx-lengthx//2
        self.starty = centery-lengthy//2
        self.centerx = centerx
        self.centery= centery
        self.lengthx = lengthx
        self.lengthy = lengthy
        self.originalColor = color
        self.color = color 
        self.screen = screen
        #black text color default
        self.titlesurface = (self.font).render(text, False, textcolor)
        self.width = 3
        self.shiftx = textshiftx
        self.shifty = textshifty
    def drawRectangle(self):
        pygame.draw.rect(self.screen, self.color,(self.startx,self.starty,self.lengthx, self.lengthy))
    def drawShadow(self):
        pygame.draw.rect(self.screen, (153,153,153),(self.startx, self.starty + self.lengthy-self.width,self.lengthx, self.width))
        pygame.draw.rect(self.screen, (153,153,153),(self.startx+self.lengthx-self.width, self.starty,self.width, self.lengthy))
    def drawText(self):
        self.screen.blit(self.titlesurface,(self.startx+self.shiftx,self.starty+self.shifty))
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
    

def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()