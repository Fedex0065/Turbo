import pygame

class Pulsante:
    def __init__(self, screen, pos, size) -> None:
        self.screen=screen
        self.colore_normale = (200,200,200)
        self.colore_cliccato = (255, 255, 255)
        self.x=pos[0]
        self.y=pos[1]
        self.rect=pygame.Rect(self.x, self.y, size[0], size[1])
        self.surf=pygame.Surface(size)
        self.clicked = False

    def draw(self, testo):
        if self.clicked == True:
            colore=self.colore_cliccato
        else:
            colore=self.colore_normale

        pygame.draw.rect(self.surf, colore, self.rect, 80)

        font = pygame.font.SysFont(pygame.font.get_default_font(), int(self.rect.height * 3/4))
        scritta_image = font.render(testo, True, colore)
        scritta_rect = scritta_image.get_rect()
        scritta_rect.left = self.rect.width // 2 - scritta_rect.centerx
        scritta_rect.top = self.rect.height // 2 - scritta_rect.centery
        self.surf.blit(scritta_image, scritta_rect)
        self.screen.blit(self.surf, self.rect)
