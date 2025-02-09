import pygame
from math import sin

class Entity(pygame.sprite.Sprite): # Cette classe sera la parente de Player et de Enemy, puisque qu'ils sont intrinsectement proche
    def __init__(self, groups,obstacles,superObstacles):
        super().__init__(groups)
        self.frame_index = 0
        self.animation_speed = .15
        self.direction = pygame.math.Vector2

        self.obstacle_sprite = obstacles
        self.superObstacles = superObstacles
    

    def Move(self,speed):  
        '''
            Cette fonction sert à tout les 'objets' vivants de se déplacer
            dans le cas du joueur on doit on pourrai
        '''
    
        if self.direction.magnitude() != 0: 
            self.direction = self.direction.normalize() # Utilise la norme du vecteur
        self.hitbox.x += self.direction.x * speed # On se déplace à une certaine vitesse selon la direction du vecteur
        self.collision('horizontal')
        self.superCollision('horizontal')
        self.hitbox.y += self.direction.y * speed
        
        self.collision('vertical')
        self.superCollision('vertical')

        # collision et supercollision reprentent chacun des murs, un possiblement traversable,
        # l'autre des vrais murs plus solides et plus épais que les batiments préfa...
        
        self.rect.center = self.hitbox.center # on assigne une hitbox à l'entité

    def wave_value(self):
        '''
            cette fonction se sert de l'oscillation de la fonction sinus pour retourner une valeur
            alpha, pour rendre transparent pendant une courte période les entités
        '''
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        else: 
            return 0

      # [ Les Collisions ]
    # Même principes pour les deux méthodes, on va en détailler qu'une seule    

    def collision(self,direction):
        '''
            Cette fonction va prendre en argument la direction où le joueur va aller ( elle sera déterminé )
        '''
        # Vu que les obstacles sont dans 2 groupes, Visible ET Obstacle, L'intérêt du super().__init__() prend son sens

        if direction == 'horizontal':                               # On va vérifier sur l'axe X
            for sprite in self.obstacle_sprite:                     # Pour chaque sprite qui est dans le groupe des obstacles
                if sprite.hitbox.colliderect(self.hitbox):          # On vérifie si la hitbox du sprite est en collision avec la hitbox du joueur
                    if self.direction.x > 0:                        # Si il est en collision, alors qu'il se dirige vers la droite
                        self.hitbox.right = sprite.hitbox.left      # On le téléporte à gauche du sprite
                    if self.direction.x < 0: # same mais pour la gauche
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical': # On vérifie sur l'axe Y
            for sprite in self.obstacle_sprite:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: # same pour le bas
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: # same pour le haut
                        self.hitbox.top = sprite.hitbox.bottom
    
    def superCollision(self,direction):
        '''
            Cette fonction va prendre en argument la direction où le joueur va aller ( elle sera déterminé )
            same que la collision mais pour les bordures du jeu
        '''
        if direction == 'horizontal':
            for sprite in self.superObstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0: 
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0: 
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.superObstacles:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0: 
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y < 0: 
                        self.hitbox.top = sprite.hitbox.bottom
    