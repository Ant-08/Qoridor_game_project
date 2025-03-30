#Presenteur
#lien entre le modele et la vue console
# -->
from random import randint,choice

from modele import *
from vue_graphique import *
from vue import *
from ClientFake import Client
import time
class presenteur_vue_console ():
    def __init__(self,jeu,vue):
        self.vue = vue
        self.manche = jeu
        self.client = Client()
        self.manche.setAffichagePLa(self.vue.afficher_plateau)
        self.manche.setAffichageResultat(self.vue.afficher_resultat)
        self.manche.setAfficheChoixMur(self.vue.choix_mur)
        self.manche.setAfficheChoixPion(self.vue.choix_pion)
        self.manche.setAfficheGetUserInput(self.vue.get_user_input)
        self.manche.setAfficheSelectMur(self.vue.select_mur)
        self.manche.setAfficheSelectDirPouvoir(self.vue.select_dir_pouvoir)

    #Boucle menu
    def menu (self):
        choix = self.vue.mode_jeux()
        if choix == 1 :
            self.manche.jeu_deux_robots()
        if choix == 2:
            self.manche.jeu_deux_players()
        else :
            return 0



class presenteur_vue_graphique :
    def __init__(self,jeu,vue_graphique):
        self.vue = vue_graphique
        self.manche = jeu
        self.client = Client()
        self.manche.setAffichagePLa(self.vue.mettre_a_jour_plateau)
        self.manche.setAffichageResultat(self.vue.afficher_resultat)
        self.manche.setAfficheChoixMur(self.vue.choix_mur)
        self.manche.setAfficheChoixPion(self.vue.choix_pion)
        self.manche.setAfficheGetUserInput(self.vue.get_user_input)
        self.manche.setAfficheSelectMur(self.vue.select_mur)
        self.manche.setAfficheSelectDirPouvoir(self.vue.select_dir_pouvoir)

    #Boucle menu
    def menu (self):
        choix=None

        while choix==None:

            choix = self.vue.choix_mode
        if choix == 1 :
            self.vue.afficher_fenetre_jeu()
            self.vue.afficher_plateau()
            self.manche.jeu_deux_robots()

        if choix == 2:
            self.vue.afficher_fenetre_jeu()
            self.vue.afficher_plateau()
            self.manche.jeu_deux_players()
        else :
            return 0
