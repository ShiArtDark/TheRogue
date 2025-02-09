import time
INTERVALLE = 60
class Chrono:
    def __init__(self): 
        self.totalEcoule = None
        self.startTime = time.time() # Prends le temps à l'initialisation
        self.OneTime = True

    def ChronoUpdate(self,hasFirtMoved):
        '''
            Cette fonction prend en argument un booléen et actualise la chronomètre
        '''
        if hasFirtMoved and self.OneTime:
            self.startTime = time.time() # Prends le temps à l'initialisation
            self.OneTime = False # Pour éviter de reset constamment

        elif hasFirtMoved:
            current = time.time() # Actualisation en temps réel
            self.totalEcoule = current - self.startTime # On fait la différence entre le temps initialisé et l'actuelle
            self.secondeEcoule = int(self.totalEcoule) # On récupère uniquement les secondes entières

            self.ms = str(self.totalEcoule).split('.')[1]
            # La fonction split() va renvoyer une liste avec les éléments présents avant et après un séparateur,
            # sachant que l'index [0], corresspond au nombre purement entier, nous on cherche à prendre uniquement les décimales
            
            self.millisecondes = str(self.ms)[0:2] # on les coupera par tronchature jusqu'au centième


            # [ PUREMENT ESTHETIQUE ]
            # Pour garder le même espacement du chrono sur l'écran, on 'remplit' les slots vides

            # [ Principe ]
            # On souhaite afficher uniquement les secondes donc on fait le module pour récupérer uniquement le reste de seconde hors minutes
            # A l'inverse, On fait la division Euclidienne pour avoir le nombre de minute

            # Cas 1, si la minute et la seconde sont des chiffres, on complète la dizaine
            if len( str( self.secondeEcoule // INTERVALLE))<2 and len(str(self.secondeEcoule% INTERVALLE )) <2 :
                return '0'+str(self.secondeEcoule//INTERVALLE)+': '+'0'+str(self.secondeEcoule% INTERVALLE )+'. '+self.millisecondes
            
            # Cas 2, si uniquement la seconde est un chiffre
            elif len( str(self.secondeEcoule%INTERVALLE)) <2:
                return str(self.secondeEcoule//INTERVALLE)+': '+'0'+str(self.secondeEcoule% INTERVALLE )+'. '+self.millisecondes
            
            # Cas 3, si uniquement la minute est un chiffre
            elif len( str( self.secondeEcoule // INTERVALLE )) <2:
                return '0'+str(self.secondeEcoule// INTERVALLE )+': '+str(self.secondeEcoule% INTERVALLE )+'. '+self.millisecondes
        else:
            return '00: 00. 00'

    def Timer_get(self, hasFirstMoved):
        '''
            cette fontion prend en argument un booléen, et renvoie la version textuel du temps passé
        '''

        if hasFirstMoved:
            total = self.totalEcoule

            self.secondeEcoule = int(total)
            self.ms = str(total).split('.')[1]   
            self.millisecondes = str(self.ms)[0:2]

            
            if len( str( self.secondeEcoule // INTERVALLE))<2 and len(str(self.secondeEcoule% INTERVALLE )) <2 :
                return '0'+str(self.secondeEcoule//INTERVALLE)+': '+'0'+str(self.secondeEcoule% INTERVALLE )+'. '+self.millisecondes
            
            # Cas 2, si uniquement la seconde est un chiffre
            elif len( str(self.secondeEcoule%INTERVALLE)) <2:
                return str(self.secondeEcoule//INTERVALLE)+': '+'0'+str(self.secondeEcoule% INTERVALLE )+'. '+self.millisecondes
            
            # Cas 3, si uniquement la minute est un chiffre
            elif len( str( self.secondeEcoule // INTERVALLE )) <2:
                return '0'+str(self.secondeEcoule// INTERVALLE )+': '+str(self.secondeEcoule% INTERVALLE )+'. '+self.millisecondes
        
        else:
            return '00: 00. 00'
        
    def PureTime(self):
        '''
            cette fonction prend aucun argument et renvoie le temps brut du temps passé à 10**-2 seconde
        '''
        total = self.totalEcoule
        seconde =str(int(total))
        bloc = seconde+'.'+str(str(total).split('.')[1])[0:2]
        return float(bloc)