# script drag_and_drop.py
#(C) Fabrice Sincère
from tkinter import *

def Clic(event):
    """ Gestion de l'événement Clic gauche """
    global DETECTION_CLIC_SUR_OBJET

    # position du pointeur de la souris
    X = event.x
    Y = event.y
    print("Position du clic -> ",X,Y)

    # coordonnées de l'objet
    [xmin,ymin,xmax,ymax] = Canevas.coords(Carre)
    print(Canevas.coords(Carre))

    print("Position objet -> ",xmin,ymin,xmax,ymax)
    if xmin<=X<=xmax and ymin<=Y<=ymax: DETECTION_CLIC_SUR_OBJET = True
    else: DETECTION_CLIC_SUR_OBJET = False
    print("DETECTION CLIC SUR OBJET -> ",DETECTION_CLIC_SUR_OBJET)

def Drag(event):
    """ Gestion de l'événement bouton gauche enfoncé """
    X = event.x
    Y = event.y
    print("Position du pointeur -> ",X,Y)

    if DETECTION_CLIC_SUR_OBJET == True:
        # limite de l'objet dans la zone graphique
        if X<0: X=0
        if X>Largeur: X=Largeur
        if Y<0: Y=0
        if Y>Hauteur: Y=Hauteur
        # mise à jour de la position de l'objet (drag)
        Canevas.coords(Carre,X-TailleCarre,Y-TailleCarre,X+TailleCarre,Y+TailleCarre)

DETECTION_CLIC_SUR_OBJET = False

# Création de la fenêtre principale
Mafenetre = Tk()
Mafenetre.title("Drag and drop")

# Création d'un widget Canvas
Largeur = 480
Hauteur = 160
TailleCarre = 20
Canevas = Canvas(Mafenetre,width=Largeur,height=Hauteur,bg ='white')
# Création d'un objet graphique
Carre = Canevas.create_rectangle(0,0,TailleCarre*2,TailleCarre*2,fill='maroon')

# La méthode bind() permet de lier un événement avec une fonction
Canevas.bind('<Button-1>',Clic) # évévement clic gauche (press)
Canevas.bind('<B1-Motion>',Drag) # événement bouton gauche enfoncé (hold down)

#Canevas.focus_set()
Canevas.pack(padx=10,pady=10)

Mafenetre.mainloop()
