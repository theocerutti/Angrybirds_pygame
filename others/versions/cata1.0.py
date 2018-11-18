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
catapulte_left_0 = PhotoImage(file = "lib/image/0_left.gif")
catapulte_left_1 = PhotoImage(file = "lib/image/1_left.gif")
catapulte_left_2 = PhotoImage(file = "lib/image/2_left.gif")
catapulte_left_3 = PhotoImage(file = "lib/image/3_left.gif")
catapulte_left_4 = PhotoImage(file = "lib/image/4_left.gif")
catapulte_left_5 = PhotoImage(file = "lib/image/5_left.gif")
catapulte_left_6 = PhotoImage(file = "lib/image/6_left.gif")
catapulte_left_7 = PhotoImage(file = "lib/image/7_left.gif")
catapulte_left_8 = PhotoImage(file = "lib/image/8_left.gif")
catapulte_left_9 = PhotoImage(file = "lib/image/9_left.gif")
catapulte_left_10 = PhotoImage(file = "lib/image/10_left.gif")
catapulte_left_11 = PhotoImage(file = "lib/image/11_left.gif")

catapulte_right_0 = PhotoImage(file = "lib/image/0_right.gif")
catapulte_right_1 = PhotoImage(file = "lib/image/1_right.gif")
catapulte_right_2 = PhotoImage(file = "lib/image/2_right.gif")
catapulte_right_3 = PhotoImage(file = "lib/image/3_right.gif")
catapulte_right_4 = PhotoImage(file = "lib/image/4_right.gif")
catapulte_right_5 = PhotoImage(file = "lib/image/5_right.gif")
catapulte_right_6 = PhotoImage(file = "lib/image/6_right.gif")
catapulte_right_7 = PhotoImage(file = "lib/image/7_right.gif")
catapulte_right_8 = PhotoImage(file = "lib/image/8_right.gif")
catapulte_right_9 = PhotoImage(file = "lib/image/9_right.gif")
catapulte_right_10 = PhotoImage(file = "lib/image/10_right.gif")
catapulte_right_11 = PhotoImage(file = "lib/image/11_right.gif")

background = PhotoImage(file = "lib/image/world.gif")


#----------------------------------------------------------------------------------------------------
# FONCTIONS

def shift_world():
	pass



#----------------------------------------------------------------------------------------------------
# CLASSES



class Catapulte:
	"""Classe permettant la gestion de la catapulte"""

	def __init__(self, posx, posy, image, liste):
		"""Constructeur de la classe catapulte
			Arguments:
				- posx, posy : position x et y de l'objet
				- image : image de l'objet de type PhotoImage
				- liste : liste utilisée et dédiée à l'objet"""

		self.cata_indice = 0
		self.cata_list = liste #on prend la liste dédié à l'une des deux catapultes
		self.image = canvas.create_image(posx, posy, image = self.cata_list[self.cata_indice] , anchor = "nw") #on met anchor = NW pour mettre le point d'ancrage en haut à droite
		self.posx = posx
		self.posy = posy
		self.drag = False
		self.hauteur_img = 76 #c'est la hauteur de l'image des catapultes

		#pour l'animation de l'objet
		self.last_run = 0
		self.period_anim = 0


	def click(self, event):
		"""Fonction permettant de voir si on clique sur l'objet"""

		souris_x, souris_y = event.x, event.y

		self.x, self.y = canvas.coords(self.image)

		if self.x <= souris_x <= self.x + self.hauteur_img and self.y <= souris_y <= self.y + self.hauteur_img: #si je clique sur la catapulte alors on met self.drag à True
			self.drag = True
		else: #si on ne clique pas dessus alors on met self.drag à False et on remet l'animation à l'image 0
			self.drag = False
			self.cata_indice = 0 #si on drag plus alors on remet l'animation du
			canvas.delete(self.image) #on supprime l'image d'avant
			self.image = canvas.create_image(self.posx, self.posy, image = self.cata_list[self.cata_indice] , anchor = "nw") #l'image de 'base' au début sera la cata gauche

	def drag_obj(self, event):
		"""Fonction permettant de drag l'objet et l'animer, si et seulement si, l'objet a été cliqué"""

		if self.drag == True:
			if time.time() - self.last_run > self.period_anim: #cette ligne est pour limiter la vitesse d'animation
				#l'animation
				self.cata_indice += 1
				if self.cata_indice == len(self.cata_list): #si cata_indice est au dernier indice de la liste alors on le remet à 0
					self.cata_indice = 0

				canvas.delete(self.image) #on supprime l'image d'avant
				self.image = canvas.create_image(self.posx, self.posy, image = self.cata_list[self.cata_indice] , anchor = "nw") #et on remet l'image suivante à la même place
			self.last_run = time.time()


background_img = canvas.create_image(0, -250, image = background, anchor = "nw")

#on créer une liste pour la catapulte à gauche (tourné vers la droite) et on y ajoute toute son animation
list_cata_right_img = []
list_cata_right_img.append(catapulte_right_0)
list_cata_right_img.append(catapulte_right_1)
list_cata_right_img.append(catapulte_right_2)
list_cata_right_img.append(catapulte_right_3)
list_cata_right_img.append(catapulte_right_4)
list_cata_right_img.append(catapulte_right_5)
list_cata_right_img.append(catapulte_right_6)
list_cata_right_img.append(catapulte_right_7)
list_cata_right_img.append(catapulte_right_8)
list_cata_right_img.append(catapulte_right_9)
list_cata_right_img.append(catapulte_right_10)
list_cata_right_img.append(catapulte_right_11)

#on créer une liste pour la catapulte à droite (tourné vers la gauche) et on y ajoute toute son animation
list_cata_left_img = []
list_cata_left_img.append(catapulte_left_0)
list_cata_left_img.append(catapulte_left_1)
list_cata_left_img.append(catapulte_left_2)
list_cata_left_img.append(catapulte_left_3)
list_cata_left_img.append(catapulte_left_4)
list_cata_left_img.append(catapulte_left_5)
list_cata_left_img.append(catapulte_left_6)
list_cata_left_img.append(catapulte_left_7)
list_cata_left_img.append(catapulte_left_8)
list_cata_left_img.append(catapulte_left_9)
list_cata_left_img.append(catapulte_left_10)
list_cata_left_img.append(catapulte_left_11)

catapulte1 = Catapulte(80, 420,  list_cata_right_img[0], list_cata_right_img)
catapulte2 = Catapulte(680, 420, list_cata_left_img[0], list_cata_left_img)


canvas.bind("<Button-1>", catapulte1.click) #lorsque l'on clique sur la catapulte 1
canvas.bind("<B1-Motion>", catapulte1.drag_obj) #lorsque l'on clique sur la catapulte 1

canvas.bind("<Button-3>", catapulte2.click) #lorsque l'on clique sur la catapulte 2
canvas.bind("<B3-Motion>", catapulte2.drag_obj) #lorsque l'on clique sur la catapulte 2

fenetre.mainloop()
