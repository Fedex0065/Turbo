import pygame

class Pulsante:
    def __init__(self, screen, pos, size) -> None:
        self.screen=screen
        self.x=pos[0]
        self.y=pos[1]
        self.rect=pygame.Rect(self.x, self.y, size[0], size[1])
        self.surf=pygame.Surface(size)

    def draw(self):
        self.surf.fill((100,100,100))
        self.screen.blit(self.surf, self.rect)
