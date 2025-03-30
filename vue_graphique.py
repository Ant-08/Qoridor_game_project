from tkinter import *
from colorama import Fore, Style
from PIL import *
import time


class vue_graphique(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.afficher_premiere_fenetre_bool = True
        self.afficher_fenetre_mode_bool = False
        self.afficher_fenetre_selectpm_bool = False
        self.afficher_fenetre_jeu_bool = False
        self.taille=11
        self.taille_true=self.taille*2-1
        self.choix_mode=None
        self.choix_p=None
        self.choix_murs=None
        self.pion_selectionne = 1
        self.mur = [0, 0, 0, 0]
        plateau = [['O' if (c % 2 == 0 and l % 2 == 0) else ' ' for c in range(self.taille * 2 - 1)] for l in range(self.taille * 2 - 1)]
        plateau[0][len(plateau)//2]='j'
        plateau[-1][len(plateau)//2]='i'
        self.plateau=plateau
        self.tour=1
        self.cooldown=5
        self.input=None
        self.input_p=None
        self.mur_select=None
        self.type_pion1=None
        self.type_pion2=None

        self.title("QUORIDOR")
        self.geometry("800x600")  # Définition de la taille de la fenêtre principale

        # Création des sous-fenêtres
        self.premiere_fenetre = Frame(self, width=800, height=600)
        self.fenetre_mode = Frame(self, width=800, height=600)
        self.fenetre_jeu = Frame(self, width=800, height=600)
        self.fenetre_selectpm=Frame(self, width=800, height=600)



        # Chargement des images
        self.image_premiere = PhotoImage(file="fond-fortnite.png")
        self.image_deuxieme = PhotoImage(file="fond-fortnite-2.png")


        # Création des widgets pour afficher les images de fond
        self.canvas_premiere = Canvas(self.premiere_fenetre, width=800, height=600, bg=self.cget("bg"))
        self.canvas_premiere.create_image(0, 0, anchor=NW, image=self.image_premiere)
        self.canvas_premiere.pack()

        self.canvas_mode = Canvas(self.fenetre_mode, width=800, height=600, bg=self.cget("bg"))
        self.canvas_mode.create_image(0, 0, anchor=NW, image=self.image_premiere)
        self.canvas_mode.pack()

        self.canvas_selectpm = Canvas(self.fenetre_selectpm, width=800, height=600, bg=self.cget("bg"))
        self.canvas_selectpm.create_image(0, 0, anchor=NW, image=self.image_deuxieme)
        self.canvas_selectpm.pack()

        self.canvas_jeu = Canvas(self.fenetre_jeu, width=800, height=600, bg=self.cget("bg"))
        self.canvas_jeu.create_image(0, 0, anchor=NW, image=self.image_deuxieme)
        self.canvas_jeu.pack()

        self.frame_plateau = Frame(self.canvas_jeu, width=self.taille*30+(self.taille-1)*9, height=self.taille*30+(self.taille-1)*9, borderwidth=1,relief="solid")
        self.frame_plateau.place(relx=0.5, rely=0.5, anchor=CENTER)
        self.frames = [[None] * self.taille_true for _ in range(self.taille_true)]

        # Création des boutons colorés


        self.crochet1=self.canvas_mode.create_text(200, 450, text="[  ]", font=self.police(38), fill="white")
        self.crochet2=self.canvas_mode.create_text(600, 450, text="[  ]", font=self.police(38), fill="white")
        self.canvas_mode.tag_bind(self.crochet1, "<Button-1>", self.handle_mode_robots)
        self.canvas_mode.tag_bind(self.crochet2, "<Button-1>", self.handle_mode_1v1)


        self.texte_valider= self.canvas_selectpm.create_text(400, 550, text="Valider", font=self.police(38), fill="white")
        x0, y0, x1, y1 = self.canvas_selectpm.bbox(self.texte_valider)
        self.rect_encadrement = self.canvas_selectpm.create_rectangle(x0 - 10, y0 - 10, x1 + 10, y1 + 10, outline="white", width=8)
        self.canvas_selectpm.tag_bind(self.texte_valider, "<Button-1>", self.valider_selection)


        # Affichage initial
        self.afficher_premiere_fenetre()
        self.update()

    def police(self,i):
        return ("Burbank Big Condensed", i, "bold")



    def afficher_premiere_fenetre(self, events=None):
        while self.afficher_premiere_fenetre_bool :
            self.update()

            self.premiere_fenetre.place(x=0, y=0)
            self.fenetre_mode.place_forget()
            self.fenetre_selectpm.place_forget()
            self.fenetre_jeu.place_forget()

            self.canvas_premiere.create_text(400,300,text="QUORIDOR",font=self.police(74), fill="white")
            self.canvas_premiere.create_text(400,400,text="Appuyez quelque part pour continuer",font=self.police(24), fill="white")
            self.canvas_premiere.bind("<Button-1>", self.afficher_fenetre_mode)

    def afficher_fenetre_mode(self, events=None):
        self.afficher_premiere_fenetre_bool = False
        self.afficher_fenetre_mode_bool = True
        while self.afficher_fenetre_mode_bool :
            self.premiere_fenetre.place_forget()
            self.fenetre_mode.place(x=0, y=0)
            self.fenetre_selectpm.place_forget()
            self.fenetre_jeu.place_forget()
            self.canvas_mode.create_text(400,200, text="Selectionnez votre mode de jeu",font=self.police(38), fill="white")
            self.canvas_mode.create_text(200, 400, text="Robots aléatoire", font=self.police(38),fill="white")
            self.canvas_mode.create_text(590, 400, text="Joueur contre Joueur", font=self.police(38),fill="white")
            self.update()


    def handle_mode_robots(self, event):
        self.choix_mode=1
        self.afficher_fenetre_mode_bool = False

    def handle_mode_1v1(self, event):
        self.choix_mode=2
        self.afficher_fenetre_mode_bool=False


    def afficher_fenetre_selectpm(self, i):
        self.update()
        self.premiere_fenetre.place_forget()
        self.fenetre_mode.place_forget()
        self.fenetre_selectpm.place(x=0, y=0)
        self.fenetre_jeu.place_forget()
        self.selectpm()
        self.selectmur()
        self.canvas_selectpm.create_text(400, 50, text=f"Selectionnez le pion et les murs du joueur {i}",font=self.police(36), fill="white")
        self.canvas_selectpm.create_text(100, 250, anchor=W, text="Pion Sapeur\n(casse un mur)", font=self.police(20),fill="white")
        self.canvas_selectpm.create_text(100, 350, anchor=W, text="Pion Jumper\n(saute un mur)", font=self.police(20),fill="white")
        self.canvas_selectpm.create_text(100, 450, anchor=W, text="Pion Sprinter\n(avance de deux cases)",font=self.police(20), fill="white")
        self.canvas_selectpm.create_text(500, 250, anchor=W, text="WallSolide. Mur incassable. \nCout 2.",font=self.police(20), fill="white")
        self.canvas_selectpm.create_text(500, 315, anchor=W, text="WallLong. Mur de longueur 4. \nCout 2.",font=self.police(20), fill="white")
        self.canvas_selectpm.create_text(500, 380, anchor=W, text="WallReusable. Mur réutilisable. \nCout 2.",font=self.police(20), fill="white")
        self.canvas_selectpm.create_text(500, 450, anchor=W, text="WallDoor. Mur // porte. \nCout 2.",font=self.police(20), fill="white")

    def valider_selection(self,event):
        self.choix_murs=self.choix_mur
        self.choix_p=self.pion_selectionne


    def choix_mur(self,i):
        choix=None
        while choix==None:
            self.afficher_fenetre_selectpm(i)
            choix=self.choix_murs
        self.choix_murs = None
        return choix

    def choix_pion(self,i):
        choix = None
        while choix == None:
            self.afficher_fenetre_selectpm(i)
            choix = self.choix_p
        self.choix_p = None
        return choix


    def selectpm(self):

        self.crochet3 = self.canvas_selectpm.create_text(50, 250,  text="[  ]", font=self.police(38), fill="white")
        self.crochet4 = self.canvas_selectpm.create_text(50, 350,  text="[  ]", font=self.police(38), fill="white")
        self.crochet5 = self.canvas_selectpm.create_text(50, 450,  text="[  ]", font=self.police(38), fill="white")

        def choisir_pion(crochet, pion):
            # Mettre à jour la variable de sélection
            self.pion_selectionne = pion

            # Mettre à jour visuellement les crochets
            crochets = [self.crochet3, self.crochet4, self.crochet5]
            for c in crochets:
                if c == crochet:
                    self.canvas_selectpm.itemconfig(c, text="[X]", fill="white")
                else:
                    self.canvas_selectpm.itemconfig(c, text="[  ]", fill="white")

        self.canvas_selectpm.tag_bind(self.crochet3, "<Button-1>",lambda event: choisir_pion(self.crochet3, 0))
        self.canvas_selectpm.tag_bind(self.crochet4, "<Button-1>",lambda event: choisir_pion(self.crochet4, 1))
        self.canvas_selectpm.tag_bind(self.crochet5, "<Button-1>",lambda event: choisir_pion(self.crochet5, 2))

    def selectmur(self):
        self.plus1 = self.canvas_selectpm.create_text(450, 250, text="+", font=self.police(28), fill="white")
        self.plus2 = self.canvas_selectpm.create_text(450, 315, text="+", font=self.police(28), fill="white")
        self.plus3 = self.canvas_selectpm.create_text(450, 380, text="+", font=self.police(28), fill="white")
        self.plus4 = self.canvas_selectpm.create_text(450, 450, text="+", font=self.police(28), fill="white")
        self.moins1 = self.canvas_selectpm.create_text(400, 250, text="-", font=self.police(28), fill="white")
        self.moins2 = self.canvas_selectpm.create_text(400, 315, text="-", font=self.police(28), fill="white")
        self.moins3 = self.canvas_selectpm.create_text(400, 380, text="-", font=self.police(28), fill="white")
        self.moins4 = self.canvas_selectpm.create_text(400, 450, text="-", font=self.police(28), fill="white")
        self.nb1= self.canvas_selectpm.create_text(425, 250, text=self.mur[0], font=self.police(28), fill="white")
        self.nb2= self.canvas_selectpm.create_text(425, 315, text=self.mur[1], font=self.police(28), fill="white")
        self.nb3= self.canvas_selectpm.create_text(425, 380, text=self.mur[2], font=self.police(28), fill="white")
        self.nb4= self.canvas_selectpm.create_text(425, 450, text=self.mur[3], font=self.police(28), fill="white")

        self.canvas_selectpm.tag_bind(self.plus1, "<Button-1>", lambda event, mur=1: self.ajouter_mur(event, mur))
        self.canvas_selectpm.tag_bind(self.moins1, "<Button-1>", lambda event, mur=1: self.retirer_mur(event, mur))
        self.canvas_selectpm.tag_bind(self.plus2, "<Button-1>", lambda event, mur=2: self.ajouter_mur(event, mur))
        self.canvas_selectpm.tag_bind(self.moins2, "<Button-1>", lambda event, mur=2: self.retirer_mur(event, mur))
        self.canvas_selectpm.tag_bind(self.plus3, "<Button-1>", lambda event, mur=3: self.ajouter_mur(event, mur))
        self.canvas_selectpm.tag_bind(self.moins3, "<Button-1>", lambda event, mur=3: self.retirer_mur(event, mur))
        self.canvas_selectpm.tag_bind(self.plus4, "<Button-1>", lambda event, mur=4: self.ajouter_mur(event, mur))
        self.canvas_selectpm.tag_bind(self.moins4, "<Button-1>", lambda event, mur=4: self.retirer_mur(event, mur))


    def ajouter_mur(self, event, mur):
        self.update()
        self.mur[mur-1] += 1
        if mur == 1:
            self.canvas_selectpm.itemconfig(self.nb1, text=self.mur[mur - 1])
        elif mur == 2:
            self.canvas_selectpm.itemconfig(self.nb2, text=self.mur[mur - 1])
        elif mur == 3:
            self.canvas_selectpm.itemconfig(self.nb3, text=self.mur[mur - 1])
        elif mur == 4:
            self.canvas_selectpm.itemconfig(self.nb4, text=self.mur[mur - 1])


    def retirer_mur(self, event, mur):
        self.update()
        if self.mur[mur - 1] > 0:
            self.mur[mur - 1] -= 1
            if mur == 1:
                self.canvas_selectpm.itemconfig(self.nb1, text=self.mur[mur - 1])
            elif mur == 2:
                self.canvas_selectpm.itemconfig(self.nb2, text=self.mur[mur - 1])
            elif mur == 3:
                self.canvas_selectpm.itemconfig(self.nb3, text=self.mur[mur - 1])
            elif mur == 4:
                self.canvas_selectpm.itemconfig(self.nb4, text=self.mur[mur - 1])

    def afficher_fenetre_jeu(self, events=None ):
        self.afficher_premiere_fenetre_bool = False
        self.afficher_fenetre_mode_bool = False
        self.afficher_fenetre_selectpm_bool = False
        self.afficher_fenetre_jeu_bool = True
        #while self.afficher_fenetre_jeu_bool :
        self.update()
        self.premiere_fenetre.place_forget()
        self.fenetre_mode.place_forget()
        self.fenetre_selectpm.place_forget()
        self.fenetre_jeu.place(x=0, y=0)
        self.canvas_jeu.create_text(100,90, text="Joueur 1", font=self.police(30), fill='white')
        self.canvas_jeu.create_text(700,90, text="Joueur 2", font=self.police(30), fill='white')



    def afficher_resultat(self,resultat):

        if resultat=="Le joueur":
            self.canvas_jeu.create_text(400, 550, text=f"C'est Alex qui a gagné", font=self.police(40), fill="white")
        elif resultat=="L'adversaire":
            self.canvas_jeu.create_text(400, 550, text=f"C'est Steve qui a gagné", font=self.police(40),fill="white")
        self.update()

    def get_user_input(self, cooldown):
        self.cooldown = cooldown
        input_value = None
        while input_value is None:
            self.update()
            self.bouger_pion()
            self.poser_murs()
            self.pouvoir()
            input_value = self.input
        self.input = None
        self.disable_bindings_moove()
        return input_value

    def pouvoir(self):
        if self.cooldown>=5:
            if self.tour==1:
                pouvoir=self.type_pion1
            else:
                pouvoir=self.type_pion2
            if pouvoir==0:
                self.destruct_wall()
            elif pouvoir==1:
                self.jump()
            elif pouvoir==2:
                self.sprint()

    def sprint(self):
        self.update
        if self.tour == 1:
            tour = 'i'
        else:
            tour = 'j'
        voisin=[]
        for i in range(self.taille_true):
            for j in range(self.taille_true):
                if self.plateau[i][j] == tour:
                    if i + 4 <= self.taille_true and self.plateau[i + 1][j] == ' ' and self.plateau[i + 3][j] == ' ' and self.plateau[i + 2][j] == 'O':
                        voisin.append((i + 4, j))
                    if i - 4 >= 0 and self.plateau[i - 1][j] == ' ' and self.plateau[i - 3][j] == ' ' and self.plateau[i - 2][j] == 'O':
                        voisin.append((i - 4, j))
                    if j + 4 <= self.taille_true and self.plateau[i][j + 1] == ' ' and self.plateau[i][j + 3] == ' ' and self.plateau[i][j+2] == 'O':
                        voisin.append((i, j + 4))
                    if j - 4 >= 0 and self.plateau[i][j - 1] == ' ' and self.plateau[i][j - 3] == ' ' and self.plateau[i][j-2] == 'O':
                        voisin.append((i, j - 4))
                    cor = (i, j)
        for pos in voisin:
            case = self.frames[pos[0]][pos[1]]
            case.bind("<Enter>", lambda event, widget=case: self.on_enter_green(event, widget))
            case.bind("<Leave>", lambda event, widget=case: self.on_leave_green(event, widget))
            case.bind("<Button-1>",
                      lambda event, direction=pos, position=cor: self.update_sprint_input(direction, position))

    def update_sprint_input(self, direction,position):
        i, j = direction
        player_input = None

        if  i == position[0] + 4 and j == position[1]:
            player_input = 'bas'
        elif i == position[0] - 4 and j == position[1]:
            player_input = 'haut'
        elif i == position[0] and  j == position[1] + 4:
            player_input = 'droite'
        elif i == position[0] and  j == position[1] - 4:
            player_input = 'gauche'

        self.input_p = player_input
        self.input="pouvoir"

    def jump(self):
        self.update()
        if self.tour == 1:
            tour = 'i'
        else:
            tour = 'j'
        voisin=[]
        for i in range(self.taille_true):
            for j in range(self.taille_true):
                if self.plateau[i][j] == tour:
                    if i + 2 <= self.taille_true and self.plateau[i+1][j]!=' ':
                        voisin.append((i + 2, j))
                    if i - 2 >= 0  and self.plateau[i-1][j]!=' ':
                        voisin.append((i - 2, j))
                    if j + 2 <= self.taille_true and self.plateau[i][j+1]!=' ' :
                        voisin.append((i, j + 2))
                    if j - 2 >= 0 and self.plateau[i][j-1]!=' ':
                        voisin.append((i, j - 2))
                    cor = (i, j)
                for pos in voisin:
                    case = self.frames[pos[0]][pos[1]]
                    case.bind("<Enter>", lambda event, widget=case: self.on_enter_green(event, widget))
                    case.bind("<Leave>", lambda event, widget=case: self.on_leave_green(event, widget))
                    case.bind("<Button-1>",lambda event, direction=pos, position=cor: self.update_jump_input(direction, position))

    def on_enter_green(self, event, widget):
        widget.config(bg="green")

    def on_leave_green(self, event, widget):
        widget.config(bg="navy")

    def update_jump_input(self, direction,position):
        i, j = direction
        player_input = None

        if i == position[0] + 2 and j == position[1]:
            player_input = 'bas'
        elif i == position[0] - 2 and j == position[1]:
            player_input = 'haut'
        elif i == position[0] and j == position[1] + 2:
            player_input = 'droite'
        elif i == position[0] and j == position[1] - 2:
            player_input = 'gauche'

        self.input_p = player_input
        self.input="pouvoir"

    def destruct_wall(self):
        if self.tour == 1:
            tour = 'i'
        else:
            tour = 'j'
        voisin = []
        for i in range(self.taille_true):
            for j in range(self.taille_true):
                if self.plateau[i][j] == tour:
                    true = 1
                    if j + 2 <= self.taille_true and self.plateau[i][j + 1] != ' ' and self.plateau[i][j + 1] != 1:
                        voisin.append((i, j + 1, true))
                    elif j - 2 >= 0 and self.plateau[i][j - 1] != ' ' and self.plateau[i][j - 1] != 1:
                        voisin.append((i, j - 1, true))
                    elif i + 2 <= self.taille_true and self.plateau[i + 1][j] != ' ' and self.plateau[i + 1][j] != 1:
                        if self.plateau[i + 1][j - 1] == ' ':
                            true = 0
                        voisin.append((i + 1, j, true))
                    elif i - 2 >= 0 and self.plateau[i - 1][j] != ' ' and self.plateau[i - 1][j] != 1:
                        if self.plateau[i - 1][j - 1] == ' ':
                            true = 0
                        voisin.append((i - 1, j, true))
                    position_du_pion = i, j
        for x in range(len(voisin)):
            case = self.frames[voisin[x][0]][voisin[x][1]]
            position = voisin[x][0], voisin[x][1]

            for widget in case.winfo_children():
                widget.destroy()

            case.config(bg="green")
            case.bind("<Button-1>",
                       lambda event, widget=case, pos=position_du_pion, direction=position: self.update_input_wall_destruct(event,widget,pos,direction))

    def update_input_wall_destruct(self, event,widget, position, direction):
        i, j = direction
        player_input = None

        if i == position[0] + 1 and j == position[1]:
            player_input = 'bas'
        elif i == position[0] - 1 and j == position[1]:
            player_input = 'haut'
        elif i == position[0] and j == position[1] + 1:
            player_input = 'droite'
        elif i == position[0] and j == position[1] - 1:
            player_input = 'gauche'

        widget.config(bg="black")
        self.input_p = player_input
        self.input = "pouvoir"

    def select_dir_pouvoir(self):
        input_value = None
        while input_value is None:
            self.update()
            input_value = self.input_p
        self.input_p = None
        return input_value



    def bouger_pion(self):
        self.update()
        self.voisinage = []
        if self.tour == 1:
            tour = 'i'
            tour_n='j'
        else:
            tour = 'j'
            tour_n='i'
        for i in range(self.taille_true):
            for j in range(self.taille_true):
                if self.plateau[i][j] == tour:
                    if i + 2 <= self.taille_true and self.plateau[i+1][j]==' ':
                        if self.plateau[i + 2][j]==tour_n and self.plateau[i+3][j]==' ':
                            self.voisinage.append((i + 4, j))
                        else:
                            self.voisinage.append((i + 2, j))
                    if i - 2 >= 0 and self.plateau[i-1][j]==' ':
                        if self.plateau[i - 2][j]==tour_n and self.plateau[i-3][j]==' ':
                            self.voisinage.append((i - 4, j))
                        else:
                            self.voisinage.append((i - 2, j))
                    if j + 2 <= self.taille_true and self.plateau[i][j+1]==' ':
                        if self.plateau[i][j + 2]==tour_n and self.plateau[i][j+3]==' ':
                            self.voisinage.append((i, j+4))
                        else:
                            self.voisinage.append((i, j + 2))
                    if j - 2 >= 0 and self.plateau[i][j-1]==' ':
                        if self.plateau[i][j - 2]==tour_n and self.plateau[i][j-3]==' ':
                            self.voisinage.append((i, j-4))
                        else:
                            self.voisinage.append((i, j - 2))
                    cor=(i,j)
        for pos in self.voisinage:
            case = self.frames[pos[0]][pos[1]]
            case.bind("<Enter>", lambda event, widget=case: self.on_enter_moove(event, widget))
            case.bind("<Leave>", lambda event, widget=case: self.on_leave_moove(event, widget))
            case.bind("<Button-1>", lambda event, direction=pos, position=cor: self.update_bouger_input(direction,position))

    def on_enter_moove(self, event, widget):
        widget.config(bg="blue")

    def on_leave_moove(self, event, widget):
        widget.config(bg="navy")

    def update_bouger_input(self, direction,position):
        i, j = direction
        player_input = None

        if (i == position[0] + 2 or i == position[0] + 4) and j == position[1]:
            player_input = 'down'
        elif (i == position[0] - 2 or i == position[0] - 4) and j == position[1]:
            player_input = 'up'
        elif i == position[0] and (j == position[1] + 2 or j == position[1] + 4):
            player_input = 'right'
        elif i == position[0] and (j == position[1] - 2 or j == position[1] - 4):
            player_input = 'left'

        self.input = player_input

    def disable_bindings_moove(self):
        for pos in self.voisinage:
            case = self.frames[pos[0]][pos[1]]
            case.config(bg="navy")
            case.unbind("<Enter>")
            case.unbind("<Leave>")
            case.unbind("<Button-1>")


    def poser_murs(self):
        for i in range(self.taille_true):
            for j in range(self.taille_true):
                if self.plateau[i][j] == ' ':
                    if i % 2 == 0 and j % 2 == 1:
                        if i>0:# vertical
                            case = self.frames[i][j]
                            voisin1 = [(i - 1, j), (i - 2, j)]
                            if self.plateau[voisin1[0][0]][voisin1[0][1]]==' ' and self.plateau[voisin1[1][0]][voisin1[1][1]]==' ':
                                case.bind("<Enter>",
                                          lambda event, widget=case, voisin=voisin1: self.on_enter_wall(event, widget, voisin))
                                case.bind("<Leave>",
                                          lambda event, widget=case, voisin=voisin1: self.on_leave_wall(event, widget, voisin))
                                case.bind("<Button-1>",
                                          lambda event, pos=(i, j), direction='n': self.update_input_wall(event, pos, direction))

                    if i % 2 == 1 and j % 2 == 0:
                        if j>0:# horizontal
                            case = self.frames[i][j]
                            voisin1 = [(i, j-1), (i, j-2)]
                            if self.plateau[voisin1[0][0]][voisin1[0][1]]==' ' and self.plateau[voisin1[1][0]][voisin1[1][1]]==' ':
                                case.bind("<Enter>",
                                          lambda event, widget=case, voisin=voisin1: self.on_enter_wall(event, widget, voisin))
                                case.bind("<Leave>",
                                          lambda event, widget=case, voisin=voisin1: self.on_leave_wall(event, widget, voisin))
                                case.bind("<Button-1>",
                                          lambda event, pos=(i, j), direction='w': self.update_input_wall(event, pos, direction))

    def on_enter_wall(self, event, widget, voisin):
        widget.config(bg="red")
        for pos in voisin:
            voisin_case = self.frames[pos[0]][pos[1]]
            voisin_case.config(bg="red")

    def on_leave_wall(self, event, widget, voisin):
        widget.config(bg="black")
        for pos in voisin:
            voisin_case = self.frames[pos[0]][pos[1]]
            voisin_case.config(bg="black")

    def update_input_wall(self, event, pos, direction ):

        coordinates = f"{pos[0]},{pos[1]}"
        self.input = f"{coordinates}{direction}"

    def disable_binding_wall(self):
        for i in range(self.taille_true):
            for j in range(self.taille_true):
                if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0):
                    case = self.frames[i][j]

                    case.unbind("<Enter>")
                    case.unbind("<Leave>")
                    case.unbind("<Button-1>")

    def select_mur(self,murs):
        input_value = None
        while input_value is None:
            self.update()
            self.choisir_type_mur()
            input_value = self.mur_select
        self.mur_select = None
        self.disable_bindings_select()
        for i in range(self.taille_true):
            for j in range(self.taille_true):
                if (i % 2 == 0 and j % 2 == 1) or (i % 2 == 1 and j % 2 == 0) or (i % 2 == 1 and j % 2 == 1):
                    case = self.frames[i][j]
                    case.config(bg="black")
        return input_value

    def choisir_type_mur(self):
        self.disable_binding_wall()
        if self.tour==1:
            self.canvas_jeu.tag_bind(self.murs10,"<Button-1>", lambda event, type=0: self.update_mur_select(type))
            self.canvas_jeu.tag_bind(self.murs11,"<Button-1>", lambda event, type=1: self.update_mur_select(type))
            self.canvas_jeu.tag_bind(self.murs12,"<Button-1>", lambda event, type=2: self.update_mur_select(type))
            self.canvas_jeu.tag_bind(self.murs13,"<Button-1>", lambda event, type=3: self.update_mur_select(type))
            self.canvas_jeu.tag_bind(self.murs14,"<Button-1>", lambda event, type=4: self.update_mur_select(type))
        else:
            self.canvas_jeu.tag_bind(self.murs20, "<Button-1>", lambda event, type=0: self.update_mur_select(type))
            self.canvas_jeu.tag_bind(self.murs21, "<Button-1>", lambda event, type=1: self.update_mur_select(type))
            self.canvas_jeu.tag_bind(self.murs22, "<Button-1>", lambda event, type=2: self.update_mur_select(type))
            self.canvas_jeu.tag_bind(self.murs23, "<Button-1>", lambda event, type=3: self.update_mur_select(type))
            self.canvas_jeu.tag_bind(self.murs24, "<Button-1>", lambda event, type=4: self.update_mur_select(type))


    def update_mur_select(self,type):
        self.mur_select=type

    def disable_bindings_select(self):
        if self.tour==1:
            self.canvas_jeu.tag_unbind(self.murs10, "<Button-1>")
            self.canvas_jeu.tag_unbind(self.murs11, "<Button-1>")
            self.canvas_jeu.tag_unbind(self.murs12, "<Button-1>")
            self.canvas_jeu.tag_unbind(self.murs13, "<Button-1>")
            self.canvas_jeu.tag_unbind(self.murs14, "<Button-1>")
        else:
            self.canvas_jeu.tag_unbind(self.murs20, "<Button-1>")
            self.canvas_jeu.tag_unbind(self.murs21, "<Button-1>")
            self.canvas_jeu.tag_unbind(self.murs22, "<Button-1>")
            self.canvas_jeu.tag_unbind(self.murs23, "<Button-1>")
            self.canvas_jeu.tag_unbind(self.murs24, "<Button-1>")

    def afficher_plateau(self):
        self.update()
        self.texte_tour=self.canvas_jeu.create_text(400,50,text=f"Au tour du joueur {self.tour}",font=self.police(48), fill="white")
        self.murs10=self.canvas_jeu.create_text(25,150,anchor=W, text=f"Mur Classique,\n reste: {0}",font=self.police(15), fill="white")
        self.murs11=self.canvas_jeu.create_text(25,225,anchor=W, text=f"Mur Solide,\n reste: {0}",font=self.police(15), fill="white")
        self.murs12=self.canvas_jeu.create_text(25,300,anchor=W ,text=f"Mur Long,\n reste: {0}",font=self.police(15), fill="white")
        self.murs13=self.canvas_jeu.create_text(25,375,anchor=W ,text=f"Mur Porte,\n reste: {0}",font=self.police(15), fill="white")
        self.murs14=self.canvas_jeu.create_text(25,450,anchor=W, text=f"Mur Temporaire,\n reste: {0}",font=self.police(15), fill="white")
        self.murs20=self.canvas_jeu.create_text(650,150,anchor=W,text=f"Mur Classique,\n reste: {0}",font=self.police(15), fill="white")
        self.murs21=self.canvas_jeu.create_text(650,225,anchor=W,text=f"Mur Solide,\n reste: {0}",font=self.police(15), fill="white")
        self.murs22=self.canvas_jeu.create_text(650,300,anchor=W,text=f"Mur Long,\n reste: {0}",font=self.police(15), fill="white")
        self.murs23=self.canvas_jeu.create_text(650,375,anchor=W,text=f"Mur Porte,\n reste: {0}",font=self.police(15), fill="white")
        self.murs24=self.canvas_jeu.create_text(650,450,anchor=W,text=f"Mur Temporaire,\n reste: {0}",font=self.police(15), fill="white")
        self.affich_cooldown1=self.canvas_jeu.create_text(25,550,anchor=W,text=f"Cooldown: {0}",font=self.police(18), fill="white")
        self.affich_cooldown2=self.canvas_jeu.create_text(650,550,anchor=W,text=f"Cooldown: {0}",font=self.police(18), fill="white")



        for i in range(self.taille_true):
            for j in range(self.taille_true):
                case = self.plateau[i][j]
                if i % 2 == 0 and j % 2 == 0:

                    frame = Frame(self.frame_plateau, width=30, height=30, borderwidth=0,bg="navy", highlightthickness=0)
                    frame.grid(row=i, column=j)
                    frame.grid_propagate(False)
                    frame.pack_propagate(0)
                    if case == 'i':
                        pion_image = PhotoImage(file="alex.png")
                        label = Label(frame, image=pion_image)
                        label.photo = pion_image
                        label.pack()
                    elif case == 'j':
                        pion_image = PhotoImage(file="steve.png")
                        label = Label(frame, image=pion_image)
                        label.photo = pion_image
                        label.pack()


                elif i%2==0 and j%2 ==1 :

                    frame = Frame(self.frame_plateau, width=9, height=30, borderwidth=0,bg="black", highlightthickness=0)
                    frame.grid(row=i, column=j)
                    frame.grid_propagate(False)
                    frame.pack_propagate(0)
                    if case==0:
                        mur_image = PhotoImage(file="block_nether_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 1:
                        mur_image = PhotoImage(file="block_bois_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 2:
                        mur_image = PhotoImage(file="block_metal_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 3:
                        mur_image = PhotoImage(file="block_terre_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 4:
                        mur_image = PhotoImage(file="block_caillou_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 'O':
                        pass
                    elif case == " ":
                        pass

                elif i % 2 == 1 and j % 2 == 0:

                    frame = Frame(self.frame_plateau, width=30, height=9, borderwidth=0,bg="black",highlightthickness=0)
                    frame.grid(row=i, column=j)
                    frame.grid_propagate(False)
                    frame.pack_propagate(0)
                    if case==0:
                        mur_image = PhotoImage(file="block_nether_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 1:
                        mur_image = PhotoImage(file="block_bois_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 2:
                        mur_image = PhotoImage(file="block_metal_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 3:
                        mur_image = PhotoImage(file="block_terre_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 4:
                        mur_image = PhotoImage(file="block_caillou_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 'O':
                        pass
                    elif case == " ":
                        pass

                else :

                    frame = Frame(self.frame_plateau, width=9, height=9, borderwidth=0,bg="black", highlightthickness=0)
                    frame.grid(row=i, column=j)
                    frame.grid_propagate(False)
                    frame.pack_propagate(0)
                    if case==0:
                        mur_image = PhotoImage(file="block_nether.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 1:
                        mur_image = PhotoImage(file="block_bois.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 2:
                        mur_image = PhotoImage(file="block_metal.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 3:
                        mur_image = PhotoImage(file="block_terre.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 4:
                        mur_image = PhotoImage(file="block_caillou.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 'O':
                        pass
                    elif case == " ":
                        pass

                self.frames[i][j] = frame

    def mettre_a_jour_plateau(self, nouveau_plateau,tour,murs01,murs02,pion1,pion2,cooldown1,cooldown2):
        self.update()
        self.tour=tour
        self.type_pion1=pion1
        self.type_pion2=pion2
        self.voisinage=[]
        murs1 = [0] * 5
        for nombre in murs01:
            murs1[nombre] += 1
        murs2 = [0] * 5
        for nombre in murs02:
            murs2[nombre] += 1

        if cooldown1>5:
            self.canvas_jeu.itemconfig(self.affich_cooldown1, text=f"Cooldown: {0}")
        else:
            self.canvas_jeu.itemconfig(self.affich_cooldown1, text=f"Cooldown: {5-cooldown1}")
        if cooldown2>5:
            self.canvas_jeu.itemconfig(self.affich_cooldown2, text=f"Cooldown: {0}")
        else:
            self.canvas_jeu.itemconfig(self.affich_cooldown2, text=f"Cooldown: {5-cooldown2}")


        self.canvas_jeu.itemconfig(self.texte_tour, text=f"Au tour du joueur {tour}")
        self.canvas_jeu.itemconfig(self.murs10, text=f"Mur Classique,\n reste: {murs1[0]}")
        self.canvas_jeu.itemconfig(self.murs11, text=f"Mur Solide,\n reste: {murs1[1]}")
        self.canvas_jeu.itemconfig(self.murs12, text=f"Mur Long,\n reste: {murs1[2]}")
        self.canvas_jeu.itemconfig(self.murs13, text=f"Mur Porte,\n reste: {murs1[3]}")
        self.canvas_jeu.itemconfig(self.murs14, text=f"Mur Temporaire,\n reste: {murs1[4]}")
        self.canvas_jeu.itemconfig(self.murs20, text=f"Mur Classique,\n reste: {murs2[0]}")
        self.canvas_jeu.itemconfig(self.murs21, text=f"Mur Solide,\n reste: {murs2[1]}")
        self.canvas_jeu.itemconfig(self.murs22, text=f"Mur Long,\n reste: {murs2[2]}")
        self.canvas_jeu.itemconfig(self.murs23, text=f"Mur Porte,\n reste: {murs2[3]}")
        self.canvas_jeu.itemconfig(self.murs24, text=f"Mur Temporaire,\n reste: {murs2[4]}")

        self.plateau = nouveau_plateau

        for i in range(self.taille_true):
            for j in range(self.taille_true):
                case = self.plateau[i][j]
                frame = self.frames[i][j]
                for widget in frame.winfo_children():
                    widget.destroy()

                if i % 2 == 0 and j % 2 == 0:

                    if case == 'i':
                        pion_image = PhotoImage(file="alex.png")
                        label = Label(frame, image=pion_image)
                        label.photo = pion_image
                        label.pack()
                    elif case == 'j':
                        pion_image = PhotoImage(file="steve.png")
                        label = Label(frame, image=pion_image)
                        label.photo = pion_image
                        label.pack()

                    # frame.bind("<Enter>", self.on_enter)
                    # frame.bind("<Leave>", self.on_leave)

                elif i % 2 == 0 and j % 2 == 1:

                    if case==0:
                        mur_image = PhotoImage(file="block_nether_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 1:
                        mur_image = PhotoImage(file="block_bois_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 2:
                        mur_image = PhotoImage(file="block_metal_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 3:
                        mur_image = PhotoImage(file="block_terre_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 4:
                        mur_image = PhotoImage(file="block_caillou_v.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 'O':
                        pass
                    elif case == " ":
                        pass

                elif i % 2 == 1 and j % 2 == 0:

                    if case==0:
                        mur_image = PhotoImage(file="block_nether_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 1:
                        mur_image = PhotoImage(file="block_bois_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 2:
                        mur_image = PhotoImage(file="block_metal_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 3:
                        mur_image = PhotoImage(file="block_terre_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 4:
                        mur_image = PhotoImage(file="block_caillou_h.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 'O':
                        pass
                    elif case == " ":
                        pass

                else:

                    if case==0:
                        mur_image = PhotoImage(file="block_nether.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 1:
                        mur_image = PhotoImage(file="block_bois.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 2:
                        mur_image = PhotoImage(file="block_metal.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 3:
                        mur_image = PhotoImage(file="block_terre.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 4:
                        mur_image = PhotoImage(file="block_caillou.png")
                        label = Label(frame, image=mur_image)
                        label.photo = mur_image
                        label.pack()
                    elif case == 'O':
                        pass
                    elif case == " ":
                        pass



