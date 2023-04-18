import random
import tkinter
from time import sleep

#Projet par Tom DARQUES et Marina FLAMENT

class Monde:
    """
    Classe qui gère la création du Monde et des individus de la simulation
    """
    def __init__(self, longueur = 40, largeur = 30, densite = 25, confinement = 0):
        """
        Constructeur de la classe Monde
        """
        self.longueur = longueur
        self.largeur = largeur
        self.duree_cycle = 250
        self.temps = 0
        self.densite = densite #en %
        self.nbr_contamines = 0
        self.nbr_decedes = 0
        self.confinement = confinement
        liste_confinement = ["Aucun confinement", "Confinement limité", "Confinement strict"]
        self.etat_confinement = liste_confinement[confinement]
        self.liste_positions = []
        self.liste_personnes = []
        self.nbr_personnes = 0
        self.contamines_initial = 1
        
        self.M = []
        for y in range(largeur):
            self.M.append([])
            for x in range(longueur):
                self.M[y].append([])
                
    def nombre_personnes(self):
        """
        Méthode qui calcule le nombre de personnes
        """
        self.nbr_personnes = round(self.largeur*self.longueur * self.densite / 100)
        
    def determiner_contamines_initial(self):
        """
        Méthode qui calcule le nombre de contaminés au début de la simulation
        """
        for i in range(self.contamines_initial):
            personne = random.choice(self.liste_personnes)
            while personne.etat_contamination == 1:
                personne = random.choice(self.liste_personnes)
            personne.etat_contamination = 1

            
    def attribuer_positions(self):
        """
        Méthode qui attribue une position unique à chaque personne
        """
        for i in range(self.nbr_personnes):
            position = [random.choice([i for i in range(1,self.longueur+1)]), random.choice([i for i in range(1,self.largeur+1)])]
            while position in self.liste_positions:
                position = [random.choice([i for i in range(1,self.longueur+1)]), random.choice([i for i in range(1,self.largeur+1)])]
            self.liste_positions.append(position)

        for position in self.liste_positions:
            self.liste_personnes.append(Personne(self.longueur, self.largeur, position[0],position[1]))
            
    def attributer_identifiant(self):
        """
        Méthode qui attribue un chiffre unique à chaque personne ( utilisée pour faire des vérifications)
        """
        i = 1
        for personne in self.liste_personnes:
            personne.id = i
            i = i+1

    
                
class Personne:
    """
    Classe qui regroupe les caractéristiques d'une personne et qui gère son comportement
    """
    def __init__(self, longueur, largeur, x = None, y = None, immunite = False):
        """
        Constructeur de la classe Personne
        """
        self.x = x
        self.y = y
        self.etat_contamination = 0
        self.immunite = immunite
        self.contagiosite = 0
        self.derogation = False
        self.confinement = confinement
        self.longueur = longueur
        self.largeur = largeur
        self.porteur_sain = False
        self.duree_contamination = 0
        self.mort = False
        self.vaccination = None
        self.duree_vaccination = 0
        self.id = None
        self.deplacement = None
        
        p = random.randint(1,100)
        if 1 <= p <= 35: #35%
            etat_initial = 5
        elif 36 <= p <= 70: #35%
            etat_initial = 4
        elif 71 <= p <= 85: #15%
            etat_initial = 3 
        elif 86 <= p <= 90: #5%
            etat_initial = 2
        else: #10%
            etat_initial = 1
        self.etat = etat_initial
    
    

    def position(self):
        """
        Méthode qui renvoie la position de la personne
        """
        return (self.x,self.y)
    
    def se_deplacer(self,confinement, liste_personnes):
        """
        Méthode qui calcule le déplacement de la personne
        """
        #Déplacement avec dérogation pas détecté contaminé
        if self.derogation == True and self.etat_contamination != 2:
            L = 7
        
        #Déplacement sans confinement
        elif confinement == 0:
            #S'il n'est pas détecté contaminé
            if self.etat_contamination != 2:
                L = self.etat
            #S'il est détecté contaminé
            else:
                L = 1
                
        #Déplacement avec confinement limité !        
        elif confinement == 1:
            #Si il est pas détecté contaminé
            if self.etat_contamination != 2:
                if self.etat - 2 >= 0:
                    L = 2
                else:
                    L = self.etat
            #S'il est détecté contaminé
            else:
                L = 1
        
        #Déplacement avec confinement total !        
        elif confinement == 2:
            L = 1
        else:
            L = 1
        
        self.deplacement = L
        x2 = self.x
        y2 = self.y
        f = True
        while f == True:
            self.x = x2
            self.y = y2
            for i in range(L):
                x = random.randint(-1,1)
                y = random.randint(-1+abs(x),1-abs(x))
                if self.x + x <= 0 or self.x + x > self.longueur:
                    x = - x
                if self.y + y <= 0 or self.y + y > self.largeur:
                    y = -y
                self.x = self.x + x
                self.y = self.y + y
            
            f = False
            for autre in liste_personnes:
                if self != autre:
                    if self.position() == autre.position():
                        f = True
 
        
    def se_contaminer(self):
        """
        Méthode qui gère la contamination d'une personne
        """
        self.etat_contamination = 1
        self.duree_contamination = 0
        self.contagiosite = 0
        if self.etat == 5:
            if 1 <= random.randint(1,100) <= 30:
                self.porteur_sain = True
        if not self.porteur_sain:
            if 1 <= random.randint(1,100) <= 80:
                self.etat = self.etat - 1
            else:
                self.etat = self.etat - 2
        if self.etat <= 0:
            self.mort = True 
        
        
class Evolution:
    """
    Classe qui gère l'évolution des individus et de la simulation au cours des cycles
    """
    def __init__(self):
        """
        
        """
        self.finie = False
        self.Monde = Monde()
        self.liste_morts = []
        self.nombre_doses_vaccination = 0
        self.contagiosite = 35
        self.arrivee_vaccination = 100
        self.efficacite_vaccins = 95
        self.theme = "white"
        self.stop = False
        self.nouveaux_morts = 0
        self.dico_informations = {"Nombre de contaminés":[],"Nombre de personnes déjà contaminées":[], "Nombre de vaccinés":[],"Nombre de morts":[]}
        self.dico_confinements = {0 : [], 1 : [], 2 : []}
        self.ancien_etat_confinement = self.Monde.confinement
        self.nbr_deja_contamines = 0
        
    def deplacer_population(self):
        """
        Méthode qui déplace toutes les personnes de la simulation à chaque cycle
        """
        for personne in self.Monde.liste_personnes:
            if personne.etat > 0:
                personne.se_deplacer(self.Monde.confinement, self.Monde.liste_personnes)
                while self.est_dans_la_meme_case(personne):
                    personne.se_deplacer(self.Monde.confinement, self.Monde.liste_personnes)
                #self.Monde.M[personne.y-1][personne.x-1] = personne

    
    def est_dans_la_meme_case(self,personne):
        """
        Méthode qui renvoie si une personne se situe dans la même case qu'une autre ou non
        """  
        for autre in self.Monde.liste_personnes:
            if personne != autre:
                if personne.position() == autre.position():
                    return True
        return False
    
    def calculer_distance(self, personne,autre):
        """
        Méthode qui calcule la distance entre deux personnes
        """
        dx = abs(personne.x - autre.x)
        dy = abs(personne.y - autre.y)
        return dx + dy
    

    
    def gerer_contaminations(self):
        """
        Méthode qui gère les contaminations entre les personnes contaminées et saines à chaque cycle
        """
        for personne in self.Monde.liste_personnes:
            for personne2 in self.Monde.liste_personnes:
                if self.calculer_distance(personne,personne2) == 1 and 1 <= random.randint(1,100) <= personne2.contagiosite:
                    if personne.etat_contamination == 0 and not personne.immunite:
                        personne.se_contaminer()
                        self.nbr_deja_contamines += 1

                        
    def gerer_morts(self):
        """
        Méthode qui gère la mort des personnes à chaque cycle
        """
        for personne in self.Monde.liste_personnes:
            if personne.mort:
                self.Monde.liste_personnes.remove(personne)
                self.liste_morts.append(personne)
                self.nouveaux_morts += 1
                self.x = None
                self.y = None
          
          
    def gerer_contamines(self):
        """
        Méthode qui gère l'évolution des personnes contaminées à chaque cycle
        """
        for personne in self.Monde.liste_personnes:
            if personne.etat_contamination != 0:
                if personne.immunite:
                    personne.etat_contamination = 0
                else:
                    if personne.derogation and personne.etat_contamination == 2:
                        personne.derogation = False
                    personne.duree_contamination = personne.duree_contamination + 1
                    
                    if 5<= personne.duree_contamination < 15:
                        personne.contagiosite = self.contagiosite
                    if 15 <= personne.duree_contamination < 25:
                        personne.contagiosite = 0.75*self.contagiosite
                    if 25 <= personne.duree_contamination:
                        personne.contagiosite = 0
                        personne.etat_contamination = 0
                        personne.immunite = True

                    if personne.etat_contamination == 1 and random.randint(1,5) == 1:
                        personne.etat_contamination = 2
        
    
    def gerer_tkinter_avant(self):
        """
        Méthode qui colorie toutes les cases du canvas dans la couleur du thème à chaque cycle
        """
        for personne in self.Monde.liste_personnes:
            canvas.itemconfigure(liste_cases[(personne.x - 1) + (personne.y - 1) * self.Monde.longueur], fill = self.theme)
    
    def gerer_tkinter(self):
        """
        Méthode qui colorie les cases du canvas en fonction de la position des personnes à chaque cycle
        """
        liste_col = ["green","orange","red"]
        for personne in self.Monde.liste_personnes:
            if personne.vaccination:
                canvas.itemconfigure(liste_cases[(personne.x - 1) + (personne.y - 1) * self.Monde.longueur], fill = "#0E3B90")
            elif personne.immunite:
                canvas.itemconfigure(liste_cases[(personne.x - 1) + (personne.y - 1) * self.Monde.longueur], fill = "#4D8BFF")
            else:
                canvas.itemconfigure(liste_cases[(personne.x - 1) + (personne.y - 1) * self.Monde.longueur], fill = liste_col[personne.etat_contamination])
    
        
    def vaccination(self):
        """
        Méthode qui gère la campagne de vaccination à chaque cycle
        """
        self.nombre_doses_vaccination = self.nombre_doses_vaccination + self.Monde.nbr_personnes * 1 / 250
        for i in range(1, 6):
            if self.nombre_doses_vaccination >= 1:
                for personne in self.Monde.liste_personnes:
                    #print(self.nombre_doses_vaccination > 0 and personne.vaccination == None and personne.etat == i, self.nombre_doses_vaccination, personne.vaccination, self.Monde.temps)
                    #input()
                    if self.nombre_doses_vaccination >= 1 and personne.vaccination == None and personne.etat == i:
                        if 1<= random.randint(1,100) <= self.efficacite_vaccins:
                            personne.vaccination = True
                        self.nombre_doses_vaccination = self.nombre_doses_vaccination - 1
        
                
    def gerer_vaccines(self):
        """
        Méthode qui gère l'évolution d'une personne vaccinée à chaque cycle
        """
        for personne in self.Monde.liste_personnes:
            if personne.duree_vaccination >= 5:
                personne.immunite = True
                personne.contagiosite = 0
                personne.etat_contamination = 0
            if personne.vaccination == True:
                personne.duree_vaccination = personne.duree_vaccination + 1

    
    def est_fini(self):
        """
        Méthode qui teste si la simulation est finie à chaque cycle
        """
        liste_contamines = []
        for personne in self.Monde.liste_personnes:
            if personne.etat_contamination != 0:
                liste_contamines.append(personne)
        if len(liste_contamines) == 0:
            self.finie = True

    def demarrage(self):
        """
        Méthode appelée au début de la simulation pour construire le Monde à partir des valeurs
        choisies par l'utilisateur
        """
        self.Monde.nombre_personnes()
        self.Monde.attribuer_positions()
        self.Monde.determiner_contamines_initial()
        self.Monde.attributer_identifiant()
        
            
    def commencer(self):
        """
        Méthode qui gère la simulation en appelant toutes les méthodes utiles à son fonctionnement à chaque cycle
        """
        if not self.finie == True:
            
            self.Monde.temps = self.Monde.temps + 1
            
            self.gerer_tkinter_avant()
            self.deplacer_population()
            self.gerer_contaminations()
            self.gerer_morts()
            if self.Monde.temps >= self.arrivee_vaccination:
                self.vaccination()
                self.gerer_vaccines()
            self.gerer_contamines()  
            self.gerer_tkinter()
            self.est_fini()
            self.pprint()
            self.gerer_dico_info()
            
            duree_cycle = echelle_cycle.get()
            self.Monde.duree_cycle = duree_cycle
            if not self.stop:
                fen.after(self.Monde.duree_cycle, E.commencer)
        else:
            t = tkinter.StringVar()
            label = tkinter.Label(fen, textvariable= t, font=("Arial", 15))
            label.place(x= longueur_canvas + 60, y = largeur_fen-75)
            t.set("Le virus a été éradiqué")
            
            return "Fin"
            

    
    def pprint_position(self):
        """
        Affiche les positions de chaque personne dans la console (utilisé pour faire des vérifications)
        """
        for personnage in self.Monde.liste_personnes:
            print(personnage.x,personnage.y)
    
    def contamines(self):
        """
        Compte le nombre de personnes contaminées à chaque cycle
        """
        somme = 0
        for personne in self.Monde.liste_personnes:
            if personne.etat_contamination != 0:
                somme = somme + 1
                
        return somme

    def vaccination1(self):
        """
        Compte le nombre de personnes vaccinées à chaque cycle
        """
        somme = 0
        for personne in self.Monde.liste_personnes:
            if personne.vaccination:
                somme = somme + 1
        return somme
        
    def pprint(self):
        """
        Affiche les informations du cycle sur le côté de la fenêtre de la simulation à chaque cycle
        """
        liste_textes[0].set("Cycle n°" + str(self.Monde.temps))
        liste_textes[1].set("Nombre de contaminés : "+ str(self.contamines()) + " : "+ str(round(self.contamines()*100/self.Monde.nbr_personnes,1)) + " %")
        liste_textes[2].set("Nombre de morts : "+ str(len(self.liste_morts)) + " : "+ str(round(len(self.liste_morts)*100/self.Monde.nbr_personnes,1)) + " %")
        liste_textes[3].set("Nombre de vaccinés : " + str(self.vaccination1()) + " : "+ str(round(self.vaccination1()*100/self.Monde.nbr_personnes,1)) + " %")
        t_doses.set("Nouvelles vaccinations par cycle : " + str(round(self.Monde.nbr_personnes * 1 / 250,2)) + " : "+ str(round(self.Monde.nbr_personnes * 1 / 250*100 / self.Monde.nbr_personnes,2)) + " %")

    def gerer_dico_info(self):
        """
        Ajoute les informations du cycle dans un dictionnaire pour les statistiques
        """
        self.dico_informations["Nombre de contaminés"] += [round(self.contamines()*100/self.Monde.nbr_personnes,2)]
        self.dico_informations["Nombre de personnes déjà contaminées"] += [round(self.nbr_deja_contamines*100/self.Monde.nbr_personnes,2)]
        self.dico_informations["Nombre de vaccinés"] += [round(self.vaccination1()*100/self.Monde.nbr_personnes,2)]
        self.dico_informations["Nombre de morts"] += [round(self.nouveaux_morts*100/self.Monde.nbr_personnes,2)]

        
E = Evolution()

fen1 = tkinter.Tk()
longueur_fen1,largeur_fen1 = 900,650
fen1.geometry(str(longueur_fen1)+"x"+str(largeur_fen1)) 
fen1.title("Réglages et paramètres de la simulation")
fen1.resizable(width = False, height = False)
fen1.configure(bg = "#2C505F")

theme = 0



def recuperer_informations():
    """
    Récupére les valeurs des curseurs et détruit la fenêtre des paramètres
    """
    global longueur_fen, largeur_fen
    longueur_fen = echelle_longueur.get()
    largeur_fen = echelle_largeur.get()
    fen1.destroy()
    
    
liste_parametres = [E.Monde.longueur,E.Monde.largeur,E.Monde.duree_cycle,E.Monde.densite,E.Monde.contamines_initial,E.contagiosite,E.arrivee_vaccination,E.efficacite_vaccins]
liste_str = ["Longueur en cases","Largeur en cases","Durée d'un cycle en ms","Densité de la population en %","Population initiale contaminée","Contagiosité du virus en %","Cycle d'arrivée de la vaccination","Efficacité des vaccins en %"]
liste_bornes = [(5,60),(4,50),(1,1500),(1,90),(1,100),(1,100),(5,150),(1,100)]
liste_incrémentations = [1,1,10,1,1,1,2,2]

def incrementer(rang):
    """
    Permet d'augmenter la valeur des paramètres grâces aux boutons + dans la fenêtre des paramètres
    """
    if liste_parametres[rang] < liste_bornes[rang][1]:
        liste_parametres[rang] = liste_parametres[rang] + liste_incrémentations[rang]
        if liste_parametres[rang] > liste_bornes[rang][1]:
            liste_parametres[rang] = liste_bornes[rang][1]
        liste_labels[rang].set(liste_parametres[rang])
    
def decrementer(rang):
    """
    Permet de diminuer la valeur des paramètres grâces aux boutons - dans la fenêtre des paramètres
    """
    if liste_parametres[rang] > liste_bornes[rang][0]:
        liste_parametres[rang] = liste_parametres[rang] - liste_incrémentations[rang]
        if liste_parametres[rang] < liste_bornes[rang][0]:
            liste_parametres[rang] = liste_bornes[rang][0]
        liste_labels[rang].set(liste_parametres[rang])

liste_boutons_plus = []
liste_boutons_moins = []
liste_labels = []

a = 30
b = 45
liste = []

for i in range(len(liste_parametres)):
    #Création du bouton d'incrémentation
    bouton_plus = tkinter.Button(fen1,text = "+",command = lambda i=i: incrementer(i))
    bouton_plus.place(x= a, y = b)
    liste_boutons_plus.append(bouton_plus)
    
    #Création du texte du paramètre
    texte = tkinter.StringVar()
    label = tkinter.Label(fen1, textvariable=texte, font=("", 10), bg = "#2C505F",fg = "white")
    label.place(x= a - 10, y = b - 30)
    texte.set(liste_str[i])
    
    #Création du label ( change en appuyant sur les boutons + ou - )
    texte2 = tkinter.StringVar()
    label2 = tkinter.Label(fen1, textvariable=texte2, font=("", 10), bg = "#2C505F",fg = "white")
    label2.place(x= a + 30, y = b)
    texte2.set(liste_parametres[i])
    liste_labels.append(texte2)
    
    #Création du bouton de décrémentation
    bouton_moins = tkinter.Button(fen1,text = "-",command = lambda i=i: decrementer(i))
    bouton_moins.place(x= a + 60, y = b )
    liste_boutons_moins.append(bouton_moins)
    
    b = b + 80
    if b >= largeur_fen1:
        b = 170
        a = a + 680

longueur_ecran = 1920
hauteur_ecran = 1080
    
echelle_longueur = tkinter.Scale(fen1, from_ = 1200, to = 2300, orient = "horizontal", tickinterval = 200, resolution = 10, length=300, label = "Longueur de la fenêtre", bg = "#2C505F",fg = "white")
echelle_longueur.pack(pady = (10,0))
echelle_longueur.set(longueur_ecran*0.85)

echelle_largeur = tkinter.Scale(fen1, from_ = 700, to = 1500, orient = "horizontal", tickinterval = 200, resolution = 10, length=300, label = "Largeur de la fenêtre", bg = "#2C505F",fg = "white")
echelle_largeur.pack()
echelle_largeur.set(hauteur_ecran*0.85)



text = tkinter.StringVar()
lab = tkinter.Label(fen1, textvariable=text, font=("", 10),bg = "#2C505F",fg = "white")
lab.pack(pady = (25,5))
text.set("Confinement")

confinement = ["Aucun confinement", "Confinement limité", "Confinement strict"]

boutons = {}

v = tkinter.IntVar()

for i in range(len(confinement)):
    c = tkinter.Radiobutton(fen1, variable = v, value = i,  text = confinement[i],bg = "#2C505F", fg = "black")
    c.pack()
    boutons[confinement[i]] = c
v.set(0)



text2 = tkinter.StringVar()
lab2 = tkinter.Label(fen1, textvariable=text2, font=("", 10),bg = "#2C505F",fg = "white")
lab2.pack(pady = (25,5))
text2.set("Thème")

themes = ["Clair","Sombre"]

boutons2 = {}

v2 = tkinter.IntVar()

for i in range(len(themes)):
    c2 = tkinter.Radiobutton(fen1, variable = v2, value = i,  text = themes[i],bg = "#2C505F",fg = "black")
    c2.pack()
    boutons2[themes[i]] = c2
v2.set(0)



text3 = tkinter.StringVar()
lab3 = tkinter.Label(fen1, textvariable=text3, font=("", 10),bg = "#2C505F",fg = "white")
lab3.pack(pady = (25,5))
text3.set("Afficher le quadrillage")

quadri = ["Oui","Non"]

boutons3 = {}

v3 = tkinter.IntVar()

for i in range(len(quadri)):
    c3 = tkinter.Radiobutton(fen1, variable = v3, value = i,  text = quadri[i],bg = "#2C505F",fg = "black")
    c3.pack()
    boutons3[themes[i]] = c3
v3.set(0)



b = tkinter.Button(fen1, text = "Confirmer", width = 30, height = 5, command = recuperer_informations, bg = "white", fg = "black")
b.pack(pady = (30,0))

continuer = True

def arreter_prog():
    """
    Permet de quitter la fenêtre des réglages et des paramètres de la simulation
    """
    global continuer
    fen1.destroy()
    continuer = False

quitter = tkinter.Button(fen1, text = "Quitter", width = 10, height = 2, command = arreter_prog, bg = "red", fg = "white")
quitter.place(x= longueur_fen1 - 100, y = 10)

fen1.mainloop()

E.Monde.longueur = liste_parametres[0]
E.Monde.largeur = liste_parametres[1]
E.Monde.duree_cycle = liste_parametres[2]
E.Monde.densite = liste_parametres[3]
E.Monde.confinement = v.get()
E.dico_confinements[E.Monde.confinement] += [1]
E.Monde.contamines_initial = liste_parametres[4]
E.contagiosite = liste_parametres[5]
E.arrivee_vaccination = liste_parametres[6]
E.efficacite_vaccins = liste_parametres[7]

theme = v2.get()
quadrillage = v3.get()


themes = ["white","black"]
if theme == 1:
    themes = ["black","white"]
E.theme = themes[0]

liste_cases = []
    

fen = tkinter.Tk()

fen.geometry(str((longueur_fen))+"x"+str(largeur_fen)) 
fen.title("Simulation de la propagation d'un virus dans une population")
fen.resizable(width = False, height = False)
longueur_canvas, hauteur_canvas = int(0.74*longueur_fen),largeur_fen
canvas = tkinter.Canvas(fen,width = longueur_canvas, height = hauteur_canvas, bg= themes[0])
canvas.place(x=0,y=0)

L = longueur_canvas/E.Monde.longueur
x1,x2 = 0,0
y1,y2 = 0, hauteur_canvas

liste_couleur_quadri = themes.copy()
if quadrillage == 1:
    liste_couleur_quadri.reverse()

    
for i in range(E.Monde.longueur):
    canvas.create_line(x1, y1, x2, y2, width=1, fill=liste_couleur_quadri[1])
    x1 = x1 + L
    x2 = x2 + L

l = hauteur_canvas/E.Monde.largeur
x1,x2 = 0,longueur_canvas
y1,y2 = 0, 0
for i in range(E.Monde.largeur):
    canvas.create_line(x1, y1, x2, y2, width=1, fill=liste_couleur_quadri[1])
    y1 =y1 + l
    y2 = y2 + l

L = L
l = l
x1,x2,y1,y2 = 1,L,1,l

for _ in range(E.Monde.largeur):
    for _ in range(E.Monde.longueur):
        liste_cases.append(canvas.create_rectangle(x1,y1,x2,y2, width = 0,fill = themes[0]))
        x1,x2 = x1 + L, x2 + L
    x1,x2 = 1,L
    y1,y2 = y1 + l, y2 + l
    

y = 40
g = 20
liste_textes = []
for i in range(4):
    if i == 1:
        y = y + 10
        g = 15
    liste_textes.append(tkinter.StringVar())
    label = tkinter.Label(fen, textvariable=liste_textes[-1], font=("Arial", g))
    label.place(x= longueur_canvas + 10, y=y)
    y = y + 40

t_doses =  tkinter.StringVar()
label_doses = tkinter.Label(fen, textvariable= t_doses, font=("Arial", 12))
label_doses.place(x= longueur_canvas + 10, y=195)
t_doses.set('Nouvelles vaccinations par cycle : 0 : 0 %')

liste_legendes_couleurs = ["green","red","orange","#0E3B90","#4D8BFF"]
liste_legendes_labels = []
liste_legendes_textes = ["Personnes saines","Personnes contaminées","Contaminés non détectés","Personnes vaccinées","Personnes immunisées"]
liste_legendes_carres = []
y = 253
y2 = 5

canvas_legende = tkinter.Canvas(fen,width = 50, height = 220)
canvas_legende.place(x=longueur_canvas + 10,y=250)

for i in range(5):
    liste_legendes_carres.append(canvas_legende.create_rectangle(2,y2,50,y2+20, width = 1,fill = liste_legendes_couleurs[i]))
    
    liste_legendes_labels.append(tkinter.StringVar())
    label = tkinter.Label(fen, textvariable=liste_legendes_labels[-1], font=("Arial", 13))
    label.place(x= longueur_canvas + 65, y=y)
    liste_legendes_labels[-1].set(liste_legendes_textes[i])
    y = y + 45
    y2 = y2 + 45
    

def changer_confinement(rang):
    """
    Permet de changer l'état de confinement du Monde pendant la simulation
    >>> changer_confinement(2)
    >>> changer_confinement(1)
    >>> changer_confinement(0)
    """
    E.Monde.confinement = rang
    t_confinement.set(liste_textes_confinements[E.Monde.confinement])
    E.dico_confinements[E.Monde.confinement] += [E.Monde.temps]
    
liste_boutons_confinements = []
liste_textes_confinements = ["Aucun confinement","Confinement limité","Confinement strict"]
liste_couleurs_boutons = ["#BDBDBD","#6F6F6F","#3B3B3B"]


echelle_cycle = tkinter.Scale(fen, from_ = 1, to = 1500, orient = "vertical", tickinterval = 999, resolution = 1, length=150, label = "Durée cycle")
echelle_cycle.place(x = longueur_canvas + 163, y = 490)
echelle_cycle.set(E.Monde.duree_cycle)

y = 510

for i in range(3):
    liste_boutons_confinements.append(tkinter.Button(fen, text = liste_textes_confinements[i], width = 20, height = 1, command = lambda i=i: changer_confinement(i), bg = liste_couleurs_boutons[i], fg = "white"))
    liste_boutons_confinements[-1].place(x= longueur_canvas + 20 , y= y)
    y = y + 50
    
t_confinement =  tkinter.StringVar()
label_confinement = tkinter.Label(fen, textvariable= t_confinement, font=("Arial", 15))
label_confinement.place(x= longueur_canvas + 20, y=475)
t_confinement.set(liste_textes_confinements[E.Monde.confinement])


def quitte():
    """
    Détruit la fenêtre de la simulation
    """
    E.stop = True
    fen.destroy()

quitter2 = tkinter.Button(fen, text = "Quitter", width = 8, height = 2, command = quitte, bg = "red", fg = "white")
quitter2.place(x= longueur_fen - 90, y = 10)


E.demarrage()
E.commencer()

def statistiques():
    """
    Ouvre une fenêtre affichant les statistiques de la simulation sous forme de graphiques
    """
    fen.destroy()
    
    fen2 = tkinter.Tk()
    fen2.geometry(str((longueur_fen))+"x"+str(largeur_fen)) 
    fen2.title("Statistiques de la simulation")
    fen2.resizable(width = False, height = False)
    fen2.configure(bg="#2C505F")
    
    liste_textes_confinements = ["Aucun confinement","Confinement limité","Confinement strict"]
    
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    a, b = 10,10
    
    
    liste_couleurs = ["green","orange","red"]
    
    dico_dimensions = {23:9,22:10,21:11,20:12,19:13,18:14,17:15,16:16,15:17,14:18,13:19,12:20,11:21,10:22,9:23,8:24,7:25}
    for info in E.dico_informations:
        
        
        fig = Figure(figsize=(longueur_fen/225, largeur_fen/225))
        ax = fig.add_subplot(111)
        
        t, = ax.plot(range(E.Monde.temps), E.dico_informations[info])
        
        L_ax = []
        L_ax.append(t)
        L_legendes_confinements = []

         
        for confinement in E.dico_confinements:
            for cycle in E.dico_confinements[confinement]:
                x = [cycle,cycle]
                y = [0,max(E.dico_informations[info])]
                t, = ax.plot(x,y, color = liste_couleurs[confinement])
                
            if E.dico_confinements[confinement] != []:
                L_ax.append(t)
                
        ax.set_xlabel("Cycles")
        ax.set_ylabel("% de la population")
        ax.grid()
            
        axx = []
        acc = [info]
        for p in L_ax:
            axx += [p]
        axx = tuple(axx)
        
        for m in E.dico_confinements:
            if E.dico_confinements[m] != []:
                acc += [liste_textes_confinements[m]]
        acc = tuple(acc)
        
        fig.legend(axx, acc, 'upper left')
             
        graph = FigureCanvasTkAgg(fig, master=fen2)
        canvas = graph.get_tk_widget()
        canvas.place(x=a,y=b)
        
        a = a + 6/11*longueur_fen
        if a+4/11*longueur_fen >= longueur_fen:
            a = 10
            b = largeur_fen/2
    
    
    fen.mainloop()



statistiques = tkinter.Button(fen, text = "Accéder aux statistiques", width = 20, height = 2, command = statistiques, bg = "blue", fg = "white")
statistiques.place(x= (longueur_canvas + longueur_fen)/2-85, y = largeur_fen-40)

#fen.mainloop()



