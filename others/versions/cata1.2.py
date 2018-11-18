#!/usr/bin/env python
#-*- coding: utf-8 -*-

#CE QUI FAUT FAIRE
#catapulte en bas en haut/gauche droite
#les catapultes sont éloignés de facon que la deuxieme sort de l'écran, lorsqu'une tire la caméra est sur la boule de canon
#animation de l'image de tir
#trajectoire dynamique avec des points
#background dynamique qui bouge selon la position de la souris
#pouvoirs : vitesse balle ++, barrière, possibilité de détruire la boule adverse, projecticles spéciaux, truc pour recup vie, truc pour augmenter sa vitesse
#système de vie des joueurs
#I.A ? -> si oui plusieurs niveaux de difficultés
#système de gain d'argent permettant d'acheter des pouvoirs, vies, armure..  -> si on améliore l'armure la catapulte aura un new design
#sytème de barrière

from tkinter import *
import time

fenetre = Tk()

#fenetre.iconbitmap("mon_icone.ico") # on change l'icône de notre fenêtre
fenetre.geometry("1000x800") # on change les dimensions de notre fenêtre
fenetre.title('Jeu des catapultes') #on change le titre du jeu

canvas = Canvas(fenetre, width = 840, height = 680, bg ='black')
canvas.pack()



#----------------------------------------------------------------------------------------------------
# VARIABLES



#----------------------------------------------------------------------------------------------------
# IMAGES
catapulte_left = PhotoImage(file = "lib/image/cata_left.gif")
catapulte_right = PhotoImage(file = "lib/image/cata_right.gif")
red_bird_img = PhotoImage(file = "lib/image/red_bird.gif")
background = PhotoImage(file = "lib/image/world.gif")


#----------------------------------------------------------------------------------------------------
# FONCTIONS

def shift_world():
	pass



#----------------------------------------------------------------------------------------------------
# CLASSES



class Catapulte:
	"""Classe permettant la gestion de la catapulte"""

	def __init__(self, posx, posy, image, x0ela, y0ela, x1ela, y1ela, x2ela, y2ela, x3ela, y3ela):
		"""Constructeur de la classe catapulte
			Arguments:
				- posx, posy : position x et y de l'objet
				- image : image de l'objet de type PhotoImage
				- liste : liste utilisée et dédiée à l'objet"""

		self.image = canvas.create_image(posx, posy, image = image , anchor = "nw") #on met anchor = NW pour mettre le point d'ancrage en haut à droite
		self.posx = posx
		self.posy = posy
		self.drag = False
		self.hauteur_img = 210 #c'est la hauteur de l'image des catapultes

		#positions x y des élastiques
		self.x0ela, self.y0ela, self.x1ela, self.y1ela = x0ela, y0ela, x1ela, y1ela
		self.x2ela, self.y2ela, self.x3ela, self.y3ela = x2ela, y2ela, x3ela, y3ela

		#crétion des elastiques
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)


	def click(self, event):
		"""Fonction permettant de voir si on clique sur l'objet"""

		souris_x, souris_y = event.x, event.y

		self.x, self.y = canvas.coords(self.image)

		if self.x <= souris_x <= self.x + self.hauteur_img and self.y <= souris_y <= self.y + self.hauteur_img: #si je clique sur la catapulte alors on met self.drag à True
			self.drag = True

	def unclick(self, event):
		"""Fonction permettant de détecter lorsque l'on relâche le clique"""

		self.drag = False

		#on supprime les élastiques lorsque l'on clique
		canvas.delete(self.elastique1)
		canvas.delete(self.elastique2)

		#recréation des élastiques de la catapulte
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)

	def drag_obj(self, event):
		"""Fonction permettant de drag l'objet et l'animer, si et seulement si, l'objet a été cliqué"""

		souris_x, souris_y = event.x, event.y

		#on limite les positions des élastiques
		if souris_x > self.x0ela + 100:
			souris_x = self.x0ela + 100
		if souris_y > self.y0ela + 100:
			souris_y = self.y0ela + 100
		if souris_x < self.x0ela - 100:
			souris_x = self.x0ela - 100
		if souris_y < self.y0ela - 100:
			souris_y = self.y0ela - 100

		if self.drag == True: #on change la position des élastiques en fonction de la position de la souris
			canvas.coords(self.elastique1, self.x0ela, self.y0ela, souris_x, souris_y)
			canvas.coords(self.elastique2, self.x2ela, self.y2ela, souris_x, souris_y)


background_img = canvas.create_image(0, -250, image = background, anchor = "nw")
red_bird = canvas.create_image(70, 285, image = red_bird_img, anchor = "nw")
red_bird = canvas.create_image(690, 285, image = red_bird_img, anchor = "nw")

catapulte1 = Catapulte(80, 290, catapulte_left, 96, 327, 100, 331,   137, 327, 141, 331)
catapulte2 = Catapulte(680, 290, catapulte_right, 722, 327, 726, 331,   764, 327, 768, 331)


canvas.bind("<Button-1>", catapulte1.click) #lorsque l'on clique sur la catapulte 1
canvas.bind("<ButtonRelease-1>", catapulte1.unclick) #lorsqu'on relâche le clique sur la catapulte 1
canvas.bind("<B1-Motion>", catapulte1.drag_obj) #lorsque l'on clique sur la catapulte 1

canvas.bind("<Button-3>", catapulte2.click) #lorsque l'on clique sur la catapulte 2
canvas.bind("<ButtonRelease-3>", catapulte2.unclick) #lorsqu'on relâche le clique sur la catapulte 2
canvas.bind("<B3-Motion>", catapulte2.drag_obj) #lorsque l'on clique sur la catapulte 2

fenetre.mainloop()
