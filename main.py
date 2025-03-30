from modele import *
from presenteur import *
from vue_graphique import *
from vue import *

def main1():
    partie = jeu()
    view = vue_graphique()
    presenteur = presenteur_vue_graphique(partie,view)
    presenteur.menu()


main1()
