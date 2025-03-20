###############################################
##                                           ##
## Programm fur das Spiel Catch the BAll     ##
##                                           ##
###############################################

# authors: Antonia Herz, Marit Schiller
# date: 10.03.2025
# brief: Erstellt Kreise (= Balle) und ein Rechteck (=Fanger), den man steuern kann.


# Bibliotheken
import random as ran    #Die Bibliothek 'random' ermoglicht es einem, eine zufallige Zahl zu erhallten; das ist praktisch, wenn man ein Obkjekt eine zufallige Farbe geben mochte oder an eine zufallige Stelle platzieren mochte
import pygame           #Die Bibliothek 'pygame' enthalt essentielle bestandteile ohne die dieses Program uberhaubt nicht machbar ware; z.B. das Fenster in dem das Program grafisch dargestellt wird
pygame.init()

# Fenster Constanten
BREITE = 730
HOEHE = 750 
WIN = pygame.display.set_mode ((BREITE, HOEHE))
pygame.display.set_caption ("Catch the Ball")   #Uberschrift vom Fenster
FENSTER_FARBE = ('WHITE')

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
MIN_TIME = 400          #Minimale Zeit nach der ein neuer Ball auftaucht
MAX_TIME = 900          #Maximale Zeit nach der ein nauer Ball auftaucht
FIRST_BALL_TIME = 1000  #Zeit nach der der erste Ball auftaucht

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
COUNTER_START = 0   #Anfangswert vom Counter
COUNTER_ADD = 1     #Wert um der der Counter erhoht wird, wenn ein Ball gefangen wurde
COUNTER_SUB = 1     #Wert um der der Counter verniedrigt wird, wenn ein Ball den 'Boden' berührt

# Userevents
BALL_HIT_FANGER = pygame.USEREVENT +1
BALL_HIT_GROUND = pygame.USEREVENT +2
TIMER = pygame.USEREVENT +3

# Constanten fürs gewinnen
WINNING_COUNTER = 25        #Counterwert bei dem man gewonnen hat
WINNING_TEXT = 'You won!'
AFTER_WINNING_DELAY = 3000  #Wartezeit nach dem gewinnen
WINNING_FARBE = 'BLACK'

# Listen
Balle_Liste = []

# Vorinitialisierung der Variablen
counter = 0
ball_x = BREITE /2
delay_time = FIRST_BALL_TIME
keys = False
run = True
counter_text = ''
winning_text = ''
ball_farbe_rot = 0
ball_farbe_grun = 0
ball_farbe_blau = 0
render_var = 1


# Klasse Fanger:
class Fanger:

    def __init__ (self, x, y, fanger_breite, fanger_hoehe):
        self.x = x
        self.y = y
        self.fanger_breite = fanger_breite
        self.fanger_hoehe = fanger_hoehe

    def draw (self, win):
        pygame.draw.rect (win,FANGER_FARBE, (self.x, self.y, self.fanger_breite, self.fanger_hoehe))    #Fanger werden als Rechtecke gezeichnet
    
    def move(self, rechts = True):                                                                     #Funktion zum bewegen des Fangers, ubergebene werte sind self und recht = True
        if rechts:                                                                                      #Wenn die Bedingung wahr ist (d.h. wenn das 2. Element rechts = True ist, 'True' muss dabei nicht hingeschrieben werden),
            self.x += FANGER_GES                                                                        #wird auf die x-Position die Pixelanzahl von der Geschwindigkeit addiert.
        else:                                                                                           #Wenn die Bedingung nicht wahr ist,
            self.x -= FANGER_GES                                                                        #wird von der x-Position die Geschwindigkeit abgezogen.

# Klasse Ball:
class Ball:
    def __init__(self, x, y, BALL_RADIUS, farbe):
        self.x = x
        self.y = y
        self.radius = BALL_RADIUS
        self.farbe = farbe                                                                              #Die Farbe soll variabel sein

    def draw (self, win):               
        pygame.draw.circle(win, self.farbe, (self.x, self.y), self.radius)                              #Ball werden als Kreise gezeichnet

    def create_rect(self):                                                                              #Ball wird als Rechteck initialisiert, dadurch kann man spater uberprufen, ob ein Ball mit dem Fanger colidiert
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2) #Dadurch, das Kreise keine Rechtecke sind gibt es naturlich Teile, die als Rechteck existieren aber nicht als Ball, aber angesichts der Geschwindigkeit vom Ball und Fanger und der Grosse des Balls ist es unserer Meinung nach Entschuldbar

# Bewegungsfunktion des Fangers
def fanger_movement(fanger, keys):
    if keys [pygame.K_RIGHT] and (fanger.x + FANGER_BREITE + FANGER_GES <= BREITE): #Damit der fanger nicht auf der rechten Seite aus dem Fenster verschwinden kann
        fanger.move (rechts = True)
    if keys [pygame.K_LEFT] and ( fanger.x - FANGER_GES >= 0 ):                     #Damit der fanger nicht auf der linken Seite aus dem Fenster verschwinden kann; 0 ist die x-Position am linken Rand
        fanger.move (rechts = False )

# Bewegungsfunkton des Balls
def balle_movement(Balle_Liste, fanger):
    fanger_rect = pygame.Rect(fanger.x, fanger.y, FANGER_BREITE, FANGER_HOEHE)      #Der fanger wird als Rechteck interpretiert
    for ball in Balle_Liste:
        ball.y += BALL_GES                                                          #Fallbewegung des Balls

        if ball.create_rect().colliderect(fanger_rect):                             #Es wird uberpruft, ob das Rechteck um den Ball mit dem fanger-Rechteck kollidiert
            pygame.event.post(pygame.event.Event(BALL_HIT_FANGER))
            Balle_Liste.remove(ball)                                                #Dadurch, dass der ball aus der Liste 'Balle_Liste entfernt wird, wird er auch vom Fenster entfernt
        elif ball.y + BALL_RADIUS >= HOEHE:
            pygame.event.post(pygame.event.Event(BALL_HIT_GROUND))
            Balle_Liste.remove(ball)                                                #Dadurch, dass der ball aus der Liste 'Balle_Liste entfernt wird, wird er auch vom Fenster entfernt

# Spawnfunktion des Balls
def spawn_ball():
    ball_x = ran.randint(MIN_BALL_X, MAX_BALL_X)                                                                                 #Damit die x-Koordinate fur jeden Ball individuell ist, muss diese jedesmal neu bestimmt werden, daher ist die bestimmung in der Funktion zu finden
    ball = pygame.Rect(ball_x, BALL_Y, BALL_RADIUS, BALL_RADIUS)
    ball_farbe_rot = ran.randint(BALL_FARBE_MIN, BALL_FARBE_MAX)                                                                 #Die Farbe jedes Balls soll auch individuell sein, daher muss der Rot-, Grun- und Blauanteil jedesmal neu bestimmt werden
    ball_farbe_grun = ran.randint(BALL_FARBE_MIN, BALL_FARBE_MAX)
    ball_farbe_blau = ran.randint(BALL_FARBE_MIN, BALL_FARBE_MAX)
    if (ball_farbe_rot > BALL_FARBE_GRENZE) and (ball_farbe_grun > BALL_FARBE_GRENZE) and (ball_farbe_blau > BALL_FARBE_GRENZE):    #Je heller die ball-farbe wird, desto schwieriger ist es sie vom Hintergrund zu untscheiden, daher muss sie beschrankt werden. Da aber eine erlaubte farbe z.B. (250, 0, 0) (also Rot) sein soll, kann man nicht einfach die Obere Grenze der Farben runtersetzten, sonder muss uberprufen, ob alle Teile der Farbe zu hell sind
        BALL_FARBE = (BALL_FARBE_ERSATZ)
    else:
        BALL_FARBE = ((ball_farbe_rot), (ball_farbe_grun), (ball_farbe_blau))
    ball = Ball(ball_x, BALL_Y, BALL_RADIUS, BALL_FARBE)
    Balle_Liste.append(ball)

# Malfunktion
def draw (win, fanger, Balle_Liste, counter):
    win.fill(FENSTER_FARBE)                                                                                     #fullen des Fensters mit Fullfarbe vom Fenster, damit alle Elemente auf ein 'neues Blatt' gezeichnet werden, sonst sieht man die Spur die die Elemente machen -> man wusste nicht so die z.B. der Fanger gewindet
    counter_text = COUNTER.render('Counter: ' + str(counter), render_var, COUNTER_FARBE)                        #Countertext wird eingefuhrt   #'COUNTER: ' Rausziehen?
    win.blit(counter_text, (COUNTERPOSITION_X, COUNTERPOSITION_Y))                                              #Counter wird gemalt, dadurch, dass er nach dem fullen des Fensters gemalt wird, kann man ihn sehen
    fanger.draw(win)                                                                                            #Zeichnen des Fangers, dadurch, dass er nach dem Counter gemalt wird, kann man den Fanger ganz sehen, selbt wenn der counter auf Hohe des Fangers ist
    for ball in Balle_Liste:                                                                                    #Fur alle Elemente 'ball' aus der Liste 'Balle_Liste':
        ball.draw(win)                                                                                          #male 'ball     -> die Ball-Malfunktion ist die letzte, die aufgerufen wird, somit sind die immer ganz zu sehen
    pygame.display.update()                                                                                     #Damit alle Elemente tatsachlich so angezeigt werden wie sie nach dem aufrugen aller funktionen sind

def winning(win, text):
    winning_text = WINNING_FONT.render(text, render_var, WINNING_FARBE)                                          #Text furs gewinnen
    win.blit(winning_text, (BREITE//2 - winning_text.get_width()/2, HOEHE//2 - winning_text.get_height()/2))    #Gewinntext wird gemalt
    pygame.display.update()
    pygame.time.delay(AFTER_WINNING_DELAY)                                                                      #Eine bestimmte Zeit lang wird gewartet, wahrend alles pausiert wird

# Hauptfunktion 
def main():
                    #Variablen fur die Haubtfunktion
    run=True 
    clock = pygame.time.Clock()
    fanger = Fanger(BREITE/2 - FANGER_BREITE/2, HOEHE - FANGER_Y, FANGER_BREITE, FANGER_HOEHE)  #fanger wird in der Mitte des Fensters erstellt, auf einer vorgegebenen Hohe
    delay_time = FIRST_BALL_TIME                                                                #delay-time wird eingestellt
    pygame.time.set_timer(TIMER, delay_time)                                                    #'timer' wird gestartet
    counter = COUNTER_START                                                                     #Counter wird gesetzt

    while run:
        clock.tick(FPS)
        keys = pygame.key.get_pressed()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:                                                       #Wenn das Fenster geschlossen wird (rotes X)
                run = False                                                                     # soll das programm geendet werden
            
            if event.type == pygame.USEREVENT +1:                                               #Wenn der Ball gefangen wurde
                counter += COUNTER_ADD
            if event.type == pygame.USEREVENT +2:                                               #Wenn der Ball auf den Boden aufkommt
                counter -= COUNTER_SUB

            if (event.type == TIMER) and (len(Balle_Liste) < MAX_BALLANZAHL):                   #Wenn die Zeit abgelaufen ist, und die maximale Ballanzahl noch nicht erreicht wurde
                spawn_ball()                                                                    # wird ein neuer ball erstellt
                delay_time = ran.randint(MIN_TIME, MAX_TIME)                                    #Neue zufallige Zeit wird eingestallt, dadurch ist sie fur jedenn ball individuell (kann naturlich gleich sein, muss aber nicht)
                pygame.time.set_timer(TIMER, delay_time)                                        #'timer' wird gestartet

        fanger_movement(fanger, keys)
        balle_movement (Balle_Liste, fanger)

        draw(WIN, fanger, Balle_Liste, counter)

        if counter >= WINNING_COUNTER:
            winning(WIN, WINNING_TEXT)
            break                                                                               #Nachdem das Spiel gewonnen wurde, soll das Programm ABGEBROCHEN werden

    pygame.quit()

if __name__ == '__main__':      # Stellt sicher, dass das Projekt aus der Datei heraus ausgefuhrt wird; wird immer so gemacht
    main()