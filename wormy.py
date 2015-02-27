import pygame, sys
import random, time
from pygame.locals import *

global FOOD, HEAD, setDisplay, WORM

WORM =[]
#           R    G   B
RED    = ( 255 , 0,  0  )
GREEN  = (  0 , 255, 0  )
BLUE   = (  0 ,  0, 255 )
DARK   = (  0 ,  0,  0  )
WHITE  = ( 255, 255,255 )
SILVER = ( 192, 192,192 )
AQUA   = (  0,  255,255 )
FUCHSIA= (255,   0, 255 )
GRAY   = (128, 128, 128 )
LIME   = (  0, 255,   0 )
MAROON = (128,   0,   0 )
NAVY   = (  0,   0, 128 )
OLIVE  = (128, 128,   0 )
PURPLE = (128,   0, 128 )
TEAL   = (  0, 128, 128 )
YELLOW = (255, 255,   0 )

W_SCREEN = 700            # Size of Windows
H_SCREEN = 500
W_FRAMEGAME = 600         # Size of Range Frame Game
H_FRAMEGAME = 400
CELL = 20

POSITION_SCORE = ((W_SCREEN + W_FRAMEGAME) / 2, (H_SCREEN + H_FRAMEGAME) / 2)
POSITION_POINT = ((W_SCREEN + W_FRAMEGAME) / 2, (H_SCREEN + H_FRAMEGAME) / 2 + CELL)

FPS = 15

BOUNDARY = 5
NUMBER_HEAD = 4
HEAD = NUMBER_HEAD - 1   # Head of Snake
TAIL = 0                 # Tail of Snake



DIRECTION_TABLE = {
    "RIGHT" :   (CELL,0),
    "LEFT"  :   (-CELL,0),
    "UP"    :   (0,-CELL),
    "DOWN"  :   (0,CELL)
}

fpsClock = pygame.time.Clock()

def randomN(Bdry = 0):                                ### The boundary of randomize with the edge of screen
    return [(random.randint(0 + Bdry, W_FRAMEGAME/CELL - Bdry) * CELL, random.randint(0 + Bdry,H_FRAMEGAME/CELL - Bdry)*CELL)]
    ### Random the co-ordinate fit with the CELL size

def initEnv(WORM):
    global HEAD, setDisplay

    pygame.mixer.music.load("tetris.mp3")              # This is the background music
    pygame.mixer.music.play(-1, 1.0)

    HEAD = NUMBER_HEAD - 1

    WORM += randomN(HEAD - TAIL + 2)                     ### I use the tuple to store the status (x,y), Head - Tail + 2 is just the boundary, It's not vital
    for i in range(TAIL+1, HEAD + 1):
        WORM += [(WORM[i-1][0]+CELL, WORM[i-1][1])]     ### The next cell of WORM will be the previous cell

def moveWorm(WORM, direction):
    global HEAD
    for i in range(TAIL, HEAD ):
        WORM[i] = WORM[i+1]              ### Move the previous status to previous cell

    x = direction[0] + WORM[HEAD][0]
    y = direction[1] + WORM[HEAD][1]
    ### WORM HEAD will have new status from user
    WORM[HEAD] = (x,y)
#    print WORM

def addPart(WORM, direction):
    x = direction[0] + WORM[TAIL][0]
    y = direction[1] + WORM[TAIL][1]
    WORM.insert(TAIL,(x, y))

def checkEaten(WORM, direction):
    global FOOD, HEAD
#     print "Direction ", direction
#    print "Head ", HEAD
#    print "FOOD ", FOOD

    x = WORM[HEAD][0] + direction[0]
    y = WORM[HEAD][1] + direction[1]
#    print (x,y)
    if (x, y) == FOOD[0]:
        HEAD += 1
#        addPart(WORM, direction)
        WORM.append(FOOD[0])
        FOOD = randomN(1)
        return True
    else:
#        print False
        return False

def drawRect(SURFACE, object):
    pygame.draw.rect(SURFACE, GREEN, (object[0][0],object[0][1],CELL, CELL))

def drawWorm(SURFACE, WORM):
    for i in WORM:
        pygame.draw.rect(SURFACE, RED, (i[0],i[1] , CELL, CELL))

def drawGrid(SURFACE, W_FRAMEGAME, H_FRAMEGAME, CELL, color):
    for i in range(0,H_FRAMEGAME, CELL):
        pygame.draw.line(SURFACE, color, (0,i),(W_FRAMEGAME,i), 1)      ### Draw horizontal line
    for i in range(0,W_FRAMEGAME, CELL):
        pygame.draw.line(SURFACE, color, (i,0),(i, H_FRAMEGAME), 1)    ### Draw vertical line

     ### Draw boundary edge of game
    pygame.draw.line(SURFACE, color, (0, H_FRAMEGAME ), (W_FRAMEGAME , H_FRAMEGAME ), 1) # horizon
    pygame.draw.line(SURFACE, color, (W_FRAMEGAME , 0), (W_FRAMEGAME , H_FRAMEGAME ), 1) # vertical

def drawText(text, size, color, position):       ### bgColor is the background Color
    fontObj = pygame.font.Font('freesansbold.ttf', size)
    textSurfaceObj = fontObj.render(str(text), True, color)
    textRectObj = textSurfaceObj.get_rect()
    textRectObj.center = position
    return (textSurfaceObj, textRectObj)

def hitWall(WORM):
    if WORM[HEAD][0] >= W_FRAMEGAME or WORM[HEAD][0] < 0 or WORM[HEAD][1] >= H_FRAMEGAME or WORM[HEAD][1] < 0:
        return True
    else:
        return False

def eatSelf(WORM):
    for i in WORM[TAIL : (HEAD - 4)]:
        if WORM[HEAD] == i:
            return True
    return False

def drawInit(WORM, FOOD):
    drawGrid(setDisplay, W_FRAMEGAME, H_FRAMEGAME, CELL, DARK)     ### Draw the WORM state
    drawWorm(setDisplay, WORM)
#    drawRect(setDisplay, FOOD)

    coord = (FOOD[0][0], FOOD[0][1])
    APPLE_IMG = image('apple.png', setDisplay, (CELL, CELL), coord)
    APPLE_IMG.draw()


def gameOver(WORM):
    global HEAD
    if hitWall(WORM) == True or eatSelf(WORM) == True:
        return True
    else:
        return False

def terminate():
    pygame.quit()
    sys.exit()

class image():
    def __init__(self, dir, SURFACE, scale, coord):    # coord is co-ordinate of image drawed on
        self.img = pygame.image.load(dir)
        self.SURFACE = SURFACE
        self.scale = scale
        self.coord = coord
    def draw(self):
        self.img = pygame.transform.scale(self.img, self.scale)
        self.SURFACE.blit(self.img, self.coord)


class sound():
    def __init__(self, soundFile):
        self.sound = pygame.mixer.Sound(soundFile)
    def play(self):     ### second is the time playing of sound
        self.sound.play()
    def stop(self):
        self.sound.stop()


class ANIMATION(object):
    def __init__(self, title, size, color, angle, SURFACE):
        self.title = title
        self.size = size
        self.color = color
        self.angle = angle           ### the angle after rotate for each cycle
        self.SURFACE = SURFACE
        self.degree = 0
    def setFont(self):
        self.titleFont = pygame.font.Font('freesansbold.ttf', self.size)
        self.titleSurf = self.titleFont.render(self.title, True, self.color)
    def setMovement(self):
        self.rotaeRect = self.rotateSurf.get_rect()
        self.rotaeRect.center = (W_SCREEN/2, H_SCREEN/2)
        self.SURFACE.blit(self.rotateSurf, self.rotaeRect)
        self.degree += self.angle
    def moveRotate(self):
        self.rotateSurf = pygame.transform.rotate(self.titleSurf, self.degree)
        self.setMovement()


def startScreen():
    global setDisplay


    pygame.init()
    setDisplay = pygame.display.set_mode((W_SCREEN, H_SCREEN))
    pygame.display.set_caption('WORMY !')

    #### Draw some titile for WORMy and add some music background
    RTA = ANIMATION ("WORMY", 40, YELLOW, 10, setDisplay)
    RTA.setFont()

    pygame.mixer.music.load('happiness.mp3')
    pygame.mixer.music.play(-1,0.0)

    BACK_GROUND = image('background.jpg', setDisplay, (W_SCREEN, H_SCREEN), (0,0))
    WORM_IMG = image('wormy.png', setDisplay, (170, 170), (W_SCREEN*0.7,H_SCREEN*0.7))
    APPLE_IMG = image('apple.png', setDisplay, (50,50), (W_FRAMEGAME*0.75, H_SCREEN*0.85))


    while True:
        setDisplay.fill(DARK)
        BACK_GROUND.draw()
        APPLE_IMG.draw()
        WORM_IMG.draw()
        RTA.moveRotate()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                terminate()
            elif event.type == KEYDOWN:
                pygame.mixer.music.stop()
                runGame()
        pygame.display.update()
        fpsClock.tick(FPS)

def runGame():
    global setDisplay, FOOD, HEAD, WORM

    SCORE = ()
    POINT = ()
    WORM = []

    initEnv(WORM)
    SCORE = drawText('SCORE', 20, RED, POSITION_SCORE)
    POINT = drawText( 10*(HEAD - NUMBER_HEAD + 1), 20, PURPLE, POSITION_POINT)  ### POINT is just the co-ordinate or the object, not point score
    FOOD = randomN(1)                                                          ### The point score is HEAD - NUMBER_HEAD
    Direction = "RIGHT"

    soundEating = sound('match.wav')

    BACK_GROUND = image('BackgroundSky.jpg', setDisplay, (W_SCREEN, H_SCREEN), (0,0))

    while True:

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_DOWN and Direction != "UP"):
                    Direction = "DOWN"
                elif (event.key == K_LEFT and Direction != "RIGHT"):
                    Direction = "LEFT"
                elif (event.key == K_UP and Direction != "DOWN"):
                    Direction = "UP"
                elif (event.key == K_RIGHT and Direction != "LEFT"):
                    Direction = "RIGHT"

        BACK_GROUND.draw()
        setDisplay.blit(SCORE[0], SCORE[1])
        setDisplay.blit(POINT[0], POINT[1])

        if checkEaten(WORM, DIRECTION_TABLE[Direction]) == True:
            POINT = drawText( 10*(HEAD - NUMBER_HEAD + 1), 20, PURPLE, POSITION_POINT)
            soundEating.play()
        else:
            moveWorm(WORM, DIRECTION_TABLE[Direction])

        if (gameOver(WORM) == True):
            pygame.mixer.music.stop()
            gameOverScreen()

        drawInit(WORM, FOOD)
        pygame.display.update()

        fpsClock.tick(FPS)            ### The speed of game, we use delay

class menuGameOver(object):
    def __init__(self, SURFACE):
        self.SURFACE = SURFACE
        self.strGameOver = drawText("Game Over", 40, DARK, ( W_SCREEN/2, H_SCREEN/2 - 3*CELL))
        self.strContinue = drawText("Do you want to continue ?", 25, DARK, ( W_SCREEN/2, H_SCREEN/2))
        self.strYes      = drawText("Yes", 25, DARK, ( W_SCREEN/2 - 3*CELL, H_SCREEN/2 + 2*CELL))
        self.strNo       = drawText("No", 25, DARK, ( W_SCREEN/2 + 3*CELL , H_SCREEN/2 + 2*CELL))
    def drawing(self):
        self.SURFACE.blit(self.strGameOver[0], self.strGameOver[1])
        self.SURFACE.blit(self.strContinue[0], self.strContinue[1])
        self.SURFACE.blit(self.strYes[0],      self.strYes[1])
        self.SURFACE.blit(self.strNo[0],       self.strNo[1])

def gameOverScreen():
    global setDisplay, WORM, FOOD
    ### Draw some graph in here

    menuOver = menuGameOver(setDisplay)                ### Class of menuGameOver
    pygame.mixer.music.load('livingdream.mp3')
    pygame.mixer.music.play(-1, 0.0)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_y:
                    pygame.mixer.music.stop()
                    runGame()
                elif event.key == K_n:
                    pygame.mixer.music.stop()
                    startScreen()

        drawInit(WORM, FOOD)
        menuOver.drawing()
        pygame.display.update()

if __name__ == "__main__":
    startScreen()