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
pygame.init()

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
MAX_TIME = 1000
FIRST_BALL_TIME = 1000

MIN_BALL_X = BALL_RADIUS
MAX_BALL_X = BREITE - BALL_RADIUS


COUNTER = pygame.font.SysFont('comicsans', 20)
WINNING_FONT = pygame.font.SysFont('comicsans', 100)

COUNTERPOSITION_X, COUNTERPOSITION_Y = 10, 10
counter = 0

BALL_HIT_FANGER = pygame.USEREVENT +1
BALL_HIT_GROUND = pygame.USEREVENT +2
TIMER = pygame.USEREVENT +3

WINNING_COUNTER = 25
WINNING_TEXT = 'You won!'
AFTER_WINNING_DELAY = 3000

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


class Ball:
    def __init__(self, x, y, BALL_RADIUS, farbe):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.farbe = farbe

    def draw (self, win):
        pygame.draw.circle(win, self.farbe, (self.x, self.y), self.radius)

    def create_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


def fanger_movement(fanger, keys):
    if keys [pygame.K_RIGHT] and (fanger.x + FANGER_BREITE + fanger.GES <= BREITE):
        fanger.move (rechts = True)
    if keys [pygame.K_LEFT] and ( fanger.x - fanger.GES >= 0 ):
        fanger.move (rechts = False )

def balle_movement(Balle_Liste, fanger):
    fanger_rect = pygame.Rect(fanger.x, fanger.y, FANGER_BREITE, FANGER_HOEHE)
    for ball in Balle_Liste:
        ball.y += BALL_GES
        if ball.create_rect().colliderect(fanger_rect):
            pygame.event.post(pygame.event.Event(BALL_HIT_FANGER))
            Balle_Liste.remove(ball)
        elif ball.y + BALL_RADIUS >= HOEHE:
            pygame.event.post(pygame.event.Event(BALL_HIT_GROUND))
            Balle_Liste.remove(ball)

def spawn_ball():
    ball_x = random.randint(MIN_BALL_X, MAX_BALL_X)
    ball = pygame.Rect(ball_x, 0, BALL_RADIUS, BALL_RADIUS)
    ball_farbe_rot = random.randint(0, 255)
    ball_farbe_grun = random.randint(0, 255)
    ball_farbe_blau = random.randint(0, 255)
    if (ball_farbe_rot > 235) and (ball_farbe_grun > 235) and (ball_farbe_blau > 235):
        BALL_FARBE = ('PINK')
    else:
        BALL_FARBE = ((ball_farbe_rot), (ball_farbe_grun), (ball_farbe_blau))
    ball = Ball(ball_x, 0, BALL_RADIUS, BALL_FARBE)
    Balle_Liste.append(ball)


def draw (win, fanger, Balle_Liste, counter):
    win.fill(("WHITE"))
    counter_text = COUNTER.render('Counter: ' + str(counter), 1, 'GRAY')
    win.blit(counter_text, (COUNTERPOSITION_X, COUNTERPOSITION_Y))
    fanger.draw(win)
    for ball in Balle_Liste:
        ball.draw(win)
    pygame.display.update()

def winning(win, text):
    winning_text = WINNING_FONT.render(text, 1, 'BLACK')
    win.blit(winning_text, (BREITE//2 - winning_text.get_width()/2, HOEHE//2 - winning_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(AFTER_WINNING_DELAY)

def main():

    run=True 
    clock = pygame.time.Clock()
    fanger = Fanger(BREITE/2 - FANGER_BREITE/2, HOEHE - 100, FANGER_BREITE, FANGER_HOEHE)
    delay_time = FIRST_BALL_TIME
    pygame.time.set_timer(TIMER, delay_time)
    counter = 0

    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.USEREVENT +1:
                counter += 1
            if event.type == pygame.USEREVENT +2:
                counter -= 1

            if (event.type == TIMER) and (len(Balle_Liste) < MAX_BALLANZAHL):
                spawn_ball()
                delay_time = random.randint(MIN_TIME, MAX_TIME)
                pygame.time.set_timer(TIMER, delay_time)

        fanger_movement(fanger, keys)
        balle_movement (Balle_Liste, fanger)

        draw(WIN, fanger, Balle_Liste, counter)

        if counter >= WINNING_COUNTER:
            winning(WIN, WINNING_TEXT)
            break

    pygame.quit()

if __name__ == '__main__':    
    main()