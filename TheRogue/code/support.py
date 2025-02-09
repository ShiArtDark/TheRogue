from os import walk
import pygame


def import_folder(path):
    '''
        prends en argument une chaine de charactère d'un parcours dans le gestionnaire de fichier
    '''
    surfaceList = []
    for _,__,img_files in walk(path): # Le parcours dans le gestionnaire
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha() # on charge une image
            surfaceList += [image_surf] # on l'ajoute dans une liste
    
    return surfaceList