from abc import ABC, abstractmethod
from random import randint,choice
from ClientFake import Client
import copy

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
                            self.joueur.mur_restant.append(WallSolide((0,0),'n',2))
                        elif i==1:
                            self.joueur.mur_restant.append(WallLong((0,0),'n',4))
                        elif i == 2:
                            self.joueur.mur_restant.append(WallReusable((0,0),'n',2))
                        elif i == 3:
                            self.joueur.mur_restant.append(WallDoor((0,0),'n',2))
                return True
        if nb==2:
            res_serv = True  # self.serveur.choixMur(murs)
            if res_serv == True:
                for i in range(len(choix_mur)):
                    for j in range(choix_mur[i]):
                        if i == 0:
                            self.adversaire.mur_restant.append(WallSolide((0, 0), 'n', 2))
                        elif i == 1:
                            self.adversaire.mur_restant.append(WallLong((0, 0), 'n', 4))
                        elif i == 2:
                            self.adversaire.mur_restant.append(WallReusable((0, 0), 'n', 2))
                        elif i == 3:
                            self.adversaire.mur_restant.append(WallDoor((0, 0), 'n', 2))
                return True
    #Initialisation d'une partie, choix du type de pion et placement
    def init_partie(self,joueur,adversaire,nb):
        self.plateau = [["O" if (c % 2 == 0 and l % 2 == 0) else ' ' for c in range(self.taille)] for l in
                        range(self.taille)]
        #Association de chaque joueur a son pion
        self.joueur = joueur
        self.adversaire = adversaire
        if nb==0:
            self.joueur.mur_restant= [choice([WallLong([0,0],'n',4), WallSolide([0,0],"n",2), WallReusable([0,0],"n",2), WallDoor([0,0],"n",2)]) for i in range (7)]
            self.adversaire.mur_restant = [choice([WallLong([0,0],'n',4), WallSolide([0,0],"n",2), WallReusable([0,0],"n",2), WallDoor([0,0],"n",2)]) for i in range (7)]
        #Placement des deux pions !!!!!! Probleme si plateau de taille paire a changer
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
        if 0 <= new_coor[0]  < self.taille and 0 <= new_coor[1] < self.taille - 1:
            self.plateau[coor[0]][coor[1]] = 'O'
            self.plateau[new_coor[0]][new_coor[1]] = val
            joueur.coord = list(new_coor)

    #Méthode pour faire avancer un pion avec respect des regles
    def avancer_joueur (self,new_coor,us): #Faire le cas pour sauter l'adversaire
        jump=False
        if us :
            joueur = self.joueur
            act_coor = self.joueur.coord
            if new_coor==(self.adversaire.coord[0],self.adversaire.coord[1]):
                jump=True
                new_coor=(new_coor[0]*2-act_coor[0],new_coor[1]*2-act_coor[1])
        else :
            joueur = self.adversaire
            act_coor = self.adversaire.coord
            if new_coor==(self.joueur.coord[0],self.joueur.coord[1]):
                jump=True
                new_coor=(new_coor[0]*2-act_coor[0],new_coor[1]*2-act_coor[1])
        voisin = []
        for i,j in [(0,2),(2,0),(-2,0),(0,-2)] :
            if jump:
                voisin.append((int(act_coor[0]+(i*2)),int(act_coor[1]+(j*2))))
            else:
                voisin.append((int(act_coor[0]+i),int(act_coor[1]+j)))
        if new_coor in voisin :
            if 0<= new_coor[0]+i < self.taille and 0<= j+new_coor[1] < self.taille-1:
               if self.plateau[int((act_coor[0]+new_coor[0])/2)-1][int((act_coor[1]+new_coor[1])/2)-1] not in [0,1,2]:
                   self.deplacer_joueur(act_coor,new_coor,us)
               if self.plateau[int((act_coor[0]+new_coor[0])/2)-1][int((act_coor[1]+new_coor[1])/2)-1] ==2:
                   mur = None
                   for i in self.mur_totaux :
                       if (int((act_coor[0]+new_coor[0])/2),int((act_coor[1]+new_coor[1])/2)) in i.coordonnes :
                           mur = i
                   if mur != None :
                       if mur.proprietaire == joueur:
                           self.deplacer_joueur(act_coor, new_coor, us)
                       else :
                           print("Il y a un mur !")
               else :
                   print("Il y a un mur !")
            else :
                print("Nouvelles coordonnées en dehors du plateau")
        else :
            print("Les nouvelles coordonnées ne sont pas a cote de la position")

    #Méthode pour placer un mur sur le plateau
    def placer_mur (self,mur,plateau):
        if mur.direction == 'n':
            if mur.centre[0] - mur.longueur + 1 >= 0:
                for i in range(mur.longueur):
                    plateau[mur.centre[0]-i][mur.centre[1]] = mur.type
        elif mur.direction == 'e':
            if mur.centre[1] + mur.longueur <= self.taille:
                for i in range(mur.longueur):
                    plateau[mur.centre[0]][mur.centre[1]+i] = mur.type
        elif mur.direction == 's':
            if mur.centre[0] + mur.longueur <= self.taille:
                for i in range(mur.longueur):
                    plateau[mur.centre[0]+i][mur.centre[1]] = mur.type
        elif mur.direction == 'w':
            if mur.centre[1] - mur.longueur + 1 >= 0:
                for i in range(mur.longueur):
                    plateau[mur.centre[0]][mur.centre[1]-i] = mur.type
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
            resultat = self.recursion(plateau,self.joueur.coord,True)
            resultat2= self.recursion(plateau,self.adversaire.coord,False)
            if resultat == True and resultat2 ==True:
                self.plateau = plateau.copy()
                self.mur_totaux.append(mur)
                mur.proprietaire = joueur
                joueur.mur_restant.remove(mur)
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
                """
                print(pos[0],pos[1])
                print(int(pos[0]+(i/2)),pos[1],pos[0],int(pos[1]+(j/2)))
                print(plateau[int(pos[0]+(i/2))][pos[1]],plateau[pos[0]][int(pos[1]+(j/2))])"""
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
    #Méthode qui effectue une action aleatoire pour un joueur donné
    def tour_aleatoire (self,joueur):
        if joueur == self.joueur :
            nous = True
        else :
            nous = False
        if joueur.cooldown > 5 :
            action = randint(1, 3)
        elif joueur.credit_mur > 2 :
            action = randint(1,2)
        else :
            action = 1
        if action == 1:
            voisin = []
            for i, j in [(0, 2), (2, 0), (-2, 0), (0, -2)]:
                voisin.append((int(joueur.coord[0] + i), int(joueur.coord[1] + j)))
            case = choice(voisin)
            self.avancer_joueur(case,nous)
            joueur.cooldown +=1
        elif action == 2 :
            if joueur.mur_restant != [] :
                mur = choice(joueur.mur_restant)
                centres_possibles = []
                for i in range(1,self.taille,2):
                    for j in range (1,self.taille,2):
                        centres_possibles.append((i,j))
                mur.centre = choice(centres_possibles)
                mur.direction = choice(["n","e","s","w"])
                self.poser_mur(joueur,mur)
                joueur.cooldown +=1
        else :
            joueur.pouvoir(self,choice(['haut','bas','gauche','droite']),nous)
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
        self.credit_mur = 7
        self.mur_restant = []
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
            if mur.type == 0 :
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
    def __init__(self,centre,direction,longueur):
        self.centre = centre
        self.direction = direction #('n,e,s,w')
        self.coordonnes = []
        self.longueur = longueur*2
        self.type = None
        self.proprietaire = None
        self.cout = 2
    def changer_coor (self):
        if self.direction =='n':
            for i in range (self.longueur):
                self.coordonnes.append((self.centre[0]-i,self.centre[1]))
        elif self.direction =='e':
            for i in range (self.longueur):
                self.coordonnes.append((self.centre[0],self.centre[1]+i))
        elif self.direction =='w':
            for i in range (self.longueur):
                self.coordonnes.append((self.centre[0],self.centre[1]-i))
        elif self.direction =='s':
            for i in range (self.longueur):
                self.coordonnes.append((self.centre[0]+i,self.centre[1]))

#Mur incassable
class WallSolide (mur_mere):
    def __init__(self,centre,direction,longueur):
        mur_mere.__init__(self,centre,direction,longueur)
        self.type = 0

#Mur classique
class WallLong (mur_mere):
    def __init__(self,centre,direction,longueur):
        mur_mere.__init__(self,centre,direction,longueur)
        self.type = 1

#Mur reutlisable
class WallReusable (mur_mere):
    def __init__(self,centre,direction,longueur):
        mur_mere.__init__(self,centre,direction,longueur)
        self.type = 2
    def pick_redeploy (self,jeu):
        jeu.enlever_mur(self,jeu)
        jeu.poser_mur()
#Mur porte
class WallDoor (mur_mere):
    def __init__(self,centre,direction,longueur):
        mur_mere.__init__(self,centre,direction,longueur)
        self.type = 3
