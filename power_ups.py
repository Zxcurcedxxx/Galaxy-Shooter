import random
import pygame
from pygame.locals import RLEACCEL

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, winsize):
        super(PowerUp, self).__init__()
        self.winwidth, self.winheight = winsize
        self.type = random.choice(['shield', 'double_shot', 'speed_boost'])
        self.surf = pygame.image.load(f'assets/powerups/{self.type}.png').convert()
        self.surf.set_colorkey((0,0,0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(20, self.winwidth-20),
                random.randint(20, self.winheight-20)
            )
        )
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > self.winheight:
            self.kill()

