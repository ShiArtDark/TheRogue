import pygame
from settings import *
from map import *
from Tile import Tile
from Player import Player
from Weapon import Weapon
from enemy import *
from Gate import *
from chrono import Chrono
from UI import UI
from random import *


class Level: 
    '''
        La classe Level, va générer toutes les salles ainsi que les entités dedans
    '''
    def __init__(self):
        
        # affichage du fond / le sol de la piece
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        image = pygame.image.load('assets/graphics/Texture/holder/backgroundMenu.png')
        self.bg_img = pygame.transform.scale(image, (WIDTH*1.2,HEIGHT*1.2))
        self.bg_rect = self.bg_img.get_rect(center = (WIDTH//2, HEIGHT//2))
        self.screen.blit(self.bg_img, self.bg_rect)

        self.displaySurface = pygame.display.get_surface()
        self.visibleSprites = YSortCameraGroup() # Tentative de caméra

        
        # [ Obstacle ]
        # On les assigne à un groupe
        self.obstacleSprites = pygame.sprite.Group() 
        self.SuperObstacleSprites = pygame.sprite.Group()

        # les portes sont inexistante à l'entrée de la piece
        self.North = None
        self.South = None
        self.West = None
        self.East = None

        # la premiere fois que le joueur apparait c'est au centre d'une salle
        self.x, self.y = WIDTH//2, HEIGHT//2

        # nomination des attaques
        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()

        # systeme d'étage
        self.mapIndex = 0
        self.mapActif = self.createMap(ROAD) # On crée la map
        self.floor = 0
        self.floor_ui = 1
        self.room_ui = 0
        self.counter = 0
        self.createMonster(self.floor)
        
        # affichage de l'interface
        self.ui = UI()
        self.user = ''
        self.UserInput = None

        self.music = None
        self.new_music = 'assets/sound/Music/Battle.mp3'

        # init du chrono
        self.Chronometre = Chrono()

        # condition de victoire / défaite
        self.win = False
        self.lose = False
        self.LastStats = None


    # La création de la map
    def createMap(self,ROAD):
        '''
            Cette fonction prends en argument, une liste de map généré aléatoirement ( sauf quelques salle clés)

            Elle va prendre une matrice et crée la map en question en suivant un pattern défini dans settings.py et map.py
        '''
        
        # Ceci est un message de Théo : si vous avez une bonne vue, je vous déconseille d'allez voir 
        # les maps qu'on a crée, c'est un calvaire pour tout le monde
        # - Ceux qui l'ont coder et réfléchit
        # - ceux qui essayent de la comprendre

        # J'ai compté y'a 23 assets différentes POUR DES MURS.
        for row_index,row in enumerate(ROAD[self.mapIndex]): # enumerate permet de numéroter chaque ligne
            for col_index, col in enumerate(row): # pour les colonne
                x = col_index * TILESIZE # On adapte à une taille (32x32)
                y = row_index * TILESIZE
                if col == 'X': # Bordure
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/wall.png') # On assigne le fonction du bloc à des groupes
                if col == 'Y': # Obstacle traversable
                    Tile((x,y),[self.visibleSprites,self.obstacleSprites], 'assets/graphics/Texture/Wall/wall.png')
                if col == 'P': # le joueur
                    self.player = Player((self.x,self.y),[self.visibleSprites],self.obstacleSprites,self.SuperObstacleSprites, self.create_attack, self.destroy_attack)

                # Wall

                if col == 'TW': # Top Wall
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/TopWall.png')
                if col == 'TRW': # Top Right Wall
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/TopRightCorner.png')
                if col == 'RW': # Right Wall
                    Tile((x,y),[self.visibleSprites], 'assets/graphics/Texture/Wall/RightWall.png')
                if col == 'BRW': # Bottom Right Wall
                    Tile((x,y),[self.visibleSprites], 'assets/graphics/Texture/Wall/RightinnerCorner.png')
                if col == 'BW': # Bottom Wall
                    Tile((x,y),[self.visibleSprites], 'assets/graphics/Texture/Wall/BottomWall.png')
                if col == 'BLW': # Bottom Left Wall
                    Tile((x,y),[self.visibleSprites], 'assets/graphics/Texture/Wall/LeftinnerCorner.png')
                if col == 'LW': # Left Wall
                    Tile((x,y),[self.visibleSprites], 'assets/graphics/Texture/Wall/LeftWall.png')
                if col == 'TLW': # Top Left Wall
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/TopLeftCorner.png')

                if col == 'ILW': # Inner Left Corner Wall
                    Tile((x,y),[self.visibleSprites,self.obstacleSprites], 'assets/graphics/Texture/Wall/InnerLeftCorner.png')
                if col == 'IRW': # Inner Right Corner Wall
                    Tile((x,y),[self.visibleSprites,self.obstacleSprites], 'assets/graphics/Texture/Wall/InnerRightCorner.png')
                
                if col == 'HGW': # Inner Left Wall
                    Tile((x,y),[self.visibleSprites], 'assets/graphics/Texture/Wall/lefttopcornerright.png')
                if col == 'BGW': # Inner Left Wall
                    Tile((x,y),[self.visibleSprites], 'assets/graphics/Texture/Wall/leftcornerright.png')
                if col == 'BDW': # Inner Left Wall
                    Tile((x,y),[self.visibleSprites], 'assets/graphics/Texture/Wall/cornerright.png')
                if col == 'HDW': # Inner Left Wall
                    Tile((x,y),[self.visibleSprites], 'assets/graphics/Texture/Wall/topcornerright.png')

                # Gates

                if col == 'TLG': # Top Left Gate
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/TopLeftGate.png')
                if col == 'TRG': # Top Right Gate
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/TopRightGate.png')
                if col == 'RG': # Right Gate
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/RightGate.png')
                if col == 'BLG': # Bottom Left Gate
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/BottomLeftGate.png')
                if col == 'BRG': # Bottom Right Gate
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/BottomRightGate.png')
                if col == 'LG': # Left Gate
                    Tile((x,y),[self.visibleSprites,self.SuperObstacleSprites], 'assets/graphics/Texture/Wall/LeftGate.png')
                
    
    
    def createMonster(self, floor):
        '''
            Cette fonction va déterminer l'apparition ou non de monstre par rapport à l'étage
        '''
        if floor == 0 or floor == 5 or floor == 10 or floor == 15: # Salles spéciales
            canSpawn = False
        else:
            canSpawn = True

        if canSpawn:
            # La diffculté de chaque salle augmentera progressivement

            if floor < 5:
                mob = randint(2,4)
            elif floor > 5 and floor < 10:
                mob = randint(5,7)
            else:
                mob = randint(8,10)
            self.counter = 0 # on initialise un compteur à 0 qui sera reset à chaque étage, ça coresspondera au nombre de monstre
            while self.counter <= mob:
                # Tant que le nombre de mob n'est pas atteint on continue de les faire apparaitre

                for row_index,row in enumerate(PATTERN): # PATTERN se situe dans map.py, c'est les points de spawns des monstres
                    for col_index, col in enumerate(row): 
                        x = col_index * TILESIZE # On adapte à une taille (64x64)
                        y = row_index * TILESIZE  

                        if col == 'O':
                            self.counter += 1
                            Enemy('spirit',(x,y),[self.visibleSprites, self.attackable_sprites], self.obstacleSprites, self.SuperObstacleSprites, self.damage_player)
                
                        if self.counter >= mob: # si le nombre de mob est atteint on arrête 
                            return
                        
        if floor == 15: # Derniere salle, avec 2 boss monstrueusement dangereux... arouuuu
            self.counter = 2
            Enemy('racoon', (426,356),[self.visibleSprites, self.attackable_sprites], self.obstacleSprites, self.SuperObstacleSprites, self.damage_player)
            Enemy('samourai', (853,356),[self.visibleSprites, self.attackable_sprites], self.obstacleSprites, self.SuperObstacleSprites, self.damage_player)


        elif floor == 5 or floor ==  10: # un boss
            self.counter = 1
            Monster = ['racoon', 'samourai']
            Enemy(Monster[randint(0,1)], (640,356),[self.visibleSprites, self.attackable_sprites], self.obstacleSprites, self.SuperObstacleSprites, self.damage_player)            



    # [ Les Attaques ]
    # C'est un objet indépendant du joueur qui va apparaitre et disparaitre
    def create_attack(self):
        '''
            cette méthode va crée une attaque (sprite + hitbox)
        '''
        self.current_attack = Weapon(self.player,[self.visibleSprites, self.attack_sprites])

    def destroy_attack(self):
        '''
            Pour éviter les débris des armes, on va supprimer l'attaque précédemment généré
        '''
        if self.current_attack:
            self.current_attack.kill()
        self.current_attack = None 
    
    def ChangeZone(self, player):
        '''
            cette méthode sert à changer d'étage
        '''
        
        if player.canInteract and player.interactionInput:
        # Garder en mémoire toutes les stats 

            Lasthealth = player.health + 15
            if Lasthealth > player.stats['health']:
                Lasthealth = player.stats['health']
            Lastattack = player.attack + .3
            LastCountATK = player.CountATK
            Lastspeed = player.speed
            LastScore = player.score + 250 # Bonus d'étage
            

        # Tout détruire
            self.obstacleSprites.empty()
            self.visibleSprites.empty()
            self.SuperObstacleSprites.empty()
            self.player.kill()
            self.Gate.kill()

            if player.NorthGate:
                self.x, self.y = WIDTH//2, HEIGHT - 96
            if player.SouthGate:
                self.x, self.y = WIDTH//2, 96
            if player.EastGate:
                self.x, self.y = 128, HEIGHT//2 -64
            if player.WestGate:
                self.x, self.y = WIDTH - 128, HEIGHT//2 -64
        # Reconstruire
            
            self.mapIndex += 1
            self.floor += 1

            if (self.room_ui)%5 == 0 and self.room_ui !=0:
                self.room_ui = 1
                self.floor_ui += 1
            else:
                self.room_ui += 1

            if self.mapIndex > len(ROAD)-1:
                self.mapIndex = 0
            self.createMap(ROAD)
            self.createMonster(self.floor)
        
        # Réattribution

            self.player.set_stats(Lasthealth, Lastattack,LastCountATK, Lastspeed, LastScore)

    
    def player_attack_logic(self):
        '''
            Cette fonction va nous permettre de faire la distribution de dégats au monstre
        '''
        if self.attack_sprites:
            # on fait une recherche des sprites dans le groupe attack sprite
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
                if collision_sprites:
                    for target_sprite in collision_sprites: # si on attaque et que ça collisionne avec notre arme, on deal des dégats
                        
                        if target_sprite.sprite_type == 'enemy':
                            target_sprite.get_damage(self.player, attack_sprite.sprite_type)
                        
    def damage_player(self, amount):
        '''
            Cette fonction va nous distribuer les dégats qu'on va recevoir
        '''
        if self.player.vulnerable:
            self.player.health -= amount
            if (self.player.score-75) <= 0 :
                self.player.score=0
            else:
                self.player.score -= 75 # On punit le joeur de quelques points pour avoir été touché
            self.player.vulnerable = False
            self.player.hurt_time = pygame.time.get_ticks()
    
    
    def check_Death(self):
        '''
            cette méthode nous permet de kill le joueur quand il a plus de points de vie
        '''
        if self.player.health <= 0:
            self.player.kill()
    
    def getStats(self):
        '''
            cette méthode va nous permettre de récuperer toutes infos pour la base de donnée ( self.player.countATK c'est assez anecdoctique on hésitait )
        '''
        return (self.player.score, self.Chronometre.Timer_get(), self.player.CountATK)


    def run(self):
        '''
            La méthode run nous permet d'appeler toutes les autres méthodes et vont constituer le jeu
        '''
        if not self.win:
            self.screen.blit(self.bg_img, self.bg_rect)
        
        # [ On met une musique d'ambiance]
        if self.music!=self.new_music: # Si la musique n'est pas la meme 
            self.music=self.new_music # On echange l'ancienne par la nouvelle
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load(self.music)
            pygame.mixer.music.play(loops=-1) # loop -1 = ca boucle

        if self.player.health<=0: # Si le perso meurt
            self.new_music='assets/sound/Music/Title.mp3'

        else:
            if self.floor == 15:
                self.new_music ='assets/sound/Music/EpicBoss.mp3'
                pygame.mixer.music.set_volume(.6)
            elif self.floor==5 or self.floor==10 : # Si il est dans une salle de boss, on change la musique pour une musique + épique
                self.new_music='assets/sound/Music/Boss.mp3'
            else:
                self.new_music='assets/sound/Music/Battle.mp3' # Sinon c'est la musique de base


        # On gagne à partir de la 16e salle
        if self.floor == 16: # Victoire

            self.playerScore = self.player.score # on récupère le score puis on tue le joueur pour provoquer volontairement la fin
            self.player.health = -100
            self.check_Death() 
            self.win = True

            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('assets/sound/Music/Title.mp3')
            pygame.mixer.music.play(loops=-1)

            self.ui.Glory('The Rogue, Complete', WIDTH//2, 310)
            
            self.tempsTotal = self.Chronometre.Timer_get(True)
            self.ui.ChronoDisplay(self.tempsTotal,WIDTH//2-(245//2), 400)



        elif self.player.health <= 0: # ecran de Game Over
            self.lose = True

            self.player.kill()
            #pygame.mixer.Channel(3).play('assets/sound/SFX/onePUNCHRacoon.mp3')
            tempsTotal = self.Chronometre.Timer_get(self.player.has_Firstmoved)
            self.ui.Glory('Vous etes mort...', WIDTH//2, 310)
            self.ui.ChronoDisplay(tempsTotal,WIDTH//2-(245//2), 400)
            

        else: # Actualisation si le joueur n'est ni mort ni vivant
            
            if self.counter <= self.player.monsterKilled:
                self.Gate = Gate([self.visibleSprites],self.visibleSprites)

                self.ChangeZone(self.player)
            
            
            self.visibleSprites.custom_draw(self.player)
            self.visibleSprites.enemy_update(self.player)
            self.visibleSprites.update()
            self.player_attack_logic()

            self.Gate.run(self.player)
            
            self.ui.display(self.player)
            self.ui.scoreDisplay(self.player.score, WIDTH-175, 650)
            self.ui.ChronoDisplay(self.Chronometre.ChronoUpdate(self.player.has_Firstmoved), WIDTH-275, 50)
            self.ui.roomDisplay((str(self.floor_ui)+' - '+str(self.room_ui)), WIDTH-140, 150)
            
        
        
    

class YSortCameraGroup(pygame.sprite.Group):

    '''
        Cette class est dérivée de la classe pygame.sprite.Sprite
        Elle va nous permettre de concevoir une caméra qui pourra bouger
    '''
    def __init__(self):
        super().__init__() 
        
        self.displaySurface = pygame.display.get_surface()

        self.halfWidth = self.displaySurface.get_size()[0]//2
        self.halfHeight = self.displaySurface.get_size()[1]//2
                
        self.offset = pygame.math.Vector2()
    
    def custom_draw(self,player):
        '''
            Cette méthode nous permet de faire la même chose que la fonction .draw déjà présente dans pygame, 
            à la différence que dans celle ci on peut décaler les sprites et simuler cette caméra
        '''
        self.offset.x = player.rect.centerx - self.halfWidth
        self.offset.y = player.rect.centery - self.halfHeight

        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            offset_pos= sprite.rect.topleft - self.offset//22
            self.displaySurface.blit(sprite.image, offset_pos)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
        
        
                

        
