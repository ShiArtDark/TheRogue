import pygame
from settings import *
from chrono import Chrono

class UI:
    def __init__(self):
        # Nous permet de récupérer la taille de l'écran initialisé au départ (1280x704x32)
        self.display_surface = pygame.display.get_surface()

        # On initialise 2 tailles de polices (Une grande et une plus petite)
        self.glory = pygame.font.Font(UI_FONT, 100)
        self.Title = pygame.font.Font(UI_FONT, UI_FONT_SIZE-10)
        self.font = pygame.font.Font(UI_FONT, int(UI_FONT_SIZE//2))
        self.MenuFont = pygame.font.Font(MENU_FONT,50)

        # [ ICONS ]
        # Les sprites sont mal proportionnés donc on va les upscale
        weapon = pygame.image.load('assets/graphics/player/weapon/axeIcon.png').convert_alpha()
        self.weaponSized = weapon.get_size()
        self.newWeapon = pygame.transform.scale(weapon,(self.weaponSized[0]*1.5, self.weaponSized[1]*1.5))

        dash = pygame.image.load('assets/graphics/player/weapon/DashIcon.png').convert_alpha()
        self.size = dash.get_size()
        self.newDash = pygame.transform.scale(dash,(int(self.size[0]*2), (self.size[1]*2)))
        
        # [ BAR ]
        self.health_bar_rect = pygame.Rect(25,20,HP_BAR_WIDTH, BAR_HEIGHT)

        self.Chronometre = Chrono()

    def show_bar(self,current, max_amount, bg_rect, color):
        '''
            Cette fonction prends en argument une unité , son maximum, une couleur de fond et une couleur principal
            Elle va se contenter d'afficher une barre dans le HUD
        '''
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect) # On dessine le rectangle du fond

        # On va faire la proportion
        ratio = current/max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width= current_width

        # On dessine la quantité du contenu ainsi que la bordures
        pygame.draw.rect(self.display_surface,color,current_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER,bg_rect,3) 

    # [ les SKILLS ]
    
    def display_box(self, left,top, has_Done,TYPE):
        '''
            Cette fonction prend en argument 2 coordonnées, un evenement, et une couleur de bordure ( dépendra de la compétence utilisée)
        '''
        bg_rect = pygame.Rect(left,top,ITEM_BOX_SIZE,ITEM_BOX_SIZE) # On dessine le carré du fond
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,bg_rect)
        if has_Done:
            pygame.draw.rect(self.display_surface,TYPE,bg_rect,3) # Si actif on met une couleur
        else:
            pygame.draw.rect(self.display_surface,UI_BORDER,bg_rect,3) # sinon celle de base
        return bg_rect

    
    def overlayWeapon(self,has_Attacked, TYPE):
        '''
            Cette fonction prend en argument, un évenement, et la bordure
            elle va afficher la boite de l'arme du personnage
        '''
        bg_rect = self.display_box(25,610, has_Attacked,TYPE)
        weapon_rect = self.newWeapon.get_rect(center = bg_rect.center)

        self.display_surface.blit(self.newWeapon, weapon_rect) # On affiche également l'arme
       
    def AttackKey(self,text,x,y,attacking):
        '''
            Cette fonction va afficher la touche associé à la compétence d'attaque
        '''
        if attacking:
            text_surf = self.font.render(str(text), False, BORDER_ACTIVE) # Comme l'overlay, elle va changé de couleur si actif
        else:
            text_surf = self.font.render(str(text), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(x,y))

        self.display_surface.blit(text_surf,text_rect) # On affiche la lettre
    
    # Same mais pour le dash cette fois-ci
    def overlayDash(self,canDash, TYPE):
        '''
            on met l'image du dash dans la box
        '''
        bg_rect = self.display_box(110,620, canDash,TYPE)
        dash_rect = self.newDash.get_rect(center = bg_rect.center)

        self.display_surface.blit(self.newDash, dash_rect)

    def DashKey(self,text,x,y,Dashing):
        '''
            on affiche la touche du dash
        '''
        if Dashing:
            text_surf = self.font.render(str(text), False, TEXT_COLOR)
        else:
            text_surf = self.font.render(str(text), False, DASH_BORDER)
        text_rect = text_surf.get_rect(center=(x,y))

        self.display_surface.blit(text_surf,text_rect)

    def interact(self,text,x,y,interaction):
        '''
            on affiche si à un instant T c'est possible d'intéragir
        '''
        if interaction:
            text_surf = self.Title.render(str(text), False, BORDER_ACTIVE)
        else:
            text_surf = self.Title.render(str(text), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=(x,y))

        self.display_surface.blit(text_surf,text_rect)

    # [Beaucoup de redite]    

    def ChronoDisplay(self,text, x,y):
        '''
            Cette fonction va prendre en argument la chaîne de caractère constituant le chronomètre de la classe Chrono
            On va pouvoir l'afficher
        '''
        # On veut qu'elle soit afficher au centre et en bas de l'écran  
        text_surf = self.Title.render(str(text), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomleft=(x+30,y+60))

        # On display des blocs pour plus d'esthéthisme
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,(x, y, 245, 60))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER,(x, y, 245, 60),3)

    
    def scoreDisplay(self, text, x, y):

        # C'est le score display avec pour x ,y, et text
        text_surf = self.font.render(str(text), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomright=(x+125,y+35))
        # pygame.draw.rect('la zone', la couleur du fond, pos/taille(x, y, L, l)
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,(x, y, 150, 40))
        # affichage du texte
        self.display_surface.blit(text_surf,text_rect)
        # idem mais que la bordure
        pygame.draw.rect(self.display_surface,UI_BORDER,(x, y, 150, 40),3)
    
    def roomDisplay(self, text, x, y):

        # C'est le room display avec pour x ,y, et text
        text_surf = self.font.render(str(text), False, TEXT_COLOR)
        text_rect = text_surf.get_rect(bottomleft=((WIDTH-100),y+35))
        pygame.draw.rect(self.display_surface,UI_BG_COLOR,(x, y, 100, 40))
        self.display_surface.blit(text_surf,text_rect)
        pygame.draw.rect(self.display_surface,UI_BORDER,(x, y, 100, 40),3)
    
    def Glory(self, text, x,y):
        text_surf = self.glory.render(str(text), False, UI_BG_COLOR)
        text_rect = text_surf.get_rect(center=((x,y)))
        self.display_surface.blit(text_surf,text_rect)
    
    def GloryComment(self, text, x,y):
        font = pygame.font.Font(MENU_FONT, 20)
        text_surf = font.render(str(text), False, UI_BG_COLOR)
        text_rect = text_surf.get_rect(center =((x,y)))
        self.display_surface.blit(text_surf,text_rect)
        
    def display(self, player):
        '''
            Cette fonction va afficher tout le HUD du joueur
        '''
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HP_COLOR) # la barre de vie
        self.overlayWeapon(player.attacking, BORDER_ACTIVE)
        self.overlayDash(player.canDash,DASH_BORDER)
        
        self.AttackKey('l', 90,630, player.attacking)
        self.DashKey('m',175, 630, player.canDash)
    

        if player.canInteract:
            self.display_box(580,540,player.interactionInput, BORDER_ACTIVE)
            self.interact('f', 620,580, player.interactionInput)
            
