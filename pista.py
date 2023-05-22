import pygame

class Pista:
    def __init__(self, screen, image, pos, size) -> None:
        
        # Creazione pista
        self.screen = screen
        self.rect=pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.image = image
        self.image=pygame.transform.scale(self.image, size)

    # Disegno pista
    def draw(self):
        self.screen.blit(self.image, self.rect)