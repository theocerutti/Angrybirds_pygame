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

def calcul_vector(v0x, v1x, v0y, v1y):
	"""Fonction permettant de calculer un vecteur"""

	vecteur_x = v0x - v1x
	vecteur_y = v0y - v1y
	list_v = [vecteur_x, vecteur_y]

	return list_v



#----------------------------------------------------------------------------------------------------
# CLASSES



class Catapulte:
	"""Classe permettant la gestion de la catapulte"""

	def __init__(self, posx, posy, image, x0ela, y0ela, x1ela, y1ela, x2ela, y2ela, x3ela, y3ela, posx_projectile, posy_projectile, image_projectile):
		"""Constructeur de la classe catapulte
			Arguments:
				- posx, posy : position x et y de l'objet
				- image : image de l'objet de type PhotoImage
				- liste : liste utilisée et dédiée à l'objet
				-x0ela, y1ela,..., = coordonnées des élastiques"""

		#coordonnées de la catapulte
		self.posx = posx
		self.posy = posy

		#on créer la catapulte
		self.image = canvas.create_image(self.posx, self.posy, image = image , anchor = "nw") #on met anchor = NW pour mettre le point d'ancrage en haut à droite

		self.drag = False
		self.hauteur_img = 210 #c'est la hauteur de l'image des catapultes

		#positions x y des élastiques
		self.x0ela, self.y0ela, self.x1ela, self.y1ela = x0ela, y0ela, x1ela, y1ela
		self.x2ela, self.y2ela, self.x3ela, self.y3ela = x2ela, y2ela, x3ela, y3ela

		#crétion des elastiques
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)

		#position,vecteur, gravité et création du projectile
		self.posx_proj = posx_projectile
		self.posy_proj = posy_projectile
		self.posx_proj_initale = posx_projectile #c'est la position initale du projectile, elle restera alors constante
		self.posy_proj_initale = posy_projectile
		self.image_proj = canvas.create_image(self.posx_proj, self.posy_proj, image = image_projectile, anchor = "nw")
		self.gravite = 10
		self.vy = 0
		self.vx = 0

	def click(self, event):
		"""Fonction permettant de voir si on clique sur l'objet"""

		souris_x, souris_y = event.x, event.y

		print("Click x ->", souris_x)

		self.x, self.y = canvas.coords(self.image)

		if self.x <= souris_x <= self.x + self.hauteur_img and self.y <= souris_y <= self.y + self.hauteur_img: #si je clique sur la catapulte alors on met self.drag à True
			self.drag = True

			#on (re)met le projectile dans sa position de base
			self.posx_proj = self.posx_proj_initale
			self.posy_proj = self.posy_proj_initale
			canvas.coords(self.image_proj, self.posx_proj_initale, self.posy_proj_initale)

	def unclick(self, event):
		"""Fonction permettant de détecter lorsque l'on relâche le clique"""

		if self.drag == True:
			self.liste_vecteur = calcul_vector(self.x0ela, self.souris_x, self.y0ela, self.souris_y)
			self.shoot()

		self.drag = False

		#on supprime les élastiques lorsque l'on clique
		canvas.delete(self.elastique1)
		canvas.delete(self.elastique2)

		#recréation des élastiques de la catapulte
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)

	def drag_obj(self, event):
		"""Fonction permettant de drag l'objet et l'animer, si et seulement si, l'objet a été cliqué"""

		if self.drag == True:
			self.souris_x, self.souris_y = event.x, event.y

			#on limite les positions des élastiques
			if self.souris_x > self.x0ela + 100:
				self.souris_x = self.x0ela + 100
			if self.souris_y > self.y0ela + 100:
				self.souris_y = self.y0ela + 100
			if self.souris_x < self.x0ela - 100:
				self.souris_x = self.x0ela - 100
			if self.souris_y < self.y0ela - 100:
				self.souris_y = self.y0ela - 100

			#on change la position des élastiques en fonction de la position de la souris
			canvas.coords(self.elastique1, self.x0ela, self.y0ela, self.souris_x, self.souris_y)
			canvas.coords(self.elastique2, self.x2ela, self.y2ela, self.souris_x, self.souris_y)

			#on positionne le projectile au niveau de la souris
			canvas.coords(self.image_proj, self.souris_x - 45, self.souris_y - 45)

	def shoot(self):
		"""Fonction permettant de faire le shoot du projectile"""

		print(self.vy)
		self.vx = self.liste_vecteur[0]/2
		self.liste_vecteur[1] += self.gravite
		self.vy += self.liste_vecteur[1]/10
		self.vy = min(40, self.vy) #permet de limiter vy à 20, pour pas que le projectile tombe de + en + vite à l'infini
		self.posx_proj += self.vx
		self.posy_proj += self.vy

		#si le projectile tombe au sol alors il ne va pas plus bas
		if self.posy_proj > 420:
			self.posy_proj = 420
			self.vx = 0
			self.vy = 0

		canvas.coords(self.image_proj, self.posx_proj, self.posy_proj)

		if self.posy_proj < 420: #si le projectile est au sol, il n'a plus besoin d'être animé donc on l'arrête
			fenetre.after(70, self.shoot)


background_img = canvas.create_image(0, -250, image = background, anchor = "nw")

catapulte1 = Catapulte(80, 290, catapulte_left, 96, 327, 100, 331,   137, 327, 141, 331, 70, 285, red_bird_img)
catapulte2 = Catapulte(680, 290, catapulte_right, 722, 327, 726, 331,   764, 327, 768, 331, 690, 285, red_bird_img)


canvas.bind("<Button-1>", catapulte1.click) #lorsque l'on clique sur la catapulte 1
canvas.bind("<ButtonRelease-1>", catapulte1.unclick) #lorsqu'on relâche le clique sur la catapulte 1
canvas.bind("<B1-Motion>", catapulte1.drag_obj) #lorsque l'on clique sur la catapulte 1

canvas.bind("<Button-3>", catapulte2.click) #lorsque l'on clique sur la catapulte 2
canvas.bind("<ButtonRelease-3>", catapulte2.unclick) #lorsqu'on relâche le clique sur la catapulte 2
canvas.bind("<B3-Motion>",catapulte2.drag_obj) #lorsque l'on clique sur la catapulte 2

fenetre.mainloop()
