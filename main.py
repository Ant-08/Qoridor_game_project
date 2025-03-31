from modele import *
from presenteur import *
from vue import *

def main1():
    partie = jeu()
    view = vue_console()
    presenteur = presenteur_vue_console(partie,view)
    presenteur.menu()

main1()
