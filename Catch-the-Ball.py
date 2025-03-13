###############################################
##                                           ##
## Programm für das Spiel Catch the BAll     ##
##                                           ##
###############################################

# authors: Antonia Herz, Marit Schiller
# date: 10.03.2025
# brief:


# Bibliotheken
import random
import pygame 
pygame.init()

# Fenster Constanten
BREITE = 730
HOEHE = 750 
WIN = pygame.display.set_mode ((BREITE, HOEHE))
pygame.display.set_caption ("Catch the Ball")

# FPS vom Spiel
FPS = 60

# Fanger Constanten
FANGER_BREITE = 100
FANGER_HOEHE = 20
FANGER_FARBE = (200, 60, 150)
FANGER_GES = 8
FANGER_Y = 100

# Ball Constanten
BALL_RADIUS = 7
BALL_FARBE = ('PINK')
BALL_GES = 4
BALL_Y = 0
MAX_BALLANZAHL = 10
MIN_TIME = 400
MAX_TIME = 900
FIRST_BALL_TIME = 1000

MIN_BALL_X = BALL_RADIUS
MAX_BALL_X = BREITE - BALL_RADIUS

BALL_FARBE_MIN = 0
BALL_FARBE_MAX = 255

BALL_FARBE_GRENZE = 209
BALL_FARBE_ERSATZ = 'PINK'

# Fonts
COUNTER = pygame.font.SysFont('comicsans', 20)
WINNING_FONT = pygame.font.SysFont('comicsans', 100)

# Counter Constanten
COUNTERPOSITION_X, COUNTERPOSITION_Y = 10, 10
COUNTER_FARBE = 'GRAY'
COUNTER_START = 0
COUNTER_ADD = 1
COUNTER_SUB = 1

# Userevents
BALL_HIT_FANGER = pygame.USEREVENT +1
BALL_HIT_GROUND = pygame.USEREVENT +2
TIMER = pygame.USEREVENT +3

# Constanten fürs gewinnen
WINNING_COUNTER = 25
WINNING_TEXT = 'You won!'
AFTER_WINNING_DELAY = 3000
WINNING_FARBE = 'BLACK'

# Listen
Balle_Liste = []

# Vorinitialisierung der Variablen
counter = 0

class Fanger:

    def __init__ (self, x, y, fanger_breite, fanger_hoehe):
        self.x = x
        self.y = y
        self.fanger_breite = fanger_breite
        self.fanger_hoehe = fanger_hoehe

    def draw (self, win):
        pygame.draw.rect (win,FANGER_FARBE, (self.x, self.y, self.fanger_breite, self.fanger_hoehe) )
    
    def move(self, rechts = True ):
        if rechts:
            self.x += FANGER_GES
        else:
            self.x -= FANGER_GES


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
    if keys [pygame.K_RIGHT] and (fanger.x + FANGER_BREITE + FANGER_GES <= BREITE):
        fanger.move (rechts = True)
    if keys [pygame.K_LEFT] and ( fanger.x - FANGER_GES >= 0 ):
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
    ball = pygame.Rect(ball_x, BALL_Y, BALL_RADIUS, BALL_RADIUS)
    ball_farbe_rot = random.randint(BALL_FARBE_MIN, BALL_FARBE_MAX)
    ball_farbe_grun = random.randint(BALL_FARBE_MIN, BALL_FARBE_MAX)
    ball_farbe_blau = random.randint(BALL_FARBE_MIN, BALL_FARBE_MAX)
    if (ball_farbe_rot > BALL_FARBE_GRENZE) and (ball_farbe_grun > BALL_FARBE_GRENZE) and (ball_farbe_blau > BALL_FARBE_GRENZE):
        BALL_FARBE = (BALL_FARBE_ERSATZ)
    else:
        BALL_FARBE = ((ball_farbe_rot), (ball_farbe_grun), (ball_farbe_blau))
    ball = Ball(ball_x, BALL_Y, BALL_RADIUS, BALL_FARBE)
    Balle_Liste.append(ball)


def draw (win, fanger, Balle_Liste, counter):
    win.fill(("WHITE"))
    counter_text = COUNTER.render('Counter: ' + str(counter), 1, COUNTER_FARBE)     #'COUNTER: ' Rausziehen?
    win.blit(counter_text, (COUNTERPOSITION_X, COUNTERPOSITION_Y))
    fanger.draw(win)
    for ball in Balle_Liste:
        ball.draw(win)
    pygame.display.update()

def winning(win, text):
    winning_text = WINNING_FONT.render(text, 1, WINNING_FARBE)
    win.blit(winning_text, (BREITE//2 - winning_text.get_width()/2, HOEHE//2 - winning_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(AFTER_WINNING_DELAY)

def main():

    run=True 
    clock = pygame.time.Clock()
    fanger = Fanger(BREITE/2 - FANGER_BREITE/2, HOEHE - FANGER_Y, FANGER_BREITE, FANGER_HOEHE)
    delay_time = FIRST_BALL_TIME
    pygame.time.set_timer(TIMER, delay_time)
    counter = COUNTER_START

    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.USEREVENT +1:
                counter += COUNTER_ADD
            if event.type == pygame.USEREVENT +2:
                counter -= COUNTER_SUB

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