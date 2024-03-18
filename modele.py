import random
from copy import deepcopy

LES_FORMES:list = [[(0,0),(0,-1),(0,1),(0,2)], [(0,0),(0,1),(1,1),(1,0)], [(0,0),(1,0),(0,1),(-1,1)], [(0,0),(-1,0),(0,1),(1,1)], [(-1,1),(-1,0),(0,0),(1,0)], [(0,0),(-1,0),(1,0),(1,1)], [(0,0),(-1,0),(1,0),(0,-1)]]

class ModeleTetris:
    def __init__(self, lignes:int=18, colonnes:int=13):
        """
        ModeleTetris, int, int -> NoneType
        Constructeur de la classe ModeleTetris
        """
        self.__base:int = 4
        self.__score:int = 0
        self.__haut:int = lignes + self.__base
        self.__larg:int = colonnes
        self.__terrain:list = [[-1 for _ in range(self.__larg)] for _ in range(self.__haut)]
        for i in range(4):
            self.__terrain[i] = [-2 for _ in range(self.__larg)]
        self.__forme:Forme = Forme(self)
        self.__suivante:Forme = Forme(self)
        return
        
    def get_hauteur(self):
        """
        ModeleTetris -> int
        Retourne la hauteur du terrain
        """
        return self.__haut
    
    def get_largeur(self):
        """
        ModeleTetris -> int
        Retourne la largeur du terrain
        """
        return self.__larg
    
    def get_valeur(self, ligne, colonne):
        """
        ModeleTetris, int, int -> int
        Retourne la valeur qu'il y a à aux coordonnées colonne ligne 
        """
        return self.__terrain[ligne][colonne]
    
    def est_occupe(self, ligne, colonne):
        """
        ModeleTetris, int, int -> bool
        Vérifie si l'emplacement aux coordonnées colonne ligne est occupé (c'est-à-dire que la valeur est plus grande ou égal à 0)
        """
        if ligne >= self.__haut or ligne < 0 or colonne >= self.__larg or colonne < 0:
            return True
        return self.__terrain[ligne][colonne] >= 0
    
    def fini(self):
        """
        ModeleTetris -> bool
        Vérifie si la partie est fini ou pas
        """
        for colonne in range(self.__larg):
            if self.__terrain[self.__base-1][colonne] != -2:
                return True
        return False
    
    def ajoute_forme(self):
        """
        ModeleTetris -> NoneType
        Ajoute la forme au terrain
        """
        for y, x in self.__forme.get_coords():
            self.__terrain[y][x] = self.__forme.get_couleur()
        return

    def forme_tombe(self):
        """
        ModeleTetris -> bool
        Essaie de faire tomber la forme, si elle n'y arrive pas, alors l'ancienne forme sera ajoutée au terrain et une nouvelle sera créée
        """
        if self.__forme.tombe():
            self.ajoute_forme()
            self.supprimes_lignes_completes()
            self.__forme = self.__suivante
            self.__suivante = Forme(self)
            return True
        return False

    def get_couleur_forme(self):
        """
        ModeleTetris -> int
        Retourne la couleur de la forme
        """
        return self.__forme.get_couleur()

    def get_coords_forme(self):
        """
        ModeleTetris -> list(tuple(int, int))
        Retourne les coordonnées de la forme
        """
        return self.__forme.get_coords()

    def forme_a_gauche(self):
        """
        ModeleTetris -> NoneType
        Fait déplacer la forme à gauche
        
        """
        self.__forme.a_gauche()
        return
    
    def forme_a_droite(self):
        """
        ModeleTetris -> NoneType
        Fait déplacer la forme à droite
        """
        self.__forme.a_droite()
        return
    
    def forme_tourne(self):
        """
        ModeleTetris -> NoneType
        Fait une rotation de la forme
        """
        self.__forme.tourne()
        return
    
    def est_ligne_complete(self, lig:int):
        """
        ModeleTetris, int -> bool
        Teste si la ligne lig du terrain est complète
        """
        for elem in self.__terrain[lig]:
            if elem < 0:
                return False
        return True
    
    def supprime_ligne(self, lig:int):
        """
        ModeleTetris, int -> NoneType
        Supprime la ligne d'indice lig sur le terrain, toutes les valeurs des lignes de self.__base à lig-1 inclus descendent d'un cran
        """
        nouvelleL:list = [[-2 for _ in range(self.__larg)] for _ in range(self.__base)]
        nouvelleL.append([-1 for _ in range(self.__larg)])
        for i in range(4, lig):
            nouvelleL.append(self.__terrain[i])
        for j in range(lig+1, self.__haut):
            nouvelleL.append(self.__terrain[j])
        self.__terrain = deepcopy(nouvelleL)
        return

    def supprimes_lignes_completes(self):
        """
        ModeleTetris -> NoneType
        Supprime toutes les lignes complètes, et pour chaque lignes complètes supprimées, augmente le score de 1
        """
        for i in range(4, self.__haut):
            if self.est_ligne_complete(i):
                self.supprime_ligne(i)
                self.__score += 1
        return
    
    def get_score(self):
        """
        ModeleTetris -> int
        Retourne la valeur du score
        """
        return self.__score
    
    def get_coords_suivante(self):
        """
        ModeleTetris -> list
        Retourne les coordonnées relatives de __suivante
        """
        return self.__suivante.get_coords_relative()
    
    def get_couleur_suivante(self):
        """
        ModeleTetris -> int
        Retourne la couleur de __suivante
        """
        return self.__suivante.get_couleur()
    
    def reinitialise(self):
        """
        ModeleTetris -> NoneType
        Réinitialise le terrain et ses formes
        """
        self.__terrain:list = [[-1 for _ in range(self.__larg)] for _ in range(self.__haut)]
        for i in range(4):
            self.__terrain[i] = [-2 for _ in range(self.__larg)]
        self.__forme:Forme = Forme(self)
        self.__suivante:Forme = Forme(self)
        return

class Forme:
    def __init__(self, modele):
        """
        Forme -> NoneType
        Constructeur de la classe Forme
        """
        self.__modele:ModeleTetris = modele
        self.__couleur:int = random.randint(0, len(LES_FORMES)-1)
        self.__forme:list = LES_FORMES[self.__couleur]
        self.__y0:int = 2
        self.__x0:int = random.randint(1,self.__modele.get_largeur()-2) 
        return
        
    def get_couleur(self):
        """
        Forme -> int
        Retourne la couleur de la forme
        """
        return self.__couleur
    
    def get_coords(self):
        """
        Forme -> list(tuple(int,int))
        Retourne les coordonnées de la forme
        """
        coords = [(self.__y0 + y, self.__x0 + x) for x, y in self.__forme]
        return coords
    
    def collision(self):
        """
        Forme -> bool
        Teste s'il y a une collision en dessous de la forme
        """
        x:int = 0
        y:int = 0
        for i, j in self.__forme:
            x = self.__x0 + i
            y = self.__y0 + j
            if self.__modele.est_occupe(y+1, x):
                return True
        return False
    
    def tombe(self):
        """
        Forme -> bool
        Fais tomber la forme s'il n'y a pas de collision en dessous de celle-ci, retourne True si elle ne peut plus tomber, False sinon
        """
        if not self.collision():
            self.__y0 += 1
            return False
        else:
            return True
        
    def position_valide(self, coords:tuple):
        """
        Forme -> bool
        Vérifie si la prochaine position de la forme est valide
        """
        y, x = coords
        return not self.__modele.est_occupe(y, x)
    
    def a_gauche(self):
        """
        Forme -> bool
        Vérifie si la prochaine position à gauche de la forme est valide
        """
        coords:list = self.get_coords()
        for y,x in coords:
            if not self.position_valide((y, x-1)):
                return
        self.__x0 -= 1
        return
    
    def a_droite(self):
        """
        Forme -> bool
        Vérifie si la prochaine position à droite de la forme est valide
        """
        coords:list = self.get_coords()
        for y,x in coords:
            if not self.position_valide((y, x+1)):
                return
        self.__x0 += 1
        return
    
    def tourne(self):
        """
        Forme -> NoneType
        Fait tourner la forme, si la position n'est pas valide, remet la forme à l'orientation d'avant
        """
        forme_prec:list = self.__forme.copy()
        self.__forme = [(-y, x) for x, y in self.__forme]
        coords:list = self.get_coords()
        for coord in coords:
            if not self.position_valide(coord):  
                self.__forme = forme_prec
                break
        return
    
    def get_coords_relative(self):
        """
        Forme -> list
        Retourne une copie de la liste des coordonnées relatives de la forme
        """
        return deepcopy(self.__forme)