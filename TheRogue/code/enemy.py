import pygame
from settings import *
from entity import Entity
from support import *
import random

class Enemy(Entity): # -> Cette classe est dérivée d'Entity
    def __init__(self, monster_name, pos,groups, obstacleSprites, superObstacle, damage_player):

        super().__init__(groups, obstacleSprites, superObstacle)
        self.sprite_type = 'enemy' # On met un attribut 

        self.import_graphics(monster_name) # on import les assets des monstres

        # on initialise les données basiques
        self.status = 'idle'
        self.image = pygame.image.load('assets/basics/obstacle3.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-10)

        
        self.image = self.animations[self.status][self.frame_index].convert_alpha()


        self.monster_name = monster_name
        
        # [ On ajoute les data des monstres ]
    
        monster_info = monster_data[self.monster_name]
        self.health = monster_info['health'] + random.randint(-25,25)
        self.speed = monster_info['speed'] + round(random.uniform(-0.5, 0.5), 2) # random.uniform(décimal, décimal) --> générer nombre decimal et , round(nombre_decimal, 2) pour 2 chiffres apres la virgule
        self.attack_damage = monster_info['damage'] + random.randint(-5,15)
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius'] + random.randint(-40,40)
        self.score = monster_info['score']
        self.attack_type= monster_info['attack_type']
        self.animation_speed = monster_info['animationSpeed']
        self.attackSound = pygame.mixer.Sound(monster_info['attackSound'])
        self.attackSound.set_volume(.5)
        self.deathSound = pygame.mixer.Sound('assets/sound/SFX/deathSound.wav')
        self.deathSound.set_volume(.4)

        # [ Degat ]
        self.can_attack = True
        self.attack_time = None
        self.attackCD = 1000
        self.damage_player = damage_player
        

        # Invulnerability

        self.vulnerable = True
        self.hit_time = None
        self.invicibility_duration = 400
        
    
    def import_graphics(self, name):
        '''
            Cette fonction est la même que l'import dans la class Joueur
        '''
        self.animations = {'idle':[], 'move':[],'attack': []}
        main_path = f'assets/graphics/monster/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)


    def get_player_distance_direction(self, player):
        '''
            Cette fontion permet de diriger le monstre vers le joueur grâce à des vecteurs
        '''
        enemy_vec= pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude() # Vecteur direction joueur enenmy

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize() # on le normalise
        else:
            direction = pygame.math.Vector2()

        return (distance, direction)
    
    def get_status(self, player):
        '''
            On change l'état du monstre si il bouge, ou non, ou attaque
        '''
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'

        elif distance <= self.notice_radius:
            self.status = 'move'
        else:
            self.status ='idle'
        
    def actions(self, player):
        '''
            suite des deux fonctions du dessus, les actions en conséquences
        '''
        if self.status == 'attack':
            pygame.mixer.Channel(1).play(self.attackSound)
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)

        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        '''
            Cette fonction nous permet d'animer nos sprites
        '''
        animation = self.animations[self.status]
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                    
                    self.can_attack = False
            
            self.frame_index = 0
       
        
        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable: # Permet de signifier les dégats
            alpha = self.wave_value() # fonction dans Entity (utilise la courbe sinus)
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        '''
            permet d'assurer un délais entre chaque attaque
        '''
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.attackCD:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invicibility_duration:
                self.vulnerable = True


    def get_damage(self,player, attack_type):
        '''
            cette fonction va permettre de distribuer les dégats aux monstres
        '''
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if attack_type == 'weapon':
                player.score += 25
                self.health -= player.get_full_damage_weapon()

            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        '''
            on check si la condition de survie du monstre n'est pas à découvert
        '''
        if self.health <= 0:
            pygame.mixer.Channel(3).play(self.deathSound)
            self.kill()


    def scoreKill(self, player):
        '''
            incrémente au joueur des valeurs
        '''
        if self.health < 0:
            player.score += self.score
            player.monsterKilled += 1 # au final nous sert à rien
    
    def hit_reaction(self):
        '''
            permet de donner du recul au monstre
        '''
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        '''
            cette update va uniquement concerner l'objet en lui même
        '''
        self.hit_reaction()
        self.Move(self.speed)
        self.animate()
        self.cooldowns()   
        self.check_death()

    def enemy_update(self, player):
        '''
            cette update la va devoir se servir de la classe joueur pour fonctionner
        '''

        self.get_status(player)
        self.actions(player)
        self.scoreKill(player)
        
        
        
        