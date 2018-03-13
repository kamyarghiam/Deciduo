from TermProjectFinalMath import *
import pygame


#runExercise()
#runFood()

#The framework for pygame taken from the GitHub offered by the 112 TA's
#Code within the framework is original
class PygameGame(object):
    pygame.font.init()
    def init(self):
    #this is all for the gif background
        self.myfont = pygame.font.Font('AppleGothic.ttf', 230)
        self.image_number = 1
        #gif taken from https://giphy.com/gifs/wallpaper-3o6vXTpomeZEyxufGU
        self.image = pygame.image.load('image/background-%d (dragged).tiff' %\
        self.image_number)
        self.scale = 1.5 #how to resize image 
        self.w,self.h = self.image.get_size() #size fo the image
        self.textsurface = (self.myfont).render('Deciduo', False, (236, 34, 243))

    def mousePressed(self, x, y):
        pass

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
    #this is all for the startscreen background
        maxNumberOfPhotos = 31 #there are only 31 photos
        self.image_number+=1
        if self.image_number == maxNumberOfPhotos:
            self.image_number = 1
        self.image = pygame.image.load('image/background-%d (dragged).tiff' %\
        self.image_number)
        self.w,self.h = self.image.get_size() #size fo the image
        self.image = pygame.transform.scale(self.image, (int(self.w/self.scale),int(self.h/self.scale)))
        
    def redrawAll(self, screen):
        screen.blit(self.image, (self.width/10,self.height/2))
        screen.blit(self.image, (11*self.width/20,self.height/2))
        screen.blit(self.textsurface,(200,170))


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
            time = clock.tick(self.fps)
            self.timerFired(time)
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

def main():
    game = PygameGame()
    game.run()

if __name__ == '__main__':
    main()