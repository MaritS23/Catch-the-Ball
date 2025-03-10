###############################################
##                                           ##
## Programm für das Spiel Catch the BAll     ##
##                                           ##
###############################################

# authors: Antonia Herz, Marit Schiller
# date: 10.03.2025
# brief:

import random
import pygame 
pygame.init 

BREITE = 730
HOEHE = 750 
WIN = pygame.display.set_mode ((BREITE, HOEHE))
pygame.display.set_caption ("Catch the Ball")

FPS = 60

FANGER_BREITE = 100
FANGER_HOEHE = 20

BALL_RADIUS = 7
BALL_FARBE = ('PINK')
BALL_GES = 5
MAX_BALLANZAHL = 10
MIN_TIME = 500
MAX_TIME = 2000
DELAY_TIME = random.randint(MIN_TIME, MIN_TIME)

BALL_HIT_FANGER = pygame.USEREVENT +1
BALL_HIT_GROUND = pygame.USEREVENT +2

Balle_Liste = []
Balle_Farben = []

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
    
    def move(self, rechts = True ):
        if rechts:
            self.x += self.GES
        else:
            self.x -= self.GES
        

def fanger_movement(fanger, keys):
    if keys [pygame.K_RIGHT] and (fanger.x - FANGER_BREITE + fanger.GES <= BREITE):
        fanger.move (rechts = True)
    if keys [pygame.K_LEFT] and ( fanger.x - fanger.GES >= 0 ):
        fanger.move (rechts = False )

def balle_movement(Balle_Liste, fanger):
    for ball in Balle_Liste:
        ball.y += BALL_GES
        if (ball.y + BALL_RADIUS <= fanger.y and ball.y + BALL_RADIUS + BALL_GES >= fanger.y) and (ball.x >= fanger.x and ball.x <= fanger.x + FANGER_BREITE):
            ball.y = fanger.y - BALL_RADIUS
            pygame.event.post(pygame.event.Event(BALL_HIT_FANGER))
            Balle_Liste.remove(ball)
        elif ball.y + BALL_RADIUS >= HOEHE:
            pygame.event.post(pygame.event.Event(BALL_HIT_GROUND))
            Balle_Liste.remove(ball)

def spawn_ball():
    BALL_X = 42
    ball = pygame.Rect(BALL_X, 0, BALL_RADIUS, BALL_RADIUS)
    Balle_Liste.append(ball)
    ball_farbe_rot = random.randint(0, 255)
    ball_farbe_grun = random.randint(0, 255)
    ball_farbe_blau = random.randint(0, 255)
    if (ball_farbe_rot > 235) and (ball_farbe_grun > 235) and (ball_farbe_blau > 235):
        BALL_FARBE = ('PINK')
    else:
        BALL_FARBE = ((ball_farbe_rot), (ball_farbe_grun), (ball_farbe_blau))
    Balle_Farben.append(BALL_FARBE)


def draw (win, fanger, Balle_Liste, Balle_Farben):
    win.fill(("WHITE"))
    fanger.draw(win)
    for BALL_FARBE in Balle_Farben:
        for ball in Balle_Liste:
            pygame.draw.rect(win, BALL_FARBE, ball)

    pygame.display.update()

def main():

    run=True 
    clock = pygame.time.Clock()
    fanger = Fanger(BREITE/2 - FANGER_BREITE/2, HOEHE - 100, FANGER_BREITE, FANGER_HOEHE)


    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if keys[pygame.K_SPACE] and len(Balle_Liste) < MAX_BALLANZAHL:
                spawn_ball()

        fanger_movement(fanger, keys)
        balle_movement (Balle_Liste, fanger)

        draw(WIN, fanger, Balle_Liste, Balle_Farben)

    pygame.quit()
    
main()