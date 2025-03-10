###############################################
##                                           ##
## Programm für das Spiel Catch the BAll     ##
##                                           ##
###############################################

# authors: Antonia Herz, Marit Schiller
# date: 10.03.2025
# brief:

import pygame 
pygame.init 

BREITE = 730
HOEHE = 750 
WIN = pygame.display.set_mode ((BREITE, HOEHE))

FPS = 60

FANGER_BREITE = 100
FANGER_HOEHE = 20

BALL_RADIUS = 7

class Fanger:
    Fanger_Farbe = ("BLACK")
    GES = 7

    def __init__ (self, x, y, fanger_breite, fanger_hoehe):
        self.x = x
        self.y = y
        self.fanger_breite = fanger_breite
        self.fanger_hoehe = fanger_hoehe

    def draw (self, win):
        pygame.draw.rect (win,self.Fanger_Farbe, (self.x, self.y, self.fanger_breite, self.fanger_hoehe) )

class BALL:
    BALL_FARBE = ("PINK")
    BALL_GES = 5 

    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius 

    def draw (self, win):
        pygame.draw.circle(win, self.BALL_FARBE,(self.x, self.y), self.radius)

    def move (self):
        self.y += self.BALL_GES

def draw (win, fanger, ball):
    win.fill(("WHITE"))
    fanger.draw(win)
    ball.draw (win)
    pygame.display.update()

def main():

    run=True 
    clock = pygame.time.Clock()
    fanger = Fanger(BREITE/2 - FANGER_BREITE/2, HOEHE - 100, FANGER_BREITE, FANGER_HOEHE)
    ball = BALL(42, 0, BALL_RADIUS)


    while run:
        draw(WIN, fanger, ball)
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        ball.move ()
    pygame.quit()
    
main()