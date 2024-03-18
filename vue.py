import tkinter as tk
import modele
import pygame

DIM:int = 30
COULEURS:list = ["pink", "purple", "green", "blue", "red", "yellow","orange","dark grey","black"]    
SUIVANT:int = 6

class VueTetris:
    def __init__(self, ModeleTetris:modele.ModeleTetris):
        """
        VueTetris -> NoneType
        Constructeur de la classe VueTetris
        """
        self.__modele:modele.ModeleTetris = ModeleTetris
        self.__fenetre:tk.Tk = tk.Tk()
        fenbtn:tk.Frame = tk.Frame(self.__fenetre)
        self.__can_terrain = tk.Canvas(self.__fenetre, width=self.__modele.get_largeur() * DIM, height=self.__modele.get_hauteur() * DIM, bg="grey")
        self.__fenetre.protocol("WM_DELETE_WINDOW", self.stop_music_and_close_window)
        
        self.__can_fsuivante:tk.Canvas = tk.Canvas(fenbtn, width=SUIVANT * DIM, height=SUIVANT * DIM)
        self.__les_suivants:list = [[self.__can_fsuivante.create_rectangle(x*DIM, y*DIM, (x+1)*DIM, (y+1)*DIM, outline="grey", fill="black") for x in range(SUIVANT)] for y in range(SUIVANT)]
        self.__lbl_score:tk.Label = tk.Label(fenbtn, text="Score : 0")
        self.boutonQuitter = tk.Button(fenbtn, text="Quitter", command=self.stop_music_and_close_window)
        self.boutonquifaittout:tk.Button = tk.Button(fenbtn, text="")
        
        tk.Label(fenbtn, text="Forme suivante :").pack()
        self.__can_fsuivante.pack()
        self.__lbl_score.pack()
        self.boutonquifaittout.pack()
        self.boutonQuitter.pack()
        
        self.__can_terrain.pack(side="left")
        fenbtn.pack(side="right")

        self.__les_cases = []
        for y in range(self.__modele.get_hauteur()):
            ligne = []
            for x in range(self.__modele.get_largeur()):
                case = self.__can_terrain.create_rectangle(x*DIM, y*DIM, (x+1)*DIM, (y+1)*DIM, outline="grey", fill=COULEURS[self.__modele.get_valeur(y,x)])
                ligne.append(case)
            self.__les_cases.append(ligne)
        return

    def fenetre(self):
        """
        VueTetris -> tk.Tk
        Retourne la fenêtre
        """
        return self.__fenetre

    def dessine_case(self, y, x, coul):
        """
        VueTetris, int, int, int
        Dessine une case de couleur COULEURS[coul] aux coordonnées x y
        """
        self.__can_terrain.itemconfigure(self.__les_cases[y][x], fill=COULEURS[coul])
        return

    def dessine_terrain(self):
        """
        VueTetris -> NoneType
        Dessine le terrain
        """
        for y in range(self.__modele.get_hauteur()):
            for x in range(self.__modele.get_largeur()):
                self.dessine_case(y, x, self.__modele.get_valeur(y,x))
        return

    def dessine_forme(self, coords, couleur):
        """
        VueTetris, tuple(int,int), int -> NoneType
        Dessine la forme au coordonnées coords avec pour couleur COULEURS[couleur]
        """
        for coord in coords:
            y, x = coord
            self.dessine_case(y, x, couleur)
        return
    
    def met_a_jour_score(self, val:int):
        """
        VueTetris, int -> NoneType
        Change le texte de __lbl_score pour afficher val dans le score
        """
        self.__lbl_score.configure(text=f"Score : {val}")
        return
    
    def dessine_case_suivante(self, x:int, y:int, coul:int):
        """
        VueTetris, int, int, int -> NoneType
        Dessine une case de couleur COULEURS[coul] aux coordonnées x y dans le canvas __can_fsuivante
        """
        self.__can_fsuivante.itemconfigure(self.__les_suivants[y][x], fill=COULEURS[coul])
        return
    
    def nettoie_forme_suivante(self):
        """
        VueTetris -> NoneType
        Remet du noir sur tous les carrés de __can_fsuivante
        """
        for y in range(SUIVANT):
            for x in range(SUIVANT):
                self.dessine_case_suivante(x, y, -1)
        return

    def dessine_forme_suivante(self, coords:list, coul:int):
        """
        VueTetris, list, int -> NoneType
        Nettoie le Canvas fsuivante, puis dessine la forme suivante dedans
        """
        self.nettoie_forme_suivante()
        for x,y in coords:
            self.dessine_case_suivante(x+2, y+2, coul)
        return
    
    def get_boutonquifaittout(self):
        """
        VueTetris -> tk.Button
        Retourne le bouton qui fait tout
        """
        return self.boutonquifaittout
    
    def stop_music_and_close_window(self):
        """
        VueTetris -> NoneType
        Ferme la fenêtre et stop la musique en même temps.
        """
        pygame.mixer.music.stop()
        self.__fenetre.destroy()
        return