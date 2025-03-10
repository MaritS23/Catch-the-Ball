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
WIN = pygame.display.set_mode (BREITE, HOEHE)

FPS = 60

def draw (win):
    win.fill(("WHITE"))

    pygame.display.update()

def main():

    run=True 
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()
    
main()