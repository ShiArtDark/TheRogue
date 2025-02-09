import pygame, sys
from Level import *
from Player import *
from settings import *
from RogueBaseDedonnee import *
from UI import *


# Liste de Bienfaits ( a faire en sql)

class Game: # Initialisation d'une classe Jeu
    '''
        Cette classe permet de créer notre jeu
    '''

    def __init__(self):
        '''
            On va initialiser toutes les variables
        '''

        # [ Initialisation basique ]
        pygame.init() # Init. pygame (setup de la fenêtre)
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.display_surface = pygame.display.get_surface()
        
        pygame.display.set_caption("TheRogue")

        # [ On ajoute des objets ]
        self.clock = pygame.time.Clock() # Le taux de raffraichissement de la fenêtre
        self.level = None # On initialise notre niveau avec la classe Level ( on le fera plus tard dans une méthode )
        self.DBBScripter = DataBase()
        self.ui = UI()

        # [ Sound]
        pygame.mixer.set_num_channels(10) # On setup la partie sonore du jeu
        pygame.mixer.music.set_volume(.3)

        self.music_played = 'debug'

        self.Menufont = pygame.font.Font(MENU_FONT, 75) # On initialise des polices de différentes tailles
        self.font = pygame.font.Font(MENU_FONT, 50)
        self.taskfont = pygame.font.Font(MENU_FONT, 30)
        

        # [ Interface ]
        holderUI = pygame.image.load("assets/graphics/Texture/holder/holder.png")
        self.newHolder = pygame.transform.scale(holderUI,(500,100))
        bg_image = pygame.image.load('assets/graphics/Texture/holder/backgroundMenu.png')
        self.bg = pygame.transform.scale(bg_image,(WIDTH,HEIGHT))
        self.bg_rect = self.bg.get_rect(center = (WIDTH//2,HEIGHT//2))

        # [ Prise de Texte]
        self.UserEnter = True
        self.refresh = 0
        self.onDataBase = True
        self.usernameInput = ''



    def main_menu(self):
        '''
            Cette méthode va nous permettre d'afficher tout le menu du jeu ( PLAY, SCOREBOARD, QUIT )
        '''

        # [ Setup de la musique ]
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load('assets/sound/Music/debug.mp3')
        pygame.mixer.music.play(loops=-1)
        self.music_played='debug'
        
       
        while True:
            
            for event in pygame.event.get(): 
                # un event, regroupe tout les inputs 
                # que l'ordinateur détecte (touches, la position de la souris ou le bouton pour fermer une fenêtre)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # On s'assure que tout s'arrête en fermant la fenêtre
            
            

            # On affiche un fond
            self.screen.blit(self.bg,self.bg_rect)
                

            MENU_MOUSE_POS = pygame.mouse.get_pos() # On récupère la position relative du curseur de la souris

            # On a écrit le titre du jeu puis on l'affiche
            text_surf = self.Menufont.render(str('THE ROGUE'), False, TEXT_COLOR) 
            text_rect = text_surf.get_rect(center= (WIDTH//2,150))
            self.screen.blit(text_surf,text_rect)

            
            # On initialise nos 3 boutons selon la classe bouton tout en bas du scripte Rogue.PY
            PLAY_BUTTON = Button(image= self.newHolder, pos=(WIDTH//2, 300),posImg=15, text_input="PLAY", font=self.font, base_color="#756c6a", hovering_color="White")
            SCORE_BUTTON = Button(image= self.newHolder, pos=(WIDTH//2, 450),posImg=15,
                                text_input="SCORE", font=self.font, base_color="#756c6a", hovering_color="White")
            QUIT_BUTTON = Button(image=self.newHolder, pos=(WIDTH//2, 600), posImg=15,
                                text_input="QUIT", font=self.font, base_color="#756c6a", hovering_color="White")


            for button in [PLAY_BUTTON, SCORE_BUTTON, QUIT_BUTTON]: # On check et actualise les bouton
                
                button.changeColor(MENU_MOUSE_POS) # si on passe dessus la couleur change
                button.update(self.screen)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS): # Si c'est le bouton jeu, on lance une partie
                        if self.level != None: # cette partie là nous permet de reset et pouvoir recommencer en boucle
                            self.level = None

                        else:
                            self.level = Level()
                       
                        self.NameInput() # on demande le nom au joueur
                        self.play() # on lance le jeu

                    if SCORE_BUTTON.checkForInput(MENU_MOUSE_POS): # Le bouton nous permettant d'acceder au scoreboard
                        return self.scoreboard_menu('time') # on lance une nouvelle fenetre ( argument expliqué plus bas)
                    
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS): # le boutton quitter 
                        pygame.quit()
                        sys.exit()
            

            pygame.display.update()


    
    def scoreboard_menu(self, sort):
        '''
            Cette méthode nous permet d'afficher un scoreboard, le lien avec la base de donnée
            sort est un argument de tri
        '''

        # [ Musique différente ]

        if self.music_played!='Score_music':
            pygame.mixer.Sound('assets/sound/SFX/on_tv.mp3').play()
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            pygame.mixer.music.load('assets/sound/Music/Score_music.mp3')
            pygame.mixer.music.play(loops=-1)
            self.music_played='Score_music'



        self.username = '' # Le nom est initialisé à vide
        self.sort = sort # le tri
        while True:
            if self.sort == 'time': # par le chrono
                self.request = self.DBBScripter.getScoreboard()


            if self.sort == 'score': # par le score
                self.request = self.DBBScripter.getScoreboardScore()
         
                
            if self.sort == 'username': # on cherche une personne en particulier
                self.request = self.DBBScripter.getScoreboardUsername(self.username)
            
            pygame.display.update()
            
            # [ BOUTON BIS ]
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get(): 
                # un event, regroupe tout les inputs 
                # que l'ordinateur détecte (touches, la position de la souris ou le bouton pour fermer une fenêtre)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # On s'assure que tout s'arrête en fermant la fenêtre
                if event.type == pygame.KEYDOWN:
                    # Par manque de temps on peut pas 

                    if pygame.key.name(event.key) == 'escape':
                        pygame.mixer.Sound('assets/sound/SFX/click_button.mp3').play()
                        pygame.mixer.Sound('assets/sound/SFX/on_tv.mp3').stop()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load('assets/sound/Music/debug.mp3')
                        pygame.mixer.music.play(loops=-1)
                        self.music_played='debug'
                        return False
        
            self.screen.blit(self.bg,self.bg_rect)
            score_QUIT = Button(image=None, pos=(WIDTH-100, 60),posImg=0 ,
                                text_input="X", font=self.font, base_color="white", hovering_color="red")
            
            # [ Les conditions permets de signifier l'onglet qu'on est ]
            if self.sort == 'time':
                TIME_BUTTON = Button(image=None, pos=(700, 60),posImg=0 ,text_input="CHRONO", font=self.taskfont, base_color="gold", hovering_color="white")
            else:    
                TIME_BUTTON = Button(image=None, pos=(700, 60),posImg=0 ,text_input="CHRONO", font=self.taskfont, base_color="white", hovering_color="red")
            
            if self.sort == 'score':
                SCORE_BUTTON = Button(image=None, pos=(900, 60),posImg=0 ,text_input="SCORE", font=self.taskfont, base_color="gold", hovering_color="white")
            else:    
                SCORE_BUTTON = Button(image=None, pos=(900, 60),posImg=0 ,text_input="SCORE", font=self.taskfont, base_color="white", hovering_color="red")
            
            USER_BUTTON = Button(image=None, pos=(1100, 60),posImg=0 ,
                                text_input="SEARCH", font=self.taskfont, base_color="white", hovering_color="red")


            # affichage de la fenetre de score
            self.scoreWindow()
            self.windowTitle('SCOREBOARD.EXE',75,40)
            self.First()
            self.Second()
            self.Third()
            self.Fourth()
            self.Fifth()

            # [ Activation des boutons]
            for button in [score_QUIT, TIME_BUTTON, SCORE_BUTTON, USER_BUTTON]:
                button.changeColor(pygame.mouse.get_pos())
                button.update(self.screen)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if TIME_BUTTON.checkForInput(mouse_pos):
                        
                        pygame.mixer.Sound('assets/sound/SFX/click_button.mp3').play()
                        return self.scoreboard_menu('time')
                    
                    if SCORE_BUTTON.checkForInput(mouse_pos):
                       
                        pygame.mixer.Sound('assets/sound/SFX/click_button.mp3').play()
                        return self.scoreboard_menu('score')

                    if USER_BUTTON.checkForInput(mouse_pos):
                        pygame.mixer.Sound('assets/sound/SFX/click_button.mp3').play()
                        sort = 'username'
                        self.username = self.nameInputScore()
                        return self.searchUserScoreBoard(self.username)
                        
                    
                    if score_QUIT.checkForInput(mouse_pos):
                        pygame.mixer.Sound('assets/sound/SFX/click_button.mp3').play()
                        pygame.mixer.Sound('assets/sound/SFX/on_tv.mp3').stop()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        pygame.mixer.music.load('assets/sound/Music/debug.mp3')
                        pygame.mixer.music.play(loops=-1)
                        self.music_played='debug'
                        return self.main_menu()
                        
            pygame.display.update()

    def searchUserScoreBoard(self, username = ''):
        '''
            Onglet de recherche d'un joueur, cette méthode est appelé avec le complément d'une autre fonction pour de la prise de texte

            Bon pour tout ce qui est Probleme des injections et des bugs présents mais dont je trouve pas la solution au problème le systeme il marche mais
            ça marche dans une certaine mesure

        '''


        self.username = username # on s'enfiche si le pseudonyme est fini ou non. Si le nom est inexistant ou mal ecrit, un petit message d'erreur a été concocté 
        self.sort = 'username'
        while True:
            
            self.request = self.DBBScripter.getScoreboardUsername(self.username) 
            # on lance la premiere requete pour trouver le joueur qu'on cherche
            
            pygame.display.update()

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get(): 
                # un event, regroupe tout les inputs 
                # que l'ordinateur détecte (touches, la position de la souris ou le bouton pour fermer une fenêtre)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # On s'assure que tout s'arrête en fermant la fenêtre
                if event.type == pygame.KEYDOWN:
                    # Par manque de temps on peut pas 

                    if pygame.key.name(event.key) == 'escape':
                        return 
        
            self.screen.blit(self.bg,self.bg_rect)
            score_QUIT = Button(image=None, pos=(WIDTH-100, 60),posImg=0 ,
                                text_input="X", font=self.font, base_color="white", hovering_color="red")
            if self.sort == 'time':
                TIME_BUTTON = Button(image=None, pos=(700, 60),posImg=0 ,text_input="CHRONO", font=self.taskfont, base_color="gold", hovering_color="white")
            else:    
                TIME_BUTTON = Button(image=None, pos=(700, 60),posImg=0 ,text_input="CHRONO", font=self.taskfont, base_color="white", hovering_color="red")
            
            if self.sort == 'score':
                SCORE_BUTTON = Button(image=None, pos=(900, 60),posImg=0 ,text_input="SCORE", font=self.taskfont, base_color="gold", hovering_color="white")
            else:    
                SCORE_BUTTON = Button(image=None, pos=(900, 60),posImg=0 ,text_input="SCORE", font=self.taskfont, base_color="white", hovering_color="red")
            if self.sort == 'username':
                USER_BUTTON = Button(image=None, pos=(1100, 60),posImg=0 ,text_input="SEARCH", font=self.taskfont, base_color="blue", hovering_color="red")
            else:    
                USER_BUTTON = Button(image=None, pos=(1100, 60),posImg=0 ,text_input="SEARCH", font=self.taskfont, base_color="white", hovering_color="red")

            self.scoreWindow()
            self.windowTitle('SCOREBOARD.EXE',75,40)
            self.UserCard() # On affiche le joueur qu'on vient de chercher
            

            for button in [score_QUIT, TIME_BUTTON, SCORE_BUTTON, USER_BUTTON]:
                button.changeColor(pygame.mouse.get_pos())
                button.update(self.screen)
                
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:

                    if TIME_BUTTON.checkForInput(mouse_pos):
                        pygame.mixer.Sound('assets/sound/SFX/click_button.mp3').play()
                        return self.scoreboard_menu('time')
                    
                    if SCORE_BUTTON.checkForInput(mouse_pos):
                        pygame.mixer.Sound('assets/sound/SFX/click_button.mp3').play()
                        return self.scoreboard_menu('score')

                    if USER_BUTTON.checkForInput(mouse_pos):
                        pygame.mixer.Sound('assets/sound/SFX/click_button.mp3').play()
                        self.username = self.nameInputScore()
                        return self.searchUserScoreBoard(self.username)
                        
                    
                    if score_QUIT.checkForInput(mouse_pos):
                        pygame.mixer.Sound('assets/sound/SFX/click_button.mp3').play()
                        pygame.mixer.Sound('assets/sound/SFX/on_tv.mp3').stop()
                        pygame.mixer.music.stop()
                        pygame.mixer.music.unload()
                        return self.main_menu()
                        
            
            
            pygame.display.update()

            
    def nameInputScore(self):
        classFont = pygame.font.Font(MENU2_FONT, 50)
        usernameInput = ''
        pygame.display.update()

        while True:

            for event in pygame.event.get():
                    
                if event.type == pygame.KEYDOWN:
                    # Par manque de temps on peut pas 

                    if pygame.key.name(event.key) == 'escape' or pygame.key.name(event.key) == 'return':
                        return usernameInput.lower()
                    
                    
                    elif pygame.key.name(event.key) == 'backspace' and len(usernameInput) > 0:
                        usernameInput = usernameInput.rstrip(usernameInput[-1])
                    
                    elif  len(usernameInput) <= 10:
                        if not pygame.key.name(event.key) == 'backspace' \
                            or not pygame.key.name(event.key) == 'return':
                            usernameInput += event.unicode


                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # On s'assure que tout s'arrête en fermant la fenêtre
            
            bg_rect = pygame.Rect(WIDTH//4,HEIGHT//4,WIDTH//2,HEIGHT//2) 
            pygame.draw.rect(self.display_surface,'black',bg_rect)
            pygame.draw.rect(self.display_surface,'white',bg_rect,3) 
            text_surf = classFont.render('Chercher une gravure de Legende :', False, 'white')
            text_rect = text_surf.get_rect(center=((WIDTH//2,HEIGHT//2-100)))
            self.display_surface.blit(text_surf,text_rect)

            self.displayText2(usernameInput)
            pygame.display.update()
        
# [ PUREMENT AFFICHAGE DE FENETRE ]
    def scoreWindow(self):
        bg_rect = pygame.Rect(50,20,WIDTH-100,HEIGHT-30) # On dessine le carré du fond
        pygame.draw.rect(self.display_surface,'black',bg_rect)
        pygame.draw.rect(self.display_surface,'white',bg_rect,3) # sinon celle de base
    
    def windowTitle(self, text, x,y):
        font = pygame.font.Font(MENU_FONT, 30)
        text_surf = font.render(str(text), False, 'white')
        text_rect = text_surf.get_rect(topleft=((x,y)))
        self.display_surface.blit(text_surf,text_rect)
    

    # [ Les affichages de cartes] 

    # les fonctions suivantes suivent le même principe, 
    # si on a une requête on va la décomposer pour afficher individuellement chaque donnée
    # UserCard sera affiché dans l'onglet SearchUser

    # le reste c'est le classement, la simple requete de temps ou de score diffère

    def UserCard(self):
        classFont = pygame.font.Font(MENU_FONT, 50)
        font = pygame.font.Font(MENU2_FONT, 40)
        
        bg_rect = pygame.Rect(55,120,WIDTH-110,110) # On dessine le carré du fond
        pygame.draw.rect(self.display_surface,'black',bg_rect)
        pygame.draw.rect(self.display_surface,'white',bg_rect,3) # sinon celle de base

        if self.request == "Aucune légende a ce nom...":
            username = 'User_Not_Found'
            time = '--: --. --'
            score = '----'
            date = 'Date_Not_Found'

            text_surf = font.render(username, False, 'white')
            text_rect = text_surf.get_rect(topleft=((150,150)))
            self.display_surface.blit(text_surf,text_rect)

            text_surf = font.render(time, False, 'white')
            text_rect = text_surf.get_rect(topleft=((700,150)))
            self.display_surface.blit(text_surf,text_rect)

            text_surf = font.render(str(score), False, 'white')
            text_rect = text_surf.get_rect(topleft=((900,150)))
            self.display_surface.blit(text_surf,text_rect)

            text_surf = font.render(str(date), False, 'white')
            text_rect = text_surf.get_rect(topleft=((1080,150)))
            self.display_surface.blit(text_surf,text_rect)
            
       
        elif len(self.request) >= 1:
            place, attribut = self.request
            text_surf = classFont.render(str(place), False, 'gold')
            text_rect = text_surf.get_rect(topleft=((80,130)))
            self.display_surface.blit(text_surf,text_rect)
                
        
            username = attribut[0]
            time = attribut[1]
            score = attribut[2]
            date = attribut[3]
       
            text_surf = font.render(username, False, 'white')
            text_rect = text_surf.get_rect(topleft=((150,150)))
            self.display_surface.blit(text_surf,text_rect)

            text_surf = font.render(time, False, 'white')
            text_rect = text_surf.get_rect(topleft=((700,150)))
            self.display_surface.blit(text_surf,text_rect)

            text_surf = font.render(str(score), False, 'white')
            text_rect = text_surf.get_rect(topleft=((900,150)))
            self.display_surface.blit(text_surf,text_rect)

            text_surf = font.render(str(date), False, 'white')
            text_rect = text_surf.get_rect(topleft=((1080,150)))
            self.display_surface.blit(text_surf,text_rect)
            
    def First(self):
        bg_rect = pygame.Rect(55,120,WIDTH-110,110) # On dessine le carré du fond
        pygame.draw.rect(self.display_surface,'black',bg_rect)
        pygame.draw.rect(self.display_surface,'white',bg_rect,3) # sinon celle de base

        classFont = pygame.font.Font(MENU_FONT, 50)
        font = pygame.font.Font(MENU2_FONT, 40)
        text_surf = classFont.render('1', False, 'gold')
        text_rect = text_surf.get_rect(topleft=((80,130)))
        self.display_surface.blit(text_surf,text_rect)

        if len(self.request) >0 :
            attr = self.request[0]
     
            username = attr[0]
            time = attr[1]
            score = attr[2]
            date = attr[3]
        else:
            username = 'User_Not_Found'
            time = '--: --. --'
            score = '----'
            date = 'Date_Not_Found'
       
        text_surf = font.render(username, False, 'white')
        text_rect = text_surf.get_rect(topleft=((150,150)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(time, False, 'white')
        text_rect = text_surf.get_rect(topleft=((700,150)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(score), False, 'white')
        text_rect = text_surf.get_rect(topleft=((900,150)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(date), False, 'white')
        text_rect = text_surf.get_rect(topleft=((1080,150)))
        self.display_surface.blit(text_surf,text_rect)

    def Second(self):
        bg_rect = pygame.Rect(55,235,WIDTH-110,110) # On dessine le carré du fond
        pygame.draw.rect(self.display_surface,'black',bg_rect)
        pygame.draw.rect(self.display_surface,'white',bg_rect,3) # sinon celle de base

        classFont = pygame.font.Font(MENU_FONT, 50)
        font = pygame.font.Font(MENU2_FONT, 40)
        text_surf = classFont.render('2', False, (209, 220, 237))
        text_rect = text_surf.get_rect(topleft=((80,245)))
        self.display_surface.blit(text_surf,text_rect)


      
        if len(self.request) > 1:
  
            attr = self.request[1]
            username = attr[0]
            time = attr[1]
            score = attr[2]
            date = attr[3]
        else:
            username = 'User_Not_Found'
            time = '--: --. --'
            score = '----'
            date = 'Date_Not_Found'
       
        text_surf = font.render(username, False, 'white')
        text_rect = text_surf.get_rect(topleft=((150,265)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(time, False, 'white')
        text_rect = text_surf.get_rect(topleft=((700,265)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(score), False, 'white')
        text_rect = text_surf.get_rect(topleft=((900,265)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(date), False, 'white')
        text_rect = text_surf.get_rect(topleft=((1080,265)))
        self.display_surface.blit(text_surf,text_rect)

    def Third(self):
        bg_rect = pygame.Rect(55,350,WIDTH-110,110) # On dessine le carré du fond
        pygame.draw.rect(self.display_surface,'black',bg_rect)
        pygame.draw.rect(self.display_surface,'white',bg_rect,3) # sinon celle de base

        classFont = pygame.font.Font(MENU_FONT, 50)
        font = pygame.font.Font(MENU2_FONT, 40)
        text_surf = classFont.render('3', False, (205, 127, 50))
        text_rect = text_surf.get_rect(topleft=((80,360)))
        self.display_surface.blit(text_surf,text_rect)

   
        if len(self.request) >2:
            attr = self.request[2]
      
            username = attr[0]
            time = attr[1]
            score = attr[2]
            date = attr[3]
        else:
            username = 'User_Not_Found'
            time = '--: --. --'
            score = '----'
            date = 'Date_Not_Found'
       
        text_surf = font.render(username, False, 'white')
        text_rect = text_surf.get_rect(topleft=((150,380)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(time, False, 'white')
        text_rect = text_surf.get_rect(topleft=((700,380)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(score), False, 'white')
        text_rect = text_surf.get_rect(topleft=((900,380)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(date), False, 'white')
        text_rect = text_surf.get_rect(topleft=((1080,380)))
        self.display_surface.blit(text_surf,text_rect)

    def Fourth(self):
        bg_rect = pygame.Rect(55,465,WIDTH-110,110) # On dessine le carré du fond
        pygame.draw.rect(self.display_surface,'black',bg_rect)
        pygame.draw.rect(self.display_surface,'white',bg_rect,3) # sinon celle de base

        classFont = pygame.font.Font(MENU_FONT, 50)
        font = pygame.font.Font(MENU2_FONT, 40)
        text_surf = classFont.render('4', False, 'white')
        text_rect = text_surf.get_rect(topleft=((80,475)))
        self.display_surface.blit(text_surf,text_rect)

      
        if len(self.request) >3:
            attr = self.request[3]

            username = attr[0]
            time = attr[1]
            score = attr[2]
            date = attr[3]
        else:
            username = 'User_Not_Found'
            time = '--: --. --'
            score = '----'
            date = 'Date_Not_Found'
       
        text_surf = font.render(username, False, 'white')
        text_rect = text_surf.get_rect(topleft=((150,495)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(time, False, 'white')
        text_rect = text_surf.get_rect(topleft=((700,495)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(score), False, 'white')
        text_rect = text_surf.get_rect(topleft=((900,495)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(date), False, 'white')
        text_rect = text_surf.get_rect(topleft=((1080,495)))
        self.display_surface.blit(text_surf,text_rect)

    def Fifth(self):
        bg_rect = pygame.Rect(55,580,WIDTH-110,110) # On dessine le carré du fond
        pygame.draw.rect(self.display_surface,'black',bg_rect)
        pygame.draw.rect(self.display_surface,'white',bg_rect,3) # sinon celle de base

        classFont = pygame.font.Font(MENU_FONT, 50)
        font = pygame.font.Font(MENU2_FONT, 40)
        text_surf = classFont.render('5', False, 'white')
        text_rect = text_surf.get_rect(topleft=((80,590)))
        self.display_surface.blit(text_surf,text_rect)

      
        if len(self.request) > 4:
            attr = self.request[4]
      
            username = attr[0]
            time = attr[1]
            score = attr[2]
            date = attr[3]
        else:
            username = 'User_Not_Found'
            time = '--: --. --'
            score = '----'
            date = 'Date_Not_Found'
       
        text_surf = font.render(username, False, 'white')
        text_rect = text_surf.get_rect(topleft=((150,610)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(time, False, 'white')
        text_rect = text_surf.get_rect(topleft=((700,610)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(score), False, 'white')
        text_rect = text_surf.get_rect(topleft=((900,610)))
        self.display_surface.blit(text_surf,text_rect)

        text_surf = font.render(str(date), False, 'white')
        text_rect = text_surf.get_rect(topleft=((1080,610)))
        self.display_surface.blit(text_surf,text_rect)


    def NameInput(self):
        self.usernameInput = ''
        pygame.display.update()

        alreadyUsed = self.DBBScripter.onlyUser()
    

        while True:

            for event in pygame.event.get():
                    
                if event.type == pygame.KEYDOWN:
                    # Par manque de temps on peut pas 

                    if pygame.key.name(event.key) == 'escape' or pygame.key.name(event.key) == 'return' and self.usernameInput not in alreadyUsed:
                        return False
                    
                    
                    elif pygame.key.name(event.key) == 'backspace' and len(self.usernameInput) != 0:
                        self.usernameInput = self.usernameInput.rstrip(self.usernameInput[-1])
                    
                    elif  len(self.usernameInput) <= 10:
                        if not pygame.key.name(event.key) == 'backspace' \
                            or not pygame.key.name(event.key) == 'return':
                            self.usernameInput += event.unicode

                    

                    
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # On s'assure que tout s'arrête en fermant la fenêtre
            
            self.screen.fill('white')
            self.ui.GloryComment("QUEL     NOM     GRAVEREZ    -    VOUS     DANS     L    '    HISTOIRE     ?", WIDTH//2, HEIGHT//2-200)
            self.displayText(self.usernameInput)
            pygame.display.update()


    def displayText(self, text):
        font = pygame.font.Font(MENU_FONT, 150)
        text_surf = font.render(str(text), False, UI_BG_COLOR)
        text_rect = text_surf.get_rect(center=(WIDTH//2,HEIGHT//2))
     
        # affichage du texte
        self.screen.blit(text_surf,text_rect)
    
    def displayText2(self, text):
        font = pygame.font.Font(MENU_FONT, 40)
        text_surf = font.render(str(text), False, 'white')
        text_rect = text_surf.get_rect(center=(WIDTH//2,HEIGHT//2))
     
        # affichage du texte
        self.screen.blit(text_surf,text_rect)

    def play(self):
        
        while True:

            pygame.display.update()
            for event in pygame.event.get(): 
                # un event, regroupe tout les inputs 
                # que l'ordinateur détecte (touches, la position de la souris ou le bouton pour fermer une fenêtre)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit() # On s'assure que tout s'arrête en fermant la fenêtre
                if event.type == pygame.KEYDOWN:
                    # Par manque de temps on peut pas 

                    
                    if self.level.win or self.level.lose and event.type == pygame.KEYDOWN:
                        if (pygame.key.name(event.key) == 'escape' or pygame.key.name(event.key) == 'return'):
    

                            self.level = None
                            return False
                
            
        
        

            if self.level.win:

                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('assets/sound/Music/Title.mp3')
                pygame.mixer.music.play(loops=-1)

                self.screen.fill((252, 251, 247))

                if self.onDataBase:
                    self.onDataBase = False
                    self.DBBScripter.newUser(self.usernameInput.lower(), self.level.Chronometre.PureTime(), self.level.tempsTotal, self.level.playerScore)
            
            if self.level.lose:
                pygame.mixer.music.stop()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('assets/sound/Music/Title.mp3')
                pygame.mixer.music.play(loops=-1)

                self.screen.fill((194, 54, 54))

                
            

            #self.DBBScripter.getScoreboard()

            self.level.run() # on lance la méthode de classe Level
            pygame.display.update() # on update chaque l'écran dans sa totalité
            self.clock.tick(FPS) # On raffraîchit la fenêtre un nombre tick de fois. Dans notre cas FPS = 120
            
            # Anecdote :
            # Même si un jeu tourne a une frequence plus haute que ce que l'on peut afficher, avoir un haut taux
            # permet d'être plus précis lorsqu'on exécute des touches, puisque le temps de détection est plus court.



    def run(self):  # cette méthode va lancer le jeu
        self.main_menu()


class Button():
    '''
        la classe bouton 
    '''
    def __init__(self, image, pos, posImg, text_input, font, base_color, hovering_color):
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.y_pos2 = self.y_pos - posImg # l'offsett d'une image pour plus d'esthétisme
        self.font = font
            
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos2))

    def update(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            return True
        return False

    def changeColor(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)


game = Game()
game.run()
