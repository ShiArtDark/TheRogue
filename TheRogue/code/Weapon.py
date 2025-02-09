import pygame


class Weapon(pygame.sprite.Sprite):
    def __init__(self,player, groups):
        super().__init__(groups)
        self.sprite_type = 'weapon'

        direction = player.status.split('_')[0] # dans la fonction joueur on a trié dans l'odre d'apparition donc le premier est le dernier statut éxécuté
        # On récupère le statut du joueur mais uniquement sa direction
        full_path = f'assets/graphics/player/weapon/{direction}.png' # le formatage qui aide très bien pour éviter la répétion inutile
        self.image = pygame.image.load(full_path).convert_alpha() # on import les assets sur fond transparent

        # [ Placement ]
      
        if direction == 'right':
            self.rect = self.image.get_rect(midleft = player.rect.midright + pygame.math.Vector2(-10,20))
        elif direction == 'left': 
            self.rect = self.image.get_rect(midright = player.rect.midleft + pygame.math.Vector2(10,20))
        elif direction == 'down':
            self.rect = self.image.get_rect(midtop = player.rect.midbottom + pygame.math.Vector2(-10,0))
        else:
            self.rect = self.image.get_rect(midbottom = player.rect.midtop + pygame.math.Vector2(-10,0))