import pygame, sys, time
from pygame.locals import *
from pygame import mixer
from car import Car
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
circuito=pygame.image.load('Circuiti/3.png')
bordo_circuito=pygame.image.load('Circuiti/4.png')
bordo_circuito_mask= pygame.mask.from_surface(bordo_circuito)
finish= pygame.image.load('immagini/finish.png')
finish_mask= pygame.mask.from_surface(finish)

check1=pygame.image.load('immagini/point.png')
check1_mask=pygame.mask.from_surface(check1)
check2=pygame.image.load('immagini/point.png')
check2_mask=pygame.mask.from_surface(check2)

# Serve per scegliere carattere e grandezza del testo
font = pygame.font.SysFont('comicsans', 50)

# Classi Car e Pista
P1= Car(screen, rossa, (930, 344), (20, 35))
P2= Car(screen, blu, (900, 344), (20, 35))

def draw(screen, immagini, P1, P2, Informazioni_Game):

    time_text = font.render(f"Time: {Informazioni_Game.get_level_time()}s", 1, (255, 255, 255))
    screen.blit(time_text, (10, circuito.get_height - time_text.get_height() - 40))

    vel_text = font.render(f"Vel: {round(P1.vel, 1)}px/s", 1, (255, 255, 255))
    screen.blit(vel_text, (10, circuito.get_height - vel_text.get_height() - 10))

    # P1.draw(win)
    # P2.draw(win)
    pygame.display.update()

# Schermata iniziale con titolo
def draw_text(text, title):
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(lunghezza_schermo/2, altezza_schermo/2))
    title_surface = font.render(title, True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(lunghezza_schermo/2, altezza_schermo/4))
    screen.fill((0, 0, 0))
    screen.blit(text_surface, text_rect)
    screen.blit(title_surface, title_rect)
    pygame.display.flip()

# Countdown
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

def countdown_timer(seconds):
    while seconds >= 0:
        if seconds != 0 :
            draw_text(str(seconds), "TURBO")
        else:
            draw_text("VIA!", "TURBO")
        seconds -= 1
        time.sleep(1)

draw_text("Press SPACE to start", "TURBO")
wait_for_input()
countdown_timer(3)
counter=0

# caricare l'audio e fralo partire
audio = pygame.mixer.Sound("turbo_audio.mp3")
pygame.mixer.Sound.play(audio)

# Ciclo fondamentale con aggiunta tasti
while True:

    # Chiusura finestra
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Tasti movimento 1
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

    # Tasti movimento 2
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

    # Disegno pista, macchine e checkpoint
    screen.blit(circuito, (0,0))
    screen.blit(finish, (880, 380)) 
    screen.blit(bordo_circuito, (0,0))
    screen.blit(check1, (465,350))
    screen.blit(check2, (915,400))
    P1.draw(screen)
    P2.draw(screen)

    # Collisione
    if P1.collisione(bordo_circuito_mask, 0, 0) != None:
        P1.rimbalzo(P1mov)
    
    if P2.collisione(bordo_circuito_mask, 0, 0) != None:
        P2.rimbalzo(P2mov)

    # Collisione con i checkpoint
    check1_P1= P1.collisione(check1_mask, 465, 350)
    check2_P1= P1.collisione(check2_mask, 915, 400)
    check1_P2= P2.collisione(check1_mask, 465, 350)
    check2_P2= P2.collisione(check2_mask, 915, 400)

    if check1_P1 != None and counter == 0:
        counter=1
    if check2_P1 != None and counter == 1:
        counter=2
    
    if check1_P2 != None and counter == 0:
        counter=1
    if check2_P2 != None and counter == 1:
        counter=2

    # Collisione con il finish
    fine_P1 = P1.collisione(finish_mask, *(880, 380))
    if fine_P1 != None and counter == 2:
        print("P1 ha vinto")
        # al posto di ha vinto dobbiamo aumentrare i giri che all'inizio devono essere = 0
        counter = 0

    fine_P2 = P2.collisione(finish_mask, *(880, 380))
    if fine_P2 != None and counter == 2:
        print("P2 ha vinto")
        # al posto di ha vinto dobbiamo aumentrare i giri che all'inizio devono essere = 0
        counter = 0

    # Aggiorno schermo e clock
    pygame.display.flip()
    clock.tick(60)