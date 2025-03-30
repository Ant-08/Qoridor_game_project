#Classe pour afficher dans la console
from colorama import Fore, Style

class vue :
    def __init__(self):
        pass



    #Pour choisir le mode de jeu (par exemple, 1 joueur, 2 joueurs, robot1...)
    def mode_jeux (self):
        print("Entrez 1 pour lancer deux robots aléatoire, 2 pour lancer le mode 1v1 et 3 pour quitter le programme ")
        choix = int(input("Quel mode de jeux souhaitez-vous ?  "))
        return choix
    #choix du type de pion dans la console
    def choix_pion (self,i):
        if i==0:
            print("Vous avez le choix entre trois types de pions")
        else:
            print("Joueur",i,"Vous avez le choix entre trois types de pions")
        print("Le pion sapeur. Unité qui casse un mur au contact. Entrez 0")
        print("Le pion jumper. Unité qui peut sauter un mur. Entrz 1")
        print("Le pion sprinter. Unité qui peut avancer de deux cases. Entrez 2")
        choix = int(input("Quel pion choisissez vous ?  "))
        return choix
    #Choix des murs
    def choix_mur (self,nb):
        if nb==0:
            print("Vous avez le choix entre cinq types de murs : ")
        else:
            print("Joueur",nb,"Vous avez le choix entre cinq types de murs : ")
        print("Vous avez 15 crédits pour choisir les murs que vous souhaitez")
        print(" - WallSolide. Mur incassable. Cout 2.")
        print(" - WallLong. Mur de longueur 4. Cout 2.")
        print(" - WallReusable. Mur réutilisable (pick and redeploy). Cout 2.")
        print(" - WallDoor. Mur // porte. Cout 2.")
        choix = []
        choix.append(int(input("Combien souhaitez vous de WallSolide : ")))
        choix.append(int(input("Combien souhaitez vous de WallLong : ")))
        choix.append(int(input("Combien souhaitez vous de WallReusable : ")))
        choix.append(int(input("Combien souhaitez vous de WallDoor : ")))
        return choix
    #Affiche le plateau dans la console
    def afficher_plateau(self,plateau,cpt,truc,machin,chouette,bidule,chose,nianiania):
        self.tour=cpt
        for i in range(len(plateau)):
            affichage = ""
            for j in range(len(plateau[i])):
                if str(plateau[i][j]) == "0":
                    affichage = affichage + f"{Fore.RED}X{Style.RESET_ALL}"
                elif str(plateau[i][j]) == "1":
                    affichage = affichage + f"{Fore.BLUE}X{Style.RESET_ALL}"
                elif str(plateau[i][j]) == "2":
                    affichage = affichage + f"{Fore.GREEN}X{Style.RESET_ALL}"
                elif str(plateau[i][j]) == "3":
                    affichage = affichage + f"{Fore.YELLOW}X{Style.RESET_ALL}"
                elif str(plateau[i][j]) == "4":
                    affichage = affichage + f"{Fore.MAGENTA}X{Style.RESET_ALL}"
                elif str(plateau[i][j]) == " ":
                    affichage = affichage + f"{Fore.BLACK}+{Style.RESET_ALL}"
                elif str(plateau[i][j]) == "i":
                    affichage = affichage + f"{Fore.CYAN}A{Style.RESET_ALL}"
                elif str(plateau[i][j]) == "j":
                    affichage = affichage + f"{Fore.CYAN}B{Style.RESET_ALL}"
                else:
                    affichage = affichage + str(plateau[i][j])
            print(affichage)
        print("-------")

    #Affiche le resultat de la partie dans la console
    def afficher_resultat(self,joueur):
        joueur = str(joueur)
        print(joueur + " a gagné !!")
        print("Fin de partie")

    def get_user_input(self, cpt):
        while True:
            if cpt>=5:
                print("Vous pouvez utiliser votre pouvoir")
            else:
                print("Il vous reste",5-cpt,"tours avant de pouvoir utiliser votre pouvoir")
            user_input = input(f"Joueur {self.tour}, entrez 'up', 'down', 'left', 'right' pour déplacer votre pion, \n un centre (x,y) suivit de sa direction (n,s,e,w) pour placer un mur ou 'pouvoir' pour utiliser le pouvoir de votre pion: ")
            if user_input in ['up', 'down', 'left', 'right','pouvoir'] or (user_input.endswith("n") or user_input.endswith("s") or user_input.endswith("e") or user_input.endswith("w")) and len(user_input) <=6:
                return user_input
            else:
                print("Invalid input. Please enter a valid move or wall placement.")

    def select_mur(self,murs):

        print("Quels mur voulez-vous jouer")
        print(" - WallCLassique. Mur classique. Vous en avez encore ",murs.count(0),". Entrez 0")
        print(" - WallSolide. Mur incassable. Vous en avez encore ",murs.count(1),". Entrez 1")
        print(" - WallLong. Mur de longueur 4. Vous en avez encore ",murs.count(2),". Entrez 2")
        print(" - WallReusable. Mur réutilisable (pick and redeploy). Vous en avez encore ",murs.count(3),". Entrez 3")
        print(" - WallDoor. Mur // porte. Vous en avez encore ",murs.count(4),". Entrez 4")
        user_input=input("Votre choix : ")
        return(user_input)

    def select_dir_pouvoir(self):
        user_input2 = input(f"Dans quelle direction (haut,bas,droite,gauche) souhaitez vous utiliser votre pouvoir ? ")
        return user_input2

