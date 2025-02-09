import pygame, time
from settings import *
from support import import_folder
from random import randint
from entity import Entity

class Player(Entity): # Cette classe est dérivé d'une autre classe (pygame.sprite.Sprite)

    # Une sous-classe:
    # C'est une classe qui va pouvoir reprendre les mêmes propriétés que la classe mère.
    '''
        Cette classe permet de créer un joueur
    '''
    def __init__(self,pos,groups,obstacles,superObstacles, createAttack, destroyAttack):
        '''
        --------------------------------------------
        L'initialisation prends plusieurs arguments 
        --------------------------------------------

        pos, un tuple de coordonnées x,y

        [ Groupe ]
        "groups", Concerne majoritairement les sprites uniquement visuels
        "obstacle", idem, pour les obstacles mineurs ( selon certaines conditions ils sont traversables )
        "superObstacle", idem, pour les obstacles majeurs ( par exemple les bordures )

        # Les groupes c'est une méthode qui permet de rassembler plusieurs éléments à un même niveau

        "createAttack" et "destroyAttack", deux méthodes appelées dans Level qui vienne de Weapon.py
        '''

        super().__init__(groups,obstacles,superObstacles) # ce super().init permettra de faire apparaître le joueur
        # super().init permet de crée un objet avec les mêmes caractéristiques que la parente (Player)
        # Dans notre cas 'groups' correspond à VisibleSprite

        self.image = pygame.image.load('assets/basics/player3.png').convert_alpha() # On init une image du joueur (alpha, permet de retirer le fond d'un png)
        self.rect = self.image.get_rect(topleft=pos) # on initialise la taille par rapport à celle de l'image importée précedemment
        self.hitbox = self.rect.inflate(0,-26)  # on ajuste la hitbox en conséquence


        self.importPlayerAssets() # on importe tout les sprites du persos
        
        # [ ATK ]
        self.attacking = False
        self.canNewAttack = True
        self.canNewAttackCD = 600
        self.attackCD = 300 # Le cooldown, le délais avant de pouvoir re-attaquer - on pourra le réduire in-game
        self.attackTime = None
        self.create_attack = createAttack
        self.destroy_attack = destroyAttack

        self.monsterKilled = 0
        
        # [ Mouvement ]
        self.has_Firstmoved = False
        self.direction =pygame.math.Vector2() # On utilisera des vecteurs pour les déplacements
        self.lastDirectX = 0
        self.lastDirectY = 0
        self.speed = 4 # La vitesse pourra être modifié en jeu
        

        # [ Dash ]
        self.dashInput = False
        self.canDash = True
        self.startTime = 0
        self.dashCD = 1200 # Le cooldown, le délais avant de pouvoir re-dash
        self.isDashing = False

        # [ Animation]
        self.status = 'down'
        self.frame_index = 0
        self.animationSpeed = .04 # le délais avant de switch à la frame d'après

        # [ SFX ]
        self.dashSound = [pygame.mixer.Sound('assets/sound/SFX/dash.wav'), pygame.mixer.Sound('assets/sound/SFX/dash2.ogg'),pygame.mixer.Sound('assets/sound/SFX/dash3.mp3') ]
        self.attackSound = [pygame.mixer.Sound('assets/sound/SFX/axe.wav'),pygame.mixer.Sound('assets/sound/SFX/axe2.wav'), pygame.mixer.Sound('assets/sound/SFX/axe3.wav')]
        pygame.mixer.Channel(0).set_volume(.25)
    
        # [ Collision ]
        # On utilisera 2 types de collision pour une capicité spéciale qui permettra de traverser un mur
        self.obstacle_sprite = obstacles 
        self.superObstacles = superObstacles # les bordures
        # [ Stats ]
        self.stats = { 'health': 100, 'attack': 20, 'countATK': 0, 'speed': 4, 'score': 0}

        self.health = self.stats['health']
        self.attack = self.stats['attack']
        self.CountATK = self.stats['countATK']
        self.speed = self.stats['speed']
        self.score = self.stats['score']

        self.vulnerable = True
        self.hurt_time = None
        self.invicibility_duration = 500


        # [ WIN CONDITION ]
        self.interactionInput = False

        self.NorthGate = False
        self.SouthGate = False
        self.EastGate = False
        self.WestGate = False
        self.canInteract = False

        self.idDead = False

    def importPlayerAssets(self): # On va importer chaque sprites
        chara_path = 'assets/graphics/player/' # le chemin d'accès

        # [On met les sprites dans un dictionnaire avec le nom de l'action comme clé ]

        # initialisation d'un dictionnaire de tout les états du joueurs
        self.animation = {'up': [], 'down' : [], 'left' : [], 'right' : [],
                          'up_idle': [], 'down_idle' : [], 'left_idle' : [], 'right_idle' : [],
                          'up_attack': [], 'down_attack' : [], 'left_attack' : [], 'right_attack' : []
                          }
        # on préconnisera des listes, pour l'animation ( explication en détail dans animation()]


        # ajout dans le dico
        for animation in self.animation.keys():
            fullPath = chara_path+animation # la clé va correspondre au dossier du sprite en question à charger
            self.animation[animation] = import_folder(fullPath) # plus d'info dans support.py
        
    
    def getStatus(self):
        '''
        ---------------------------------------------------------------------
        Cette fonction va chercher le status du joueur selon chaque action,
        ---------------------------------------------------------------------

        [ ETAT ]
        '_idle', le perso est passif
        '_attack', le perso est entrain d'attaquer

        [ Direction ]
        up
        down
        left
        right
        '''
        
        if self.direction.x == 0 and self.direction.y == 0: # si le joueur ne bouge pas ou n'attaque pas, on le considère comme _idle
            if not 'idle' in self.status and not 'attack' in self.status: 
                self.status = self.status +'_idle' # on le définit comme idle
        
        if self.attacking: # si le joueur attaque
            # Il va être immobile
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status : # changement de statut en attaque
                if 'idle' in self.status :
                    self.status = self.status.replace('_idle','_attack') # si il était immobile
                else:
                    self.status = self.status + '_attack' # si il attaque en mouvement
        else:
            if 'attack' in self.status:
                self.status = self.status.replace('_attack','') # Une fois l'attaque terminée on doit retirer le statut

    def input(self):
        '''
            Cette fonction va récupérer tout les inputs que le joueurs va faire
        '''
        # on reset le mouvement du personnage
        self.direction.y = 0
        self.direction.x = 0
        if not self.attacking:
            keys = pygame.key.get_pressed()
            
            # [ Dash Input]
            if keys[pygame.K_m]: 
                self.dashInput = True
                self.has_Firstmoved = True
            else:
                self.dashInput = False
            
            # [ Interaction ]
            if keys[pygame.K_f]:
                self.interactionInput = True
                self.has_Firstmoved = True
            else:
                self.interactionInput = False
                
            # [ Move Input ]
            # On se demande si utiliser les flèches c'est pas une mauvaise idées :/
            # Axe Y
            if (keys[pygame.K_DOWN] and keys[pygame.K_UP]) or (keys[pygame.K_z] and keys[pygame.K_s]):
                self.direction.y = 0
            elif keys[pygame.K_UP] or keys[pygame.K_z] :
                self.has_Firstmoved = True
                self.status = 'up'
                self.direction.y = -1
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.has_Firstmoved = True
                self.status = 'down'
                self.direction.y = 1
            # Axe X
            if (keys[pygame.K_RIGHT] and keys[pygame.K_LEFT]) or ( keys[pygame.K_q] and keys[pygame.K_d]):
                self.direction.x = 0
            elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.has_Firstmoved = True
                self.status = 'right'
                self.direction.x = 1
            elif keys[pygame.K_LEFT] or keys[pygame.K_q]:
                self.has_Firstmoved = True
                self.status = 'left'
                self.direction.x = -1

            # [ Attack + Spéciale 1 ]
            if keys[pygame.K_l] and not self.attacking and self.canNewAttack:
                self.has_Firstmoved = True
                self.CountATK += 1
                pygame.mixer.Channel(0).play(self.attackSound[randint(0,2)])
                self.attacking = True
                self.canNewAttack = False
                self.attackTime = pygame.time.get_ticks()
                self.create_attack()
              
    def Move(self,speed):
        '''
            Elle prend en argument, speed, une force pour le vecteur
            Cette méthode va s'occuper de modifier les mouvements + du dash
        '''
        endTime = pygame.time.get_ticks() # C'est une variable de temps qui va nous permettre de jauger les délais
        
        if self.direction.magnitude() != 0: 
            # ( Merci Pythagore )
            # Empêche les diagonales trop grande
            self.direction = self.direction.normalize() # Utilise la norme du vecteur

        if endTime - self.startTime > 100: # Le délais de longueur, le temps actif PENDANT le dash
            self.isDashing = False
        
        if endTime - self.startTime > self.dashCD: # Le délais avant de pouvoir re-dash
            self.canDash = True

        if self.dashInput and self.canDash and not self.attacking:  # Activation du Dash
            pygame.mixer.Channel(0).play(self.dashSound[randint(0,2)])
            self.isDashing = True
            self.canDash = False
            self.startTime = pygame.time.get_ticks() # On garde la dernière fois qu'on a dash
            self.lastDirectX = self.direction.x # On garde la dernière direction
            self.lastDirectY = self.direction.y
        
        
        if self.isDashing and not self.attacking: # Execution du Dash
            self.direction.x= self.lastDirectX
            self.direction.y = self.lastDirectY

            # [ Deplacement à une certaine pouissance ]
            self.hitbox.x += self.direction.x * 20

            #self.collision('horizontal') # Grâce à un modifier in-game on peut on/off les collisions mineurs ( " c'est pas un bug, c'est une feature découverte sans faire exprès ")
            self.superCollision('horizontal') 
            self.hitbox.y += self.direction.y * 20
            #self.collision('vertical')
            self.superCollision('vertical')
            self.rect.center = self.hitbox.center # permet de fixer la dernière position à la fin du dash

        else:
            # [ Basic Move ]
            # On procède au déplacement vecteur*force
            # Les superCollision et Collision vont faire effet uniquement s'il y a une valeur quelconque en x
            self.hitbox.x += self.direction.x * speed
            self.collision('horizontal')
            self.superCollision('horizontal')
            self.hitbox.y += self.direction.y * speed
            # Les superCollision et Collision vont faire effet uniquement s'il y a une valeur quelconque en y
            self.collision('vertical')
            self.superCollision('vertical')
            self.rect.center = self.hitbox.center

    def get_full_damage_weapon(self):
        return self.attack
            
    def Cooldowns(self):
        '''
            Cette Méthode prend aucun argument et retourne RIENN, NADDAA, QUETCHI
            Elle va simplement faire le Cooldown ( comme le dash pour les attaques )
        '''
        endTime = pygame.time.get_ticks()

        if self.attacking: # Même principe que pour le dash
            if endTime - self.attackTime >= self.attackCD:
                self.attacking = False
                self.destroy_attack() # On détruit bien le sprite d'attaque à la fin ( c'est plus propre )

        if not self.canNewAttack:
            if endTime - self.attackTime >= self.canNewAttackCD:
                self.canNewAttack = True


        if not self.vulnerable:
            if endTime - self.hurt_time >= self.invicibility_duration:
                self.vulnerable = True

    def animate(self):
        '''
            Cette méthode va s'occuper de l'animation des sprite
        '''

        # Dans le principe, plus haut on a importé nos assets.

        # Les listes représentent la suite de sprite qui va constitué l'animation
        # pour rappel une animation, c'est une succession d'image. Donc les listes sont composé de sprite qui donne l'illusion d'animation

        animation = self.animation[self.status] # On a nommé exprès nos états comme le noms des clés

        self.frame_index += self.animationSpeed 
        if self.frame_index >= len(animation):
            self.frame_index = 0 # On boucle, on répète l'animation


        self.image = animation[int(self.frame_index)] # On change d'indice quand c'est on passe à l'entier supérieur, un indice ne peut être un float
        self.rect = self.image.get_rect(center = self.hitbox.center) # On recentre l'image par rapport à l'affichage du joueur

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)


 
    
    def set_stats(self, health, attack,countAtk, speed,score):
        '''
            on rétablit les stats lors de la synchronisation de salle
        '''
        self.health = health
        self.attack = attack
        self.CountATK = countAtk
        self.speed = speed
        self.score = score

    def check_Death(self):
        if self.health <= 0:
            return True
        else:
            return False
                        
    def update(self):
        '''
            Cette fonction va être appelé constamment et exécuter toutes les méthodes importantes
        '''
        self.input()
        self.Cooldowns()
        self.getStatus()
        self.animate()
        self.Move(self.speed)
        