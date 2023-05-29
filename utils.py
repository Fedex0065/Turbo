import pygame

# Funzione per ruotare la macchina nel centro
def blit_rotate_center(schermo, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)
    schermo.blit(rotated_image, new_rect.topleft)