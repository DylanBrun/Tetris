import tkinter as tk
import modele
import vue
import time
import pygame

class Controleur:
    def __init__(self, tetris):
        """
        Controleur -> NoneType
        Constructeur de la classe Controleur
        """
        self.__tetris:modele.ModeleTetris = tetris
        self.__vue:vue.VueTetris = vue.VueTetris(tetris)
        self.__fen:vue.tk.Tk = self.__vue.fenetre()
        self.__fen.bind("<Key-Left>", self.forme_a_gauche)
        self.__fen.bind("<Key-Right>", self.forme_a_droite)
        self.__fen.bind("<Key-Down>", self.forme_tombe)
        self.__fen.bind("<Key-Up>", self.forme_tourne)
        self.__fen.bind("<space>", self.forme_tombe_instant)
        self.__fen.bind("<Escape>", self.pause_event)
        self.__delai:int = 210
        self.__delai_backup:int = self.__delai
        self.__valeur_choix:int = 0
        self.pause_:int = 0
        self.__manager:dict = {0:("Commencer", self.lance_partie), 1:("Pause", self.pause), 2:("Reprendre", self.reprendre), 3:("Recommencer", self.recommencer)}
        self.change_bouton_mode()
        pygame.mixer.init()
        self.__fen.mainloop()
        return
            
    def joue(self):
        """
        Controleur -> NoneType
        Commence et fini la partie de Tetris
        """
        if not self.__tetris.fini():
            if not self.pause_:
                self.affichage()
                self.__vue.fenetre().after(self.__delai, func=self.joue)
            else:
                return
        else:
            self.__valeur_choix = 3
            self.change_bouton_mode()
            self.son_stop()
        return
            
    def affichage(self):
        """
        Controleur -> NoneType
        Affiche la partie de Tetris
        """
        if self.__tetris.forme_tombe():
            self.__delai = self.__delai_backup
        else:
            self.__vue.dessine_terrain()
            self.__vue.dessine_forme(self.__tetris.get_coords_forme(), self.__tetris.get_couleur_forme())
            self.__vue.dessine_forme_suivante(self.__tetris.get_coords_suivante(), self.__tetris.get_couleur_suivante())
            self.__vue.met_a_jour_score(self.__tetris.get_score())
        return
    
    def forme_a_gauche(self, event):
        """
        Controleur -> NoneType
        Fait aller la forme à gauche
        """
        self.__tetris.forme_a_gauche()
        return
    
    def forme_a_droite(self, event):
        """
        Controleur -> NoneType
        Fait déplacer la forme à droite
        """
        self.__tetris.forme_a_droite()
        return

    def forme_tombe(self, event):
        """
        Controleur -> NoneType
        Fait déplacer la forme plus rapidement
        """
        self.__delai = 10
        return 
    
    def forme_tourne(self, event):
        """
        Controleur -> NoneType
        Fait une rotation de la forme
        """
        self.__tetris.forme_tourne()
        return
    
    def change_bouton_mode(self):
        """
        Controleur -> NoneType
        Modifie le bouton qui fait tout
        """
        text_, command_ = self.__manager[self.__valeur_choix]
        self.__vue.get_boutonquifaittout().configure(text=text_, command=command_)
        return
    
    def lance_partie(self):
        """
        Controleur -> NoneType
        Lance la partie
        """
        self.__valeur_choix = 1
        self.change_bouton_mode()
        self.joue()
        self.son_play()
        return
    
    def pause(self):
        """
        Controleur -> NoneType
        Met en pause la partie
        """
        self.__valeur_choix = 2
        self.change_bouton_mode()
        self.pause_ = 1
        self.__fen.unbind("<Key-Left>")
        self.__fen.unbind("<Key-Right>")
        self.__fen.unbind("<Key-Down>")
        self.__fen.unbind("<Key-Up>")
        self.__fen.unbind("<space>")
        self.__fen.bind("<Escape>", self.reprendre_event)
        self.son_pause()
        return
    
    def pause_event(self, event):
        """
        Controleur -> NoneType
        Met sur pause le jeu via le bouton Echap
        """
        if self.__valeur_choix == 1:
            self.pause()
        return
    
    def reprendre(self):
        """
        Controleur -> NoneType
        Reprend la partie
        """
        self.__valeur_choix = 1
        self.change_bouton_mode()
        self.pause_ = 0
        self.__fen.bind("<Key-Left>", self.forme_a_gauche)
        self.__fen.bind("<Key-Right>", self.forme_a_droite)
        self.__fen.bind("<Key-Down>", self.forme_tombe)
        self.__fen.bind("<Key-Up>", self.forme_tourne)
        self.__fen.bind("<space>", self.forme_tombe_instant)
        self.__fen.bind("<Escape>", self.pause_event)
        self.joue()
        self.son_unpause()
        return
    
    def reprendre_event(self, event):
        """
        Controleur -> NoneType
        Reprend la partie via le bouton Echap
        """
        if self.__valeur_choix == 2:
            self.reprendre()
        return
    
    def recommencer(self):
        """
        Controleur -> NoneType
        Recommence la partie
        """
        self.__valeur_choix = 1
        self.change_bouton_mode()
        self.__delai = self.__delai_backup
        self.__tetris.reinitialise()
        self.__vue.met_a_jour_score(0)
        self.joue()
        self.son_play()
        return
    
    def forme_tombe_instant(self, event):
        """
        Controleur -> NoneType
        Fais tomber la pièce instantanément
        """
        self.__delai = 0
        return
    
    def son_play(self):
        """
        Controleur -> NoneType
        Lance la musique du Tetris.
        """
        pygame.mixer.music.load("./sounds/tetris_background_soundtrack.mp3")
        pygame.mixer.music.play(loops=-1)
        return
        
    def son_pause(self):
        """
        Controleur -> NoneType
        Met en pause la musique du Tetris.
        """
        pygame.mixer.music.pause()
        return
    
    def son_unpause(self):
        """
        Controleur -> NoneType
        Reprend la musique du Tetris.
        """
        pygame.mixer.music.unpause()
        return
        
    def son_stop(self):
        """
        Controleur -> NoneType
        Stop la musique du Tetris.
        """
        pygame.mixer.music.stop()
        return
       

if __name__ == "__main__" :
    # création du modèle
    tetris = modele.ModeleTetris()
    # création du contrôleur. c'est lui qui créé la vue
    # et lance la boucle d'écoute des événements
    ctrl = Controleur(tetris)