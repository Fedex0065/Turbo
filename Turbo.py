import pygame, sys, time
from pygame.locals import *
from car import Car
from pulsante import Pulsante
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
circuito=pygame.image.load('immagini/circuito.png')
bordo_circuito=pygame.image.load('immagini/bordo_circuito.png')
bordo_circuito_mask= pygame.mask.from_surface(bordo_circuito)
finish= pygame.image.load('immagini/finish.png')
finish_mask= pygame.mask.from_surface(finish)
sfondo=pygame.transform.scale((pygame.image.load("immagini/Stelle.jpg")),(lunghezza_schermo, altezza_schermo))

# Checkpoint
check1_mask=pygame.mask.from_surface(pygame.image.load('immagini/point.png'))
check2_mask=pygame.mask.from_surface(pygame.image.load('immagini/point.png'))
check3_mask=pygame.mask.from_surface(pygame.image.load('immagini/point.png'))

# Classi Car
P1= Car(screen, rossa, (930, 344), (20, 35))
P2= Car(screen, blu, (900, 344), (20, 35))

# Classi Pulsante
reset=Pulsante(screen, (200, 500), (200, 100))
exit=Pulsante(screen, (600, 500), (200, 100))

# Serve per scegliere carattere e grandezza del testo
font1 = pygame.font.SysFont('comicsans', 50)
font2 = pygame.font.SysFont('comicsans', 150)

# Variabili varie
P1counter=0
P2counter=0
P1_giri = 0 
P2_giri = 0
tick = 0
secondi = 0
minuti = 0
finale=0

# Schermata iniziale con titolo
def draw_text(text, title):
    text_surface = font1.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(lunghezza_schermo/2, altezza_schermo/2))
    title_surface = font1.render(title, True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(lunghezza_schermo/2, altezza_schermo/4))
    screen.blit(sfondo, (0,0))
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

# Conta i giri dei due giocatori
def contagiri(P1_giri, P2_giri):
    font = pygame.font.SysFont(None, 35)
    testo = font.render(f"P1: {str(P1_giri)}/3", True, (255, 255, 255))
    testo2 = font.render(f"P2: {str(P2_giri)}/3", True, (255, 255, 255))
    screen.blit(testo, (550, 10))
    screen.blit(testo2, (550, 35))

# Audio e Tempo
inizio = pygame.mixer.Sound("musiche/Love nwantiti.mp3")
countdown = pygame.mixer.Sound("musiche/countdown.mp3")
audio = pygame.mixer.Sound("musiche/turbo_audio.mp3")
win = pygame.mixer.Sound("musiche/We are the champions.mp3")

pygame.mixer.Sound.play(inizio, -1)
draw_text("Press SPACE to start", "TURBO")
wait_for_input()
pygame.mixer.Sound.stop(inizio)
pygame.mixer.Sound.play(countdown)
countdown_timer(3)
pygame.mixer.Sound.stop(countdown)
pygame.mixer.Sound.play(audio, -1)

# Ciclo fondamentale con aggiunta tasti
while True:

    # Chiusura finestra
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        # Pulsanti Exit e Reset
        if event.type == pygame.MOUSEBUTTONDOWN and event.button==1:
            pos=pygame.mouse.get_pos()
            if exit.rect.collidepoint(pos):
                pygame.quit()
                sys.exit()
            if reset.rect.collidepoint(pos):
                P1_giri=0
                P2_giri=0
                screen.blit(sfondo, (0,0))
                screen.blit(circuito, (0,0))
                screen.blit(finish, (880, 380)) 
                screen.blit(bordo_circuito, (0,0))
                P1.draw_reset(screen, (930, 344))
                P2.draw_reset(screen, (900, 344))
                secondi=0
                minuti=0
                pygame.mixer.Sound.stop(win)
                pygame.mixer.Sound.play(audio, -1)
                

    # Tasti movimento P1
    keys = pygame.key.get_pressed()

    if keys[K_RIGHT]:
        P1.rotazione(right=True)

    if keys[K_LEFT]:
        P1.rotazione(left=True)

    if keys[K_UP]:
        P1.move_forward()
        P1mov=1
    elif keys[K_DOWN]:
        P1.move_backward()
        P1mov=-1

    # Tasti movimento P2
    if keys[K_d]:
        P2.rotazione(right=True)

    if keys[K_a]:
        P2.rotazione(left=True)

    if keys[K_w]:
        P2.move_forward()
        P2mov=1
    elif keys[K_s]:
        P2.move_backward()
        P2mov=-1

    # Sfondo
    screen.blit(sfondo, (0,0))

    # Disegno pista, macchine e checkpoint
    screen.blit(circuito, (0,0))
    screen.blit(finish, (880, 380)) 
    screen.blit(bordo_circuito, (0,0))
    P1.draw(screen)
    P2.draw(screen)

    # Collisione pista
    if P1.collisione(bordo_circuito_mask, 0, 0) != None:
        P1.rimbalzo(P1mov)
    
    if P2.collisione(bordo_circuito_mask, 0, 0) != None:
        P2.rimbalzo(P2mov)

    # Collisione con i checkpoint

    if P1.collisione(check1_mask, 500, 180) != None and P1counter == 0:
        P1counter=1
    if P1.collisione(check2_mask, 465, 350) != None and P1counter == 1:
        P1counter=2
    if P1.collisione(check3_mask, 915, 400) != None and P1counter == 2:
        P1counter=3
    
    if P2.collisione(check1_mask, 500, 180) != None and P2counter == 0:
        P2counter=1
    if P2.collisione(check2_mask, 465, 350) != None and P2counter == 1:
        P2counter=2
    if P2.collisione(check3_mask, 915, 400) != None and P2counter == 2:
        P2counter=3

    # Collisione con il finish
    fine_P1 = P1.collisione(finish_mask, 880, 380)
    if fine_P1 != None and P1counter == 3:
        P1_giri += 1
        P1counter = 0

    fine_P2 = P2.collisione(finish_mask, 880, 380)
    if fine_P2 != None and P2counter == 3:
        P2_giri += 1
        P2counter = 0

    # Richiamo la funzione dei giri
    contagiri(P1_giri, P2_giri)
    
    # Cronometro

    pygame.draw.rect(screen, (255, 255, 255), (700, 15, 142, 35))
    tick += 1

    if tick == 60:
        secondi += 1
        tick = 0
        font = pygame.font.SysFont(None, 50)
        if secondi < 10:
            tempo = font.render(f"00:0{minuti}:0{secondi}", True, (0, 0, 0))
            screen.blit(tempo, (700, 16))
        elif secondi >= 10:
            tempo = font.render(f"00:0{minuti}:{secondi}", True, (0, 0, 0))
            screen.blit(tempo, (700, 16))
        if secondi == 60:
            minuti += 1
            secondi = 0
    else:
        font = pygame.font.SysFont(None, 50)
        if secondi < 10:
            tempo = font.render(f"00:0{minuti}:0{secondi}", True, (0, 0, 0))
            screen.blit(tempo, (700, 16))
        elif secondi >= 10:
            tempo = font.render(f"00:0{minuti}:{secondi}", True, (0, 0, 0))
            screen.blit(tempo, (700, 16))

    # Controllo vincitore
    if P1_giri == 3:
        testo_giri = font2.render("P1 WIN !!!", True, (255, 255, 255))
        testo_giri_finale = testo_giri.get_rect(center=(lunghezza_schermo/2, altezza_schermo/2))
        screen.blit(sfondo, (0,0))
        screen.blit(testo_giri, testo_giri_finale)
        pygame.draw.rect(screen, "white", exit)
        exit.draw("Exit")
        pygame.draw.rect(screen, "white", reset)
        reset.draw("Reset")
        if finale==0:
            pygame.mixer.Sound.stop(audio)
            pygame.mixer.Sound.play(win)
            finale=1
    
    if P2_giri == 3:
        testo_giri = font2.render("P2 WIN !!!", True, (255, 255, 255))
        testo_giri_finale = testo_giri.get_rect(center=(lunghezza_schermo/2, altezza_schermo/2))
        screen.blit(sfondo,(0,0))
        screen.blit(testo_giri, testo_giri_finale)
        pygame.draw.rect(screen, "white", exit)
        exit.draw("Exit")
        pygame.draw.rect(screen, "white", reset)
        reset.draw("Reset")
        if finale==0:
            pygame.mixer.Sound.stop(audio)
            pygame.mixer.Sound.play(win)
            finale=1

    # Aggiorno schermo e clock
    pygame.display.flip()
    clock.tick(60)