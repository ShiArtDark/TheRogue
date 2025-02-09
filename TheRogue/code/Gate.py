import pygame
from settings import *
from Player import Player


class Gate(pygame.sprite.Sprite):
    '''
        Cette classe nous permet de créer nos cases
    '''
    def __init__(self, groups,visibleSprites):
        super().__init__(groups)
        self.image = pygame.image.load('assets/basics/Gate.png').convert_alpha()
        self.rect = self.image.get_rect(center = (0,0))
        self.display_surface = pygame.display.get_surface() 

        # [ Coordonnée et affichage des hitboxs des portes ]
        self.Nx,self.Ny = WIDTH//2, 32
        self.Sx, self.Sy = WIDTH//2, HEIGHT-32
        self.Wx, self.Wy = 32, HEIGHT//2
        self.Ex, self.Ey = WIDTH-32, HEIGHT//2

        # Les carré affiché vont permettre de déterminer la zone ou le joueur peut intéragir avec la porte
        self.North = pygame.draw.rect(self.display_surface,(12, 12, 12),(self.Nx-50,self.Ny-50, 100,100))
        self.South = pygame.draw.rect(self.display_surface,(12, 12, 12),(self.Sx-50,self.Sy-50, 100,100))
        self.West = pygame.draw.rect(self.display_surface,(12, 12, 12),(self.Wx-50,self.Wy-50, 100,100))
        self.East = pygame.draw.rect(self.display_surface,(12, 12, 12),(self.Ex-50,self.Ey-50, 100,100))


        self.visibleSprite = visibleSprites
    

    def run(self,player):
        '''
            Cette méthode va detecter si une collision est faite entre le joueur et une porte, en précisant laquelle
        '''
        # on check si le joueur est en collision avec une de nos portes
        if player.hitbox.colliderect(self.North) or player.hitbox.colliderect(self.South) or player.hitbox.colliderect(self.West) or player.hitbox.colliderect(self.East):
            # si c'est le cas quel porte est-il entrain d'intéragir
            # au moins il l'ouvrira plus de porte qu'on peut en ouvrir sur Parcoursup

            if player.hitbox.colliderect(self.North):
                player.NorthGate = True
            elif player.hitbox.colliderect(self.South):
                player.SouthGate = True
            elif player.hitbox.colliderect(self.East):
                player.EastGate = True
            elif player.hitbox.colliderect(self.West):
                player.WestGate = True

            player.canInteract = True
        else: 
            # si il intéragit avec rien, bah c'est assez explicite
            player.canInteract = False
            player.SouthGate = False
            player.EastGate = False
            player.NorthGate = False
            player.WestGate = False