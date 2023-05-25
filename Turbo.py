import pygame, sys, time
from pygame.locals import *
from car import Car
from Livelli_Gioco import GameInfo
from utils import blit_text_center
pygame.font.init()

# Creazione finestra
pygame.init()
altezza_schermo=750
lunghezza_schermo=1000
window_size = (lunghezza_schermo, altezza_schermo)
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
finish= pygame.image.load('immagini/finish.png')
finish_mask= pygame.mask.from_surface(finish)
white=(255, 255, 255)

#___________________________________________________________________

# Classe per i livelli e le scritte
Informazioni_Game = GameInfo()

# Serve per scegliere carattere e grandezza del testo
font = pygame.font.SysFont('comicsans', 50)
#___________________________________________________________________

# Classi Car e Pista
P1= Car(screen, rossa, (930, 370), (20, 35))
P2= Car(screen, blu, (900, 370), (20, 35))

def draw(screen, immagini, P1, P2, Informazioni_Game):

    time_text = font.render(f"Time: {Informazioni_Game.get_level_time()}s", 1, (255, 255, 255))
    screen.blit(time_text, (10, circuito.get_height - time_text.get_height() - 40))

    vel_text = font.render(
        f"Vel: {round(P1.vel, 1)}px/s", 1, (255, 255, 255))
    screen.blit(vel_text, (10, circuito.get_height - vel_text.get_height() - 10))

    # P1.draw(win)
    # P2.draw(win)
    pygame.display.update()
    
def draw_text(text):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(lunghezza_schermo/2, altezza_schermo/2))
    screen.fill((0, 0, 0))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()

def countdown_timer(seconds):
    while seconds >= 0:
        draw_text(str(seconds))
        seconds -= 1
        time.sleep(1)

def wait_for_input():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

def game_logic():
    # Logica del gioco qui
    pass

draw_text("Press SPACE to start")
wait_for_input()

countdown_timer(5)

# Avvio del gioco dopo il conto alla rovescia
game_logic()


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
    screen.blit(circuito, (0,0))
    screen.blit(finish, (880, 350)) 
    screen.blit(bordo_circuito, (0,0))
    P1.move()
    P1.draw(screen)
    P2.move()
    P2.draw(screen)

    # Collisione
    if P1.collisione(bordo_circuito_mask, 0, 0) != None:
        P1.rimbalzo(P1mov)
    
    if P2.collisione(bordo_circuito_mask, 0, 0) != None:
        P2.rimbalzo(P2mov)

    # Collisione con il finish
    fine_P1 = P1.collisione(finish_mask, *(880, 350))
    if fine_P1 != None:
        if fine_P1[1] == 0:
            print("P1 finish")
    
    fine_P2 = P2.collisione(finish_mask, *(880, 350))
    if fine_P2 != None:
        if fine_P2[1] == 0:
            print("P2 finish")

    # Aggiorno schermo e clock
    pygame.display.flip()
    clock.tick(60)