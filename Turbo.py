import pygame, sys
from pygame.locals import *
from car import Car

# Creazione finestra
pygame.init()
window_size = (1000, 750)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Turbo')
clock = pygame.time.Clock()

# Variabili colore macchina e sfondo
rossa=pygame.image.load('immagini/macchina_rossa.png')
blu=pygame.image.load('immagini/macchina_blu.png')
viola=pygame.image.load('immagini/macchina_viola.png')
verde=pygame.image.load('immagini/macchina_verde.png')
gialla=pygame.image.load('immagini/macchina_gialla.png')
circuito=pygame.image.load('Circuiti/3.png')
bordo_circuito=pygame.image.load('Circuiti/4.png')
bordo_circuito_mask= pygame.mask.from_surface(bordo_circuito)

# Classi Car e Pista
P1= Car(screen, rossa, (930, 350), (20, 35))
P2= Car(screen, blu, (900, 350), (20, 35))

# Ciclo fondamentale con aggiunta tasti
while True:

    # Chiusura finestra
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Tasti movimento
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        P1.rotazione(right=True)

    if keys[K_LEFT]:
        P1.rotazione(left=True)

    if keys[K_UP]:
        P1.move_forward()
        P1mov=1
    else:
        P1.stop()

    if keys[K_DOWN]:
        P1.move_backward()
        P1mov=-1
    else:
        P1.stop()


    if keys[K_d]:
        P2.rotazione(right=True)

    if keys[K_a]:
        P2.rotazione(left=True)

    if keys[K_w]:
        P2.move_forward()
        P2mov=1
    else:
        P2.stop()

    if keys[K_s]:
        P2.move_backward()
        P2mov=-1
    else:
        P2.stop()

    # Colore sfondo
    screen.fill((32,239,156))

    # Disegno pista, disegno e movimento macchine
    #pista.draw()
    #bordo_pista.draw()
    screen.blit(circuito, (0,0))
    P1.move()
    P1.draw(screen)
    P2.move()
    P2.draw(screen)

    # Collisione
    if P1.collisione(bordo_circuito_mask, 0, 0) != None:
        P1.rimbalzo(P1mov)
    
    if P2.collisione(bordo_circuito_mask, 0, 0) != None:
        P2.rimbalzo(P2mov)

    # Aggiorno schermo e clock
    pygame.display.flip()
    clock.tick(60)