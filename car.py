import pygame
import math
from utils import blit_rotate_center

class Car:
    def __init__(self, screen, image, pos, size) -> None:

        # Creazione macchina
        self.screen = screen
        self.image= image
        self.image = pygame.transform.scale(self.image, size)
        self.x, self.y = pos[0], pos[1]
        self.vel= 0
        self.vel_rot= 3
        self.angolo= 0

    # Funzione per ruotare la macchina (incremento o riduco l'angolo in base alla velocità di rotazione)
    def rotazione(self, left=False, right=False):
        if left:
            self.angolo += self.vel_rot
        elif right:
            self.angolo -= self.vel_rot

    # Movimenti avanti e indietro
    def move_forward(self):
        self.vel = 2
        self.move()

    def move_backward(self):
        self.vel = -1
        self.move()

    # Movimento legato proprio al fatto che può ruotare
    def move(self):
        radianti = math.radians(self.angolo)
        verticale = math.cos(radianti) * self.vel
        orizzontale = math.sin(radianti) * self.vel

        self.y -= verticale
        self.x -= orizzontale

    # Stop movimento
    def stop(self):
        self.vel= 0

    # Collisione
    def collisione(self, mask, x=0, y=0):
        car_mask= pygame.mask.from_surface(self.image)
        offset= (int(self.x - x), int(self.y - y))
        intersezione= mask.overlap(car_mask, offset)
        return intersezione
    
    # Rimbalzo
    def rimbalzo(self):
        self.vel= -2
        self.move()

    # Disegno macchina su schermo
    def draw(self, schermo):
        blit_rotate_center(schermo, self.image, (self.x, self.y), self.angolo)