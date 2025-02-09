import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    '''
        Cette classe nous permet de créer nos cases
    '''
    def __init__(self, pos, groups,type):
        super().__init__(groups)
        self.image = pygame.image.load(type).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10) # Petite attention au détail

