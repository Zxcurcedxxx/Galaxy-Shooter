import pygame

SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 500, 500

ADDAST1 = pygame.USEREVENT + 1
ADDAST2 = pygame.USEREVENT + 2
ADDAST3 = pygame.USEREVENT + 3
ADDAST4 = pygame.USEREVENT + 4
ADDAST5 = pygame.USEREVENT + 5

pygame.time.set_timer(ADDAST1, 2000)
pygame.time.set_timer(ADDAST2, 6000)
pygame.time.set_timer(ADDAST3, 10000)
pygame.time.set_timer(ADDAST4, 15000)
pygame.time.set_timer(ADDAST5, 20000)

