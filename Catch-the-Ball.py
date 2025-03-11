###############################################
##                                           ##
## Programm für das Spiel Catch the BAll     ##
##                                           ##
###############################################

# authors: Antonia Herz, Marit Schiller
# date: 10.03.2025
# brief:

import pygame 
pygame.init()

BREITE = 730
HOEHE = 750 
WIN = pygame.display.set_mode ((BREITE, HOEHE))
pygame.display.set_caption ("Catch the Ball")

FPS = 60

FANGER_BREITE = 100
FANGER_HOEHE = 20

BALL_RADIUS = 7

COUNTER = pygame.font.SysFont('comicsans', 20)
COUNTERPOSITION_X, COUNTERPOSITION_Y = 10, 10
counter = 0

BALL_HIT_FANGER = pygame.USEREVENT +1
BALL_HIT_GROUND = pygame.USEREVENT +2

Balle_Liste = []

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
        

def fanger_movement(fanger, keys):
    if keys [pygame.K_RIGHT] and (fanger.x - FANGER_BREITE + fanger.GES <= BREITE):
        fanger.move (rechts = True)
    if keys [pygame.K_LEFT] and ( fanger.x - fanger.GES >= 0 ):
        fanger.move (rechts = False )

def ball_movement(ball, fanger):
    if(ball.y + BALL_RADIUS <= fanger.y and ball.y + BALL_RADIUS + ball.BALL_GES >= fanger.y) and (ball.x >= fanger.x and ball.x <= fanger.x + FANGER_BREITE):
        ball.y = fanger.y - BALL_RADIUS
        pygame.event.post(pygame.event.Event(BALL_HIT_FANGER))
    elif ball.y + BALL_RADIUS >= HOEHE:
        ball.y = ball.y
        pygame.event.post(pygame.event.Event(BALL_HIT_GROUND))
    else:
        ball.move()

def draw (win, fanger, ball, counter):
    win.fill(("WHITE"))
    counter_text = COUNTER.render('Counter: ' + str(counter), 1, 'GRAY')
    win.blit(counter_text, (COUNTERPOSITION_X, COUNTERPOSITION_Y))
    fanger.draw(win)
    ball.draw (win)
    pygame.display.update()

def main():

    run=True 
    clock = pygame.time.Clock()
    fanger = Fanger(BREITE/2 - FANGER_BREITE/2, HOEHE - 100, FANGER_BREITE, FANGER_HOEHE)
    ball = BALL(42, 0, BALL_RADIUS)
    counter = 0

    Balle_Liste.append(ball)


    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.USEREVENT +1:
                counter += 1
            if event.type == pygame.USEREVENT +2:
                counter -= 1

        keys = pygame.key.get_pressed()
        fanger_movement(fanger, keys)
        ball_movement (Balle_Liste[0], fanger)

        draw(WIN, fanger, Balle_Liste[0], counter)

    pygame.quit()
    
main()