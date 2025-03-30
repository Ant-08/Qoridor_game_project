from abc import ABC, abstractmethod
from random import randint,choice
from ClientFake import Client
import copy
import time
from functools import *

#######################################################################################################################
#######################################################################################################################
#Classe jeu contient les méthodes pour jouer une partie
class jeu :
    #Initialisation de la classe
    def __init__(self,taille=11):
        self.taille = taille*2-1
        self.plateau = [['O' if (c %2==0 and l%2==0) else ' ' for c in range(taille*2-1)]  for l in range(taille*2-1)]
        self.joueur = None
        self.adversaire = None
        self.serveur = Client()
        self.mur_totaux = []

########################################################################
# Méthode de jeu:
# ----------------
    #Verification du choix des murs
    def choix_mmur(self,choix_mur,nb):
        murs=[]
        for i in range(len(choix_mur)):
            for j in range(choix_mur[i]):
                murs.append(i)
        if (len(murs))>7 :
            return False
        if nb!=2:
            res_serv = True#self.serveur.choixMur(murs)
            if res_serv == True :
                for i in range(len(choix_mur)):
                    for j in range(choix_mur[i]):
                        if i == 0:
                            self.joueur.mur_restant.append(WallClassique((0,0),0))
                        elif i==1:
                            self.joueur.mur_restant.append(WallSolide((0,0),0))
                        elif i == 2:
                            self.joueur.mur_restant.append(WallLong((0,0),0))
                        elif i == 3:
                            self.joueur.mur_restant.append(WallDoor((0,0),0))
                        elif i == 4:
                            self.joueur.mur_restant.append(WallTemporary((0, 0), 0))
                return True
        if nb==2:
            res_serv = True  # self.serveur.choixMur(murs)
            if res_serv == True:
                for i in range(len(choix_mur)):
                    for j in range(choix_mur[i]):
                        if i == 0:
                            self.adversaire.mur_restant.append(WallClassique((0,0),0))
                        elif i==1:
                            self.adversaire.mur_restant.append(WallSolide((0,0),0))
                        elif i == 2:
                            self.adversaire.mur_restant.append(WallLong((0,0),0))
                        elif i == 3:
                            self.adversaire.mur_restant.append(WallDoor((0,0),0))
                        elif i == 4:
                            self.adversaire.mur_restant.append(WallTemporary((0, 0), 0))
                return True
    #Initialisation d'une partie, choix du type de pion et placement
    def init_partie(self,nb,joueur,adversaire):
        self.plateau = [["O" if (c % 2 == 0 and l % 2 == 0) else ' ' for c in range(self.taille)] for l in
                        range(self.taille)]
        if nb==0: #[choice([WallLong([0,0],0), WallSolide([0,0],0), WallTemporary([0,0],0), WallDoor([0,0],0)]) for i in range (7)]
            self.joueur = joueur
            self.adversaire = adversaire
            self.joueur.mur_restant= [choice([WallClassique([0,0],0),WallLong([0,0],0), WallSolide([0,0],0), WallTemporary([0,0],0), WallDoor([0,0],0)]) for i in range (7)]
            self.adversaire.mur_restant = [choice([WallClassique([0,0],0),WallLong([0,0],0), WallSolide([0,0],0), WallTemporary([0,0],0), WallDoor([0,0],0)]) for i in range (7)]
        self.deplacer_joueur(self.joueur.coord,(self.taille-1,self.taille//2),True)
        self.deplacer_joueur(self.adversaire.coord,(0,self.taille//2),False)

    #Méthode pour deplacer un pion sur une case du plateau
    def deplacer_joueur (self,coor,new_coor,us):
        if us :
            val = "i"
            joueur = self.joueur
        else :
            val = 'j'
            joueur = self.adversaire
        if 0 <= new_coor[0]  < self.taille and 0 <= new_coor[1] < self.taille:########################################################################################
            self.plateau[coor[0]][coor[1]] = 'O'
            self.plateau[new_coor[0]][new_coor[1]] = val
            joueur.coord = list(new_coor)

    #Méthode pour faire avancer un pion avec respect des regles
    def avancer_joueur (self,new_coor,us):
        jump=False
        new_coor2=(0,0)
        if us : #On récupère les coordonnées du joueur 1 et on verfie si les nouvelles coor sont diff de celles de l'adversaire
            joueur = self.joueur
            act_coor = self.joueur.coord
            if new_coor==(self.adversaire.coord[0],self.adversaire.coord[1]):
                jump=True
                new_coor2=(new_coor[0]+(new_coor[0]-act_coor[0]),new_coor[1]+(new_coor[1]-act_coor[1]))
        else : # Meme chose dans l'autre sens
            joueur = self.adversaire
            act_coor = self.adversaire.coord
            if new_coor==(self.joueur.coord[0],self.joueur.coord[1]):
                jump=True
                new_coor2=(new_coor[0]*2-act_coor[0],new_coor[1]*2-act_coor[1])
        #On regarde les cases voisines disponibles
        voisin = []
        for i,j in [(0,2),(2,0),(-2,0),(0,-2)] :
            if jump:
                voisin.append((int(act_coor[0]+(i*2)),int(act_coor[1]+(j*2))))
            else:
                voisin.append((int(act_coor[0]+i),int(act_coor[1]+j)))
        if new_coor in voisin or new_coor2 in voisin:
            if 0<= new_coor[0] < self.taille and 0<= new_coor[1] < self.taille:
               if self.plateau[int((act_coor[0]+new_coor[0])/2)][int((act_coor[1]+new_coor[1])/2)] == ' ':
                   if jump :
                       if self.plateau[int((new_coor[0]+new_coor2[0])/2)][int((new_coor[1]+new_coor2[1])/2)] == ' ':
                           self.deplacer_joueur(act_coor, new_coor2, us)
                   else :
                       self.deplacer_joueur(act_coor,new_coor,us)
               elif self.plateau[int((act_coor[0]+new_coor[0])/2)-1][int((act_coor[1]+new_coor[1])/2)-1] ==3:
                   mur = None
                   for i in self.mur_totaux :
                       if (int((act_coor[0]+new_coor[0])/2),int((act_coor[1]+new_coor[1])/2)) in i.coordonnes :
                           mur = i
                   if mur != None :
                       if mur.proprietaire == joueur:
                           self.deplacer_joueur(act_coor, new_coor, us)
                       else :
                           print("Pas propietaire de ce mur !")
               else :
                   print("Il y a un mur !")
            else :
                print("Nouvelles coordonnées en dehors du plateau")
        else :
            print("Les nouvelles coordonnées ne sont pas a cote de la position")

    #Méthode pour placer un mur sur le plateau
    def placer_mur (self,mur,plateau):
        if mur.direction == 0:#Nord
            if mur.centre[0] - (mur.longueur-1) >= 0:######################################################################""
                for i in range(mur.longueur):
                    if plateau[mur.centre[0]-i][mur.centre[1]] != ' ':
                        return 1
                for i in range(mur.longueur):
                    plateau[mur.centre[0]-i][mur.centre[1]] = mur.type
            else:
                return 2
        elif mur.direction == 1:#Est
            if mur.centre[1] + mur.longueur <= self.taille:
                for i in range(mur.longueur):
                    if plateau[mur.centre[0]][mur.centre[1] + i] != ' ':
                        return 1
                for i in range(mur.longueur):
                    plateau[mur.centre[0]][mur.centre[1]+i] = mur.type
            else:
                return 2
        elif mur.direction == 2:#Sud
            if mur.centre[0] + mur.longueur <= self.taille:
                for i in range(mur.longueur):
                    if plateau[mur.centre[0] + i][mur.centre[1]] != ' ':
                        return 1
                for i in range(mur.longueur):
                    plateau[mur.centre[0]+i][mur.centre[1]] = mur.type
            else:
                return 2
        elif mur.direction == 3:#Ouest
            if mur.centre[1] - (mur.longueur -1)>= 0:########################################################################################
                for i in range(mur.longueur):
                    if plateau[mur.centre[0]][mur.centre[1] - i] != ' ':
                        return 1
                for i in range(mur.longueur):
                    plateau[mur.centre[0]][mur.centre[1]-i] = mur.type
            else:
                return 2
        return plateau
    def enlever_mur (self,mur,plateau):
        for i in mur.coordonnes :
            plateau[i[0]][i[1]] = ' '

    #Méthode pour placer un mur avec respect des regles
    def poser_mur (self,joueur,mur):
        if joueur.credit_mur > 0:
            mur.changer_coor()
            plateau_test = copy.deepcopy(self.plateau)
            plateau = self.placer_mur(mur,plateau_test)
            if plateau == 1:
                print("Déja un mur")
            elif plateau==2:
                print("Hors plateau")
            else :
                resultat = self.recursion(plateau,self.joueur.coord,True)
                resultat2= self.recursion(plateau,self.adversaire.coord,False)
                if resultat == True and resultat2 ==True:
                    self.plateau = plateau.copy()
                    self.mur_totaux.append(mur)
                    mur.proprietaire = joueur
                    joueur.mur_restant.remove(mur)
                    if mur.type == 4 :
                        joueur.mur_temp.append(mur)
                    joueur.credit_mur = joueur.credit_mur - 1
                else :
                    print("Nouveau mur invalide, plus de chemin possible")
        else :
            print("Vous n'avez plus assez de mur")
    #Méthode pour verifier s'il reste un chemin
    #Fonctionne mais est tres lent si pas de solution et pas bcp bloqué
    #Piste d'amélioration vérifier en amont si le mur fait une ligne continue, si c'est pas le cas lancer le script chemin
    def recursion(self,plateau,pos,us):
        visite =set()
        visite.add((pos[0],pos[1]))
        return self.chemin_restant(plateau,pos,visite,us)
    #Méthode recursive pour verifier un chemin a partir d'un position donnée
    def chemin_restant (self,plateau,pos,visite,us):
        if us:
            arrivee = 0
        else:
            arrivee = self.taille-1
        if pos[0] == arrivee:
            return True
        voisin = set()
        for i, j in [(0,2),(2,0),(-2,0),(0,-2)] :
            if 0<= pos[0]+i < self.taille and 0<= j+pos[1] < self.taille :
                if (i !=0 and plateau[int(pos[0]+(i/2))][pos[1]] == ' ') or (j !=0 and plateau[pos[0]][int(pos[1]+(j/2))] == ' '):
                    voisin.add((pos[0]+i, j+pos[1]))
        dispo = voisin - visite
        if len(dispo)==0:
            return
        for new_pos in dispo :
                visite.add(new_pos)
                res = self.chemin_restant(plateau,new_pos,visite,us)
                if res == True:
                    return True
                visite.remove(new_pos)
    #Méthode qui verifie les conditions de gains
    def verifier_victoire (self):
        if self.joueur.coord[0] == 0:
            return 1
        elif self.adversaire.coord[0] == self.taille-1:
            return 2
        else :
            return 0

########################################################################
# Méthode pour lier le mdoèle au présenteur:
# ------------------------------------------

    def affichage_pla(self,plateau):
        pass
    def affichage_resultat(self,res):
        pass
    def affichage_choix_pion(self,i):
        pass
    def affichage_choix_mur(self,nb):
        pass
    def affichage_get_user_input(self,tour,partie):
        pass
    def affichage_select_mur(self,mur):
        pass
    def affichage_select_dir_pouvoir(self):
        pass
    def setAffichagePLa(self,function):
        self.affichage_pla = partial(function)
    def setAffichageResultat(self,function):
        self.affichage_resultat = partial(function)
    def setAfficheChoixPion(self,function):
        self.affichage_choix_pion = partial(function)
    def setAfficheChoixMur(self,function):
        self.affichage_choix_mur = partial(function)
    def setAfficheGetUserInput(self,function):
        self.affichage_get_user_input = partial(function)
    def setAfficheSelectMur(self,function):
        self.affichage_select_mur = partial(function)
    def setAfficheSelectDirPouvoir(self,function):
        self.affichage_select_dir_pouvoir = partial(function)


########################################################################
# Méthode avec les boucles de parties:
# ------------------------------------

    #Méthode qui effectue une action aleatoire pour un joueur donné
    def tour_aleatoire (self,joueur):
        if joueur == self.joueur :
            nous = True
            possibilites = [(0, 2), (2, 0), (-2, 0), (-2, 0), (-2, 0), (0, -2)]
        else :
            nous = False
            possibilites = [(0, 2), (2, 0), (2, 0), (2, 0), (-2, 0), (0, -2)]
        if joueur.cooldown > 5 :
            action = randint(1, 3)
        elif joueur.credit_mur > 2 :
            action = randint(1,2)
        else :
            action = 1
        if action == 1:
            voisin = []
            for i, j in possibilites:
                voisin.append((int(joueur.coord[0] + i), int(joueur.coord[1] + j)))
            case = choice(voisin)
            self.avancer_joueur(case,nous)
            joueur.cooldown +=1
        elif action == 2 :
            if joueur.mur_restant != [] :
                mur = choice(joueur.mur_restant)
                centres_possibles = []
                for i in range(1,self.taille):
                    if i %2 == 0:
                        for j in range (1,self.taille,2):
                            centres_possibles.append((i,j))
                    else:
                        for j in range (0,self.taille,2):
                            centres_possibles.append((i,j))
                            centres_possibles.append((i,j))

                            centres_possibles.append((i,j))
                            centres_possibles.append((i,j))
                mur.centre = choice(centres_possibles)
                direction_possible = [0,1,2,3]
                if mur.centre[0]%2==0 :
                    direction_possible.remove(1)
                    direction_possible.remove(3)
                else :
                    direction_possible.remove(0)
                    direction_possible.remove(2)
                mur.direction = choice(direction_possible)
                self.poser_mur(joueur,mur)
                joueur.cooldown +=1
        else :
            joueur.pouvoir(self,choice(['haut','bas','gauche','droite']),nous)
            joueur.cooldown += 1


    def jeu_deux_robots(self):
        #joueur = self.choix_ppion(1)
        self.init_partie(0,choice([pionJump(),pionSprinteur()]),choice([pionJump(),pionSprinteur()]))
        #self.client.registerTeam('stitch',joueur.type)
        #self.choix_pmur(0)
        joueur= self.joueur
        adver = self.adversaire
        tour = 1
        murs_restantsj1 = [self.joueur.mur_restant[i].type for i in range(len(self.joueur.mur_restant))]
        murs_restantsj2 = [self.adversaire.mur_restant[i].type for i in range(len(self.adversaire.mur_restant))]
        pion1 = self.joueur.type
        pion2 = self.adversaire.type
        cooldown1 = self.joueur.cooldown
        cooldown2 = self.adversaire.cooldown
        self.affichage_pla(self.plateau, tour, murs_restantsj1, murs_restantsj2, pion1, pion2,cooldown1,cooldown2)
        continuer = True
        while continuer :
            time.sleep(0.05)
            if len(joueur.mur_temp) > 0:
                for i in joueur.mur_temp:
                    i.timer = i.timer - 1
                    if i.timer == 0:
                        self.enlever_mur(i, self.plateau)
                        joueur.mur_temp.remove(i)
            if len(adver.mur_temp) > 0:
                for i in adver.mur_temp:
                    i.timer = i.timer - 1
                    if i.timer == 0:
                        self.enlever_mur(i, self.plateau)
                        adver.mur_temp.remove(i)
            if tour == 1:
                self.tour_aleatoire(joueur)
            elif tour == 2:
                self.tour_aleatoire(adver)
            #self.client.askPriority()
            plateau = self.plateau
            murs_restantsj1=[self.joueur.mur_restant[i].type for i in range(len(self.joueur.mur_restant))]
            murs_restantsj2=[self.adversaire.mur_restant[i].type for i in range(len(self.adversaire.mur_restant))]
            cooldown1 = self.joueur.cooldown
            cooldown2 = self.adversaire.cooldown
            self.affichage_pla(plateau, tour, murs_restantsj1, murs_restantsj2,pion1,pion2,cooldown1,cooldown2)
            res = self.verifier_victoire()
            if res == 1:
                continuer = False
                self.affichage_pla(self.plateau, tour, murs_restantsj1, murs_restantsj2, pion1, pion2,cooldown1,cooldown2)
                self.affichage_resultat("Le joueur")
            elif res == 2:
                continuer = False
                self.affichage_pla(self.plateau, tour, murs_restantsj1, murs_restantsj2, pion1, pion2,cooldown1,cooldown2)
                self.affichage_resultat("L'adversaire")
            tour = tour % 2 + 1
        time.sleep(30)

    def choix_ppion_pmur (self,i):
        pion = self.affichage_choix_pion(i)
        if i==1:
            if pion == 0:
                self.joueur= pionSapeur()
            elif pion == 1:
                self.joueur= pionJump()
            elif pion == 2:
                self.joueur = pionSprinteur()
        else :
            if pion == 0:
                self.adversaire= pionSapeur()
            elif pion == 1:
                self.adversaire= pionJump()
            elif pion == 2:
                self.adversaire = pionSprinteur()
        faire_choix = True
        while faire_choix:
            mur = self.affichage_choix_mur(i)
            res = self.choix_mmur(mur, i)
            if res == True:
                faire_choix = False
            else:
                print("Il y a une erreur")


    def jeu_deux_players(self):
        #joueur1=self.choix_ppion_pmur(1)
        #joueur2=self.choix_ppion_pmur(2)
        #self.init_partie(1)
        self.init_partie(0,choice([pionSapeur(),pionSprinteur(),pionJump()]),choice([pionSapeur(),pionSprinteur(),pionJump()]))
        joueur1=self.joueur
        joueur2=self.adversaire
        continuer = True
        tour = 1
        while continuer:
            plateau = self.plateau
            murs_restantsj1 = [self.joueur.mur_restant[i].type for i in range(len(self.joueur.mur_restant))]
            murs_restantsj2 = [self.adversaire.mur_restant[i].type for i in range(len(self.adversaire.mur_restant))]
            pion1=self.joueur.type
            pion2=self.adversaire.type
            cooldown1=self.joueur.cooldown
            cooldown2=self.adversaire.cooldown
            self.affichage_pla(plateau, tour, murs_restantsj1, murs_restantsj2,pion1,pion2,cooldown1,cooldown2)
            if tour == 1:
                player_input = self.affichage_get_user_input(self.joueur.cooldown)
                self.tour_1v1(joueur1,player_input)
                self.joueur.cooldown = self.joueur.cooldown+1
            elif tour==2:
                player_input = self.affichage_get_user_input(self.adversaire.cooldown)
                self.tour_1v1(joueur2,player_input)
                self.adversaire.cooldown = self.adversaire.cooldown+1
            res = self.verifier_victoire()
            if res == 1:
                continuer = False
                self.affichage_pla(plateau, tour, murs_restantsj1, murs_restantsj2, pion1, pion2,cooldown1,cooldown2)
                self.affichage_resultat("Le joueur")
            elif res == 2:
                continuer = False
                self.affichage_pla(plateau, tour, murs_restantsj1, murs_restantsj2, pion1, pion2,cooldown1,cooldown2)
                self.affichage_resultat("L'adversaire")
            tour = tour % 2 + 1
        time.sleep(30)


    def tour_1v1(self,joueur,player_input):
        if joueur == self.joueur :
            nous = True
        else :
            nous = False
        if player_input in ['up', 'down', 'left', 'right']:
            new_coord=()
            if nous:
                if player_input == "up":
                    new_coord = ((int(self.joueur.coord[0] + -2), int(self.joueur.coord[1] + 0)))
                elif player_input == "down":
                    new_coord = ((int(self.joueur.coord[0] + 2), int(self.joueur.coord[1] + 0)))
                elif player_input == "left":
                    new_coord = ((int(self.joueur.coord[0] + 0), int(self.joueur.coord[1] + -2)))
                elif player_input == "right":
                    new_coord = ((int(self.joueur.coord[0] + 0), int(self.joueur.coord[1] + 2)))
            else:
                if player_input == "up":
                    new_coord = ((int(self.adversaire.coord[0] + -2), int(self.adversaire.coord[1] + 0)))
                elif player_input == "down":
                    new_coord = ((int(self.adversaire.coord[0] + 2), int(self.adversaire.coord[1] + 0)))
                elif player_input == "left":
                    new_coord = ((int(self.adversaire.coord[0] + 0), int(self.adversaire.coord[1] + -2)))
                elif player_input == "right":
                    new_coord = ((int(self.adversaire.coord[0] + 0), int(self.adversaire.coord[1] + 2)))
            self.avancer_joueur(new_coord, nous)
        elif player_input.endswith("n") or player_input.endswith("s") or player_input.endswith("e") or player_input.endswith("w"):
            murs = []
            for i in joueur.mur_restant:
                murs.append(i.type)
            mur_choisi = self.affichage_select_mur(murs)
            mur=None
            for j in joueur.mur_restant:
                if j.type == int(mur_choisi):
                    mur = j
            centre = player_input.split(",")
            x = centre[0]
            y = centre[1][:-1]
            mur.centre = (int(x), int(y))
            a = player_input[-1:]
            if a=='n':#################################################################################
                mur.direction=0
            elif a=='e':
                mur.direction=1
            elif a == 's':
                mur.direction = 2
            elif a == 'w':
                mur.direction = 3
            self.poser_mur(joueur, mur)

        elif player_input == "pouvoir" :
            input=self.affichage_select_dir_pouvoir()
            if nous:
                self.joueur.pouvoir(self,input,nous)
            else:
                self.adversaire.pouvoir(self,input,nous)

    def IA_1 (self):
        pass
#######################################################################################################################
#######################################################################################################################
#Classe abstraites des pions
class pion_mere (ABC):
    #Cette classe est la classe mère des différents pion
    #Un pion doit avoir la méthode de déplacement, la méthode du pouvoir, la méthode de d'affichage...
    @abstractmethod
    def __init__(self):
        self.coord = [0,0]
        self.credit_mur = 17
        self.mur_restant = []
        self.mur_temp = []
        self.cooldown = 5
    #Méthode abstraites pour utiliser un pouvoir (defini pour chaque pion)
    @abstractmethod
    def pouvoir (self):
        pass

#Classe du pion sapeur
class pionSapeur (pion_mere):
    def __init__(self):
        pion_mere.__init__(self)
        self.nom = 'PionSapeur'
        self.type = 0
    #Méthode pour enlever un mur
    def pouvoir (self,jeu,direction,us):
        mur = None
        if direction == 'haut' :
            for i in jeu.mur_totaux :
                if (self.coord[0]-1,self.coord[1]) in i.coordonnes :
                    mur = i
        elif direction == 'droite' :
            for i in jeu.mur_totaux :
                if (self.coord[0],self.coord[1]+1) in i.coordonnes :
                    mur = i
        elif direction == 'gauche' :
            for i in jeu.mur_totaux :
                if (self.coord[0],self.coord[1]-1) in i.coordonnes :
                    mur = i
        elif direction == 'bas' :
            for i in jeu.mur_totaux :
                if (self.coord[0]+1,self.coord[1]) in i.coordonnes :
                    mur = i
        if mur != None :
            if mur.type == 1 :
                print("Mur incassable")
            else :
                jeu.mur_totaux.remove(mur)
                jeu.enlever_mur(mur,jeu.plateau)
                self.cooldown = -1



#Classe du pion sprinteur
class pionSprinteur (pion_mere):
    def __init__(self):
        pion_mere.__init__(self)
        self.nom = 'PionSprinteur'
        self.type = 2
    def pouvoir (self,jeu,direction,us):
        for i in range (2):
            if direction == 'haut':
                jeu.avancer_joueur((self.coord[0]-2,self.coord[1]),us)
            elif direction == 'bas':
                jeu.avancer_joueur((self.coord[0] +2, self.coord[1]), us)
            elif direction == 'gauche':
                jeu.avancer_joueur((self.coord[0], self.coord[1]-2), us)
            elif direction == 'droite':
                jeu.avancer_joueur((self.coord[0], self.coord[1]+2), us)
        self.cooldown = -1


#Classe du pion jumper
class pionJump (pion_mere):
    def __init__(self):
        pion_mere.__init__(self)
        self.nom = 'PionJump'
        self.type = 1
    def pouvoir (self,jeu,direction,us):
        if direction == 'haut':
            jeu.deplacer_joueur(self.coord,(self.coord[0] - 2, self.coord[1]), us)
        elif direction == 'bas':
            jeu.deplacer_joueur(self.coord,(self.coord[0] + 2, self.coord[1]), us)
        elif direction == 'gauche':
            jeu.deplacer_joueur(self.coord,(self.coord[0], self.coord[1] - 2), us)
        elif direction == 'droite':
            jeu.deplacer_joueur(self.coord,(self.coord[0], self.coord[1] + 2), us)
        self.cooldown = -1

#######################################################################################################################
#######################################################################################################################
#Classe abstraite des murs
class mur_mere (ABC):
    @abstractmethod
    def __init__(self,centre,direction):
        self.centre = centre
        self.direction = direction #('n=0,e=1,s=2,w=3')
        self.coordonnes = []
        self.longueur = 2+1
        self.type = None
        self.proprietaire = None
        self.cout = 1

    def changer_coor (self):
        self.coordonnes=[]
        if self.direction ==0:
            for i in range (self.longueur):
                self.coordonnes.append((self.centre[0]-i,self.centre[1]))
        elif self.direction ==1:
            for i in range (self.longueur):
                self.coordonnes.append((self.centre[0],self.centre[1]+i))
        elif self.direction ==3:
            for i in range (self.longueur):
                self.coordonnes.append((self.centre[0],self.centre[1]-i))
        elif self.direction ==2:
            for i in range (self.longueur):
                self.coordonnes.append((self.centre[0]+i,self.centre[1]))

#Mur classique
class WallClassique (mur_mere):
    def __init__(self,centre,direction):
        mur_mere.__init__(self,centre,direction)
        self.type = 0

#Mur incassable
class WallSolide (mur_mere):
    def __init__(self,centre,direction):
        mur_mere.__init__(self,centre,direction)
        self.type = 1
        self.cout = 2

#Mur long
class WallLong (mur_mere):
    def __init__(self,centre,direction):
        mur_mere.__init__(self,centre,direction)
        self.longueur=7
        self.type = 2
        self.cout = 3

#Mur porte
class WallDoor (mur_mere):
    def __init__(self,centre,direction):
        mur_mere.__init__(self,centre,direction)
        self.type = 3
        self.cout = 3

#Mur temporaire
class WallTemporary (mur_mere):
    def __init__(self,centre,direction):
        mur_mere.__init__(self,centre,direction)
        self.type = 4
        self.timer=6
        self.cout = 1

#######################################################################################################################
#######################################################################################################################