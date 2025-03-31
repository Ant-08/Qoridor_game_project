#Presenteur
#lien entre le modele et la vue console
# -->
from random import randint,choice

from modele import *
from vue import *
from ClientFake import Client
class presenteur_vue_console ():
    def __init__(self,jeu,vue):
        self.vue = vue
        self.partie = jeu
        self.client = Client()
    #Boucle menu
    def menu (self):
        choix = self.vue.mode_jeux()
        if choix == 1 :
            self.jeu_deux_robots()
        if choix == 2:
            self.jeu_deux_players()
        else :
            return 0
    #Méthode pour choisir un pion
    def choix_ppion (self,i):
        pion = self.vue.choix_pion(i)
        if pion == 0:
            return pionSapeur()
        elif pion == 1:
            return pionJump()
        elif pion == 2:
            return pionSprinteur()
    def choix_pmur (self,nb):
        faire_choix = True
        while faire_choix :
            mur = self.vue.choix_mur(nb)
            res = self.partie.choix_mmur(mur,nb)
            if res == True :
                faire_choix = False
            else :
                print("Il y a une erreur")
    def jeu_deux_robots(self):
        #joueur = self.choix_ppion(1)
        self.partie.init_partie(choice([pionJump(),pionSprinteur()]),choice([pionJump(),pionSprinteur()]),0)
        #self.client.registerTeam('stitch',joueur.type)
        #self.choix_pmur(0)
        joueur= self.partie.joueur
        adver = self.partie.adversaire
        print(joueur,adver)
        continuer = True
        tour = 1
        while continuer :
            if tour == 1:
                self.partie.tour_aleatoire(joueur)
            elif tour == 2:
                self.partie.tour_aleatoire(adver)
            #self.client.askPriority()
            plateau = self.partie.plateau
            self.vue.afficher_plateau(plateau)
            res = self.partie.verifier_victoire()
            if res == 1:
                continuer = False
                self.vue.afficher_resultat("Le joueur")
            elif res == 2:
                continuer = False
                self.vue.afficher_resultat("L'adversaire")
            tour = tour % 2 + 1
        self.menu()


    def jeu_deux_players(self):
        joueur1=self.choix_ppion(1)
        joueur2=self.choix_ppion(2)
        self.partie.init_partie(joueur1,joueur2,1)
        self.choix_pmur(1)
        self.choix_pmur(2)
        continuer = True
        tour = 1
        while continuer:
            plateau = self.partie.plateau
            self.vue.afficher_plateau(plateau)
            if tour == 1:
                player_input = self.vue.get_user_input(tour,self.partie.joueur.cooldown)
                self.tour_1v1(joueur1,player_input)
                self.partie.joueur.cooldown = self.partie.joueur.cooldown+1
            elif tour==2:
                player_input = self.vue.get_user_input(tour,self.partie.adversaire.cooldown)
                self.tour_1v1(joueur2,player_input)
                self.partie.adversaire.cooldown = self.partie.adversaire.cooldown+1
            res = self.partie.verifier_victoire()
            if res == 1:
                continuer = False
                self.vue.afficher_resultat("Le joueur 1")
            elif res == 2:
                continuer = False
                self.vue.afficher_resultat("Le joueur 2")
            tour = tour % 2 + 1
        self.menu()

    def tour_1v1(self,joueur,player_input):
        if joueur == self.partie.joueur :
            nous = True
        else :
            nous = False
        if player_input in ['up', 'down', 'left', 'right']:
            new_coord=()
            if nous:
                if player_input == "up":
                    new_coord = ((int(self.partie.joueur.coord[0] + -2), int(self.partie.joueur.coord[1] + 0)))
                elif player_input == "down":
                    new_coord = ((int(self.partie.joueur.coord[0] + 2), int(self.partie.joueur.coord[1] + 0)))
                elif player_input == "left":
                    new_coord = ((int(self.partie.joueur.coord[0] + 0), int(self.partie.joueur.coord[1] + -2)))
                elif player_input == "right":
                    new_coord = ((int(self.partie.joueur.coord[0] + 0), int(self.partie.joueur.coord[1] + 2)))
            else:
                if player_input == "up":
                    new_coord = ((int(self.partie.adversaire.coord[0] + -2), int(self.partie.adversaire.coord[1] + 0)))
                elif player_input == "down":
                    new_coord = ((int(self.partie.adversaire.coord[0] + 2), int(self.partie.adversaire.coord[1] + 0)))
                elif player_input == "left":
                    new_coord = ((int(self.partie.adversaire.coord[0] + 0), int(self.partie.adversaire.coord[1] + -2)))
                elif player_input == "right":
                    new_coord = ((int(self.partie.adversaire.coord[0] + 0), int(self.partie.adversaire.coord[1] + 2)))
            self.partie.avancer_joueur(new_coord, nous)
        elif player_input.endswith("n") or player_input.endswith("s") or player_input.endswith("e") or player_input.endswith("w"):
            print(joueur.mur_restant)
            murs = []
            for i in joueur.mur_restant:
                murs.append(i.type)
            mur_choisi = self.vue.select_mur(murs)
            mur=None
            for j in joueur.mur_restant:
                if j.type == int(mur_choisi):
                    mur = j
            centre = player_input.split(",")
            x = centre[0]
            y = centre[1][:-1]
            mur.centre = (int(x), int(y))
            mur.direction = player_input[-1:]
            self.partie.poser_mur(joueur, mur)

        elif player_input == "pouvoir" :
            input=self.vue.select_dir_pouvoir()
            if nous:
                self.partie.joueur.pouvoir(self.partie,input,nous)
            else:
                self.partie.adversaire.pouvoir(self.partie,input,nous)