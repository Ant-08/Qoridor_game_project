import typing
from typing import List
import time
import numpy as np

# taille de la carte
tailleMap = 11
matriceVide = np.zeros((tailleMap*2-1, tailleMap*2-1))
# Argent de début pour acheter murs
nbrPointAchatMur = 15
#couple type de mur et cout de ce mur
murEtCout = {0:2,1:2,3:2,4:2}

# Classe qui va permettre la communication avec le serveur.
# Version non fonctionnelle du client, uniquement la pour que vous puissiez le prendre en considération
# pour permettre une transition plus facile au 2eme semestre.
class Client:

    # ------------------------------------------------------------------------
    # FONCTION UTILISEES AU DEBUT DU JEU
    # -----------------------------------------------------------------------

    # enregistre l'équipe auprès du serveur, avec un nom d'équipe et un type de pion
    # type de pion 0:pionSappeur, 1:pion Jumper, 2:pion sprinter
    def registerTeam(self, name:str, pionChoisi:int):
        return True

    # choisi un ensemble de mur pour commencer la partie
    # error 0:trop cher en point
    # Version locale de ce qui se fera sur le serveur
    def choixMur(self, murs:List[int]):
        totalCout = 0
        try :
            for mur in murs :
                totalCout += murEtCout.get(mur)
        except ValueError:
            print("mur n'existe pas dans la liste des murs dispos")

        return True



    # ------------------------------------------------------------------------
    # FONCTION UTILISEES PENDANT LE JEU
    # ------------------------------------------------------------------------

    # Fonction à appeler dans une boucle While, qui est bloquante. C'est a dire que la fonction est en
    # "pause" tant que l'autre joueur est en train de jouer
    def askPriority(self):
        # Temps d'attente en seconde
        time.sleep(2)
        # Renvoi une matrice contenant les cases du jeu.
        return matriceVide




    # return 0 si s'est bien passé
    # Code erreur  1:, 2:obstacle mur, 3:sortie de terrain, 10:mauvais input
    def deplacement(self, joueur: str, positionX:int, positionY:int):
        if not isinstance(joueur, str) or not isinstance(positionX, int) or not isinstance(positionY, int):
            raise TypeError()
        return 0

    # Orientation : 0 : vers le haut, 1 vers la droite, 2 vers le bas, 3 vers la gauche
    # type mur : 0:mur incassable 1:mur long 2:mur réutilisable 3:murTemporaire 4:mur "porte"
    # return 0 si ok
    # Code erreur : 1:mur sort map, 2:mur croise autre mur, 3:mur enferme joueur 4:mur non disponible 10:mauvais input
    def placementMur(self, joueur : str, typeMur:int , positionX:int, positionY:int, orientation: int):
        if not isinstance(joueur, str) or not isinstance(typeMur, int) or not isinstance(positionX, int) or not isinstance(positionY, int) or not isinstance(orientation, int):
            raise TypeError()
        return 0

    # utilisation du pouvoir de l'unité
    # Sauter par dessus
    # return 0 si ok
    # code erreur 1:pouvoir en rechargement  10:mauvais input
    def utilisationPouvoir(self, orientation):
        if isinstance(orientation, int):
            raise TypeError()
        return 0
