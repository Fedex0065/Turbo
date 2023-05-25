import pygame

# Funzione per ruotare la macchina nel centro
def blit_rotate_center(schermo, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    schermo.blit(rotated_image, new_rect.topleft)

# Funzione per scrivere un testo nel centro
def blit_text_center(schermo, font, text):
    render = font.render(text, 1, (200, 200, 200))
    schermo.blit(render, (schermo.get_width()/2 - render.get_width() /2, schermo.get_height()/2 - render.get_height()/2))