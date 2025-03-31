
import datetime
import sqlite3

class DataBase:
    def __init__(self):
        self.connexion = sqlite3.connect("baseDeDonnee.db")

        count = self.connexion.execute("SELECT count(*) FROM user")
        self.countList = list(count)[0][0] # On recupere le nombre d'id entrée (on peut s'y fier à 100% on ne supprimera aucun id)
        
    
    def newUser(self,username, time , chrono, score):
        '''
            enregistre une nouvelle légende dans le marbre, 
            on entre son nom, son temps de complétion pur, son chronomètre ainsi que son score
        '''
        
        #On initialisera une table avec un id mis automatiquement
        self.connexion.execute("INSERT INTO user \
                  (username, temps) VALUES \
                  ('"+username+"', "+str(time)+")")
    
        self.connexion.commit()
        
        self.connexion.execute("INSERT INTO scoreboard \
                               (id, chrono, score, date) VALUES \
                               ('"+str(self.getId(username))+"','"+chrono+"', "+str(score)+", +'"+str(datetime.datetime.now()).split('.')[0]+"')")
        
         
        self.connexion.commit()

    def getId(self, username): # on recupere le nom par son nom
        '''
            on récupère l'id du'un joueur déjà enregistré
        '''

        search = self.connexion.execute("SELECT id FROM user \
                       WHERE username='"+username+"'")
        searchList = list(search)

        id = searchList[0][0]

        return id
    

    def getUserTable(self): # On décide de pas prendre le temps puisqu'on en aura pas besoin
        '''
            cette méthode nous permet de récupérer tout les joueurs qui gravé leurs nom dans le marbre
            on récupère un dictionnaire de pseudo associé à leur id respectif
        '''
        user = {}
        search = self.connexion.execute("SELECT id, username FROM user ")
        searchList = list(search)
        
        
        for i in range(self.countList):
            id, username = searchList[i]
            user[i+1]= {'username' : username}

        
        return user
    
    def onlyUser(self):
        '''
            reprend le meme principe que getusertab mais uniquement pour les pseudonyme
        '''
        username = []
        for i in range(self.countList):
            username += [self.getUserTable()[i+1]['username']]
        
        return username
    


    def getScoreboard(self):
        '''
            renvoie une liste de joueurs classé selon leur temps
        '''
        search = self.connexion.execute("SELECT user.username, chrono, score, date FROM scoreboard \
                                JOIN user ON user.id = scoreboard.id  \
                                ORDER BY user.temps ASC")
        
        searchList = list(search)
        return searchList
    
    def getScoreboardScore(self):
        '''
            renvoie une liste de joueur classé selon leur score
        '''
        search = self.connexion.execute("SELECT user.username, chrono, score, date FROM scoreboard \
                                JOIN user ON user.id = scoreboard.id  \
                                ORDER BY score DESC")
        
        searchList = list(search)
        return searchList
    
    
    def getScoreboardUsername(self, username):
        '''
            fait la recherche d'un joueur en particulier et renvoie son classement par rapport au temps
        '''
        search = self.connexion.execute("SELECT user.username, chrono, score, date FROM scoreboard \
                                JOIN user ON user.id = scoreboard.id  \
                                WHERE user.username LIKE '"+username+"%'")
        
        searchList = list(search)
        if searchList != []:
            DataUsername = self.onlyUser()

            for user in DataUsername:
                
                if username in user:
                    name = searchList[0][0]
                    

                    request = self.getRank()
                    
                    for i in range(len(request)-1):

                        place, attribut = request[i]
                    
                        if name == request[i][1][0]:
                            
                            return (i+1,attribut)
                
            return "Aucune légende a ce nom..."
        else:
            return "Aucune légende a ce nom..."


    def getCount(self): 
        '''
            recupère le nombre de ligne enregistré dans notre table scoreboard et user
        '''
        search = self.connexion.execute("SELECT Count(*) FROM scoreboard")
        searchList = list(search)
        return searchList[0][0]
    
    def getRank(self):
        '''
            récupère le rang associé au temps
        '''
        ranking = self.getScoreboard()
        ranks = []

        for index, i in enumerate(ranking, 1):
            ranks += [(index, i)]
        
        return ranks
