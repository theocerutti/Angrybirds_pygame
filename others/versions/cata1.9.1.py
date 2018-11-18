#!/usr/bin/env python
#-*- coding: utf-8 -*-

#b----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#j'ai fait expres que ca bug ici pour que vous lisiez ceci :

# A LIRE !!!!! CET VERSION CORRIGE LE BUG DU SHIFT "faire un bon shift" (voir section problèmes rencontrés) CEPENDANT ELLE LE CORRIGE DE MANIERE NON OPTIMISEE ET PAS VRAIMENT ELEGANTE MAIS PLUTOT DE MANIERE FORCING DONC CETTE VERSION EST A MODIFER !!!!!!!

#b------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#IDEE DE DVPT
#pouvoirs : vitesse balle ++, barrière, possibilité de détruire la boule adverse, projecticles spéciaux, truc pour recup vie, truc pour augmenter sa vitesse
#système de vie des joueurs
#système de gain d'argent permettant d'acheter des pouvoirs, vies, armure..  -> si on améliore l'armure la catapulte aura un new design
#sytème de barrière

#CE QU'IL FAUT FAIRE
#mettre shift_world et return_camera dans la classe WORLD
#faire une bonne attente pour le return camera

#PROBLEME RENCONTRES/BUGS
#

#PROBLEME ET LEURS SOLUTION
#le shift ne peut se faire car la pos_x_obj ne fait que baisser, ce systeme de shift ne va pas avec les projectiles
#	-> j'ai ajouté un intermediaire posx_shift qui elle ne se remet pas a 500
#si je shift deux fois en mm temps (ex: haut/droite) y'a un bug car il affiche l'image quand y'a un shift mais quand il y eb a deux alors le shift en premier prend le dessus./ faire un fonc affichage qui se fait a la fin --> j'ai enlevé les shifts haut/bas
#lors du shift les positions ne sont pas changés (même si l'affichage lui est modifié) --> j'ai   juste return la valeur
#plusieurs bug de shift bizarres : j'avais oublié de reinitialiser self.pox_shift dans le fonc de reset !
#faire un bon shift -> lorsque je prends proj1 -> shift sur proj2/cata2; si je prends proj2 -> shift sur proj1/cata1 ---> j'ai utilisé
##pas de shift pour la trajectoire --> j'avais oublié de mettre les pts_trajectoire des deux cata (j'avais juste mis self)

from tkinter import *
from math import *
import time

fenetre = Tk()

#fenetre.iconbitmap("mon_icone.ico") # on change l'icône de notre fenêtre
fenetre.geometry("1000x800") # on change les dimensions de notre fenêtre
fenetre.title('Jeu des catapultes') #on change le titre du jeu

hauteur_canvas, largeur_canvas = 840, 680
canvas = Canvas(fenetre, width = hauteur_canvas, height = largeur_canvas, bg ='black')
canvas.pack()


#----------------------------------------------------------------------------------------------------
# VARIABLES

#tour du joueur, quand il est à 0 -> cest le tour du J0 (à gauche) quand il est à 1 c'est au tour du J1 (à droite)
tour = 0
compteur = 0



#----------------------------------------------------------------------------------------------------
# IMAGES
catapulte_left_img = PhotoImage(file = "lib/image/cata_left.gif")
catapulte_right_img = PhotoImage(file = "lib/image/cata_right.gif")
red_bird_img = PhotoImage(file = "lib/image/red_bird.gif")
red_bird_mirror_img = PhotoImage(file = "lib/image/red_bird_mirror.gif")
background_img = PhotoImage(file = "lib/image/world.gif")


#----------------------------------------------------------------------------------------------------
# FONCTIONS


def calcul_vector(v0x, v1x, v0y, v1y):  #self.x_center_ela, self.souris_x, self.y_center_ela, self.souris_y
	"""Fonction permettant de calculer un vecteur"""

	vecteur_x = v0x - v1x
	vecteur_y = v0y - v1y
	print("Impulsion x ->",vecteur_y,"\nImpulsion y ->", vecteur_x)
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
				- x0ela, y1ela,..., = coordonnées des élastiques"""

		#coordonnées de la catapulte
		self.posx = posx
		self.posy = posy

		#on créer la catapulte
		self.image = canvas.create_image(self.posx, self.posy, image = image , anchor = "nw") #on met anchor = NW pour mettre le point d'ancrage en haut à droite

		self.drag = False
		self.largeur_img = 64
		self.hauteur_img = 204 #c'est la hauteur de l'image des catapultes

		#positions x y des élastiques
		self.x0ela, self.y0ela, self.x1ela, self.y1ela = x0ela, y0ela, x1ela, y1ela
		self.x2ela, self.y2ela, self.x3ela, self.y3ela = x2ela, y2ela, x3ela, y3ela
		self.x_center_ela, self.y_center_ela = self.x0ela + 20, self.y0ela #ordonnées du centre "d'inertie" entre les deux élastiques

		#crétion des elastiques
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)

		#position,vecteur, gravité et création du projectile
		self.posx_proj = posx_projectile
		self.posy_proj = posy_projectile
		self.posx_proj_initale = posx_projectile #c'est la position initale du projectile, elle restera alors constante
		self.posy_proj_initale = posy_projectile
		self.posx_shift = posx_projectile #c'est la position pour le shift elle ne sera pas utilisé pour l'affichage de la position
		self.image_proj = canvas.create_image(self.posx_proj, self.posy_proj, image = image_projectile, anchor = 'nw')
		self.gravite = 10
		self.vy = 0
		self.vx = 0

		#trajectoire des points
		self.list_point_trajectoire = []
		self.list_point_trajectoire_x = []
		self.list_point_trajectoire_y = []

	def reset_pos_proj(self):
		"""Fonction permettant de réinitialiser la position du projectile"""

		self.posx_proj = self.posx_proj_initale
		self.posy_proj = self.posy_proj_initale
		self.posx_shift = self.posx_proj_initale
		self.vx = 0
		self.vy = 0

		#on enleve les points de la trajectoire
		for point in range(len(self.list_point_trajectoire)):
			canvas.delete(self.list_point_trajectoire[point])
		self.list_point_trajectoire_x = []
		self.list_point_trajectoire_y = []
		self.list_point_trajectoire = []

	def click(self, event):
		"""Fonction permettant de voir si on clique sur l'objet"""

		self.souris_x, self.souris_y = event.x, event.y

		print("Click x ->", self.souris_x - background.posx,"\nClick y ->", self.souris_y - background.posy + 250)

		if self.posx <= self.souris_x <= self.posx + self.largeur_img and self.posy <= self.souris_y <= self.posy + self.hauteur_img: #si je clique sur la catapulte alors on met self.drag à True
			self.drag = True

			#on (re)met le projectile dans sa position de base
			self.reset_pos_proj()
			canvas.coords(self.image_proj, self.posx_proj, self.posy_proj)

	def drag_obj(self, event):
		"""Fonction permettant de drag l'objet et l'animer, si et seulement si, l'objet a été cliqué"""

		if self.drag == True:
			self.souris_x, self.souris_y = event.x, event.y

			#on limite les positions des élastiques
			if self.souris_x > self.x_center_ela + 100:
				self.souris_x = self.x_center_ela + 100
			if self.souris_y > self.y_center_ela + 100:
				self.souris_y = self.y_center_ela + 100
			if self.souris_x < self.x_center_ela - 120:
				self.souris_x = self.x_center_ela - 120
			if self.souris_y < self.y_center_ela - 100:
				self.souris_y = self.y_center_ela - 100

			#on change la position des élastiques en fonction de la position de la souris
			canvas.coords(self.elastique1, self.x0ela, self.y0ela, self.souris_x, self.souris_y)
			canvas.coords(self.elastique2, self.x2ela, self.y2ela, self.souris_x, self.souris_y)

			#on positionne le projectile au niveau de la souris
			canvas.coords(self.image_proj, self.souris_x - 30, self.souris_y - 30) #30 c'est la moitié de la taille de l'image du projectile

	def unclick(self, event):
		"""Fonction permettant de détecter lorsque l'on relâche le clique"""

		if self.drag == True:
			self.liste_vecteur = calcul_vector(self.x_center_ela, self.souris_x, self.y_center_ela, self.souris_y)
			self.shoot()

		self.drag = False

		#on supprime les élastiques lorsque l'on un-clique
		canvas.delete(self.elastique1)
		canvas.delete(self.elastique2)

		#recréation des élastiques de la catapulte
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)

	def shoot(self):
		"""Fonction permettant de faire le shoot du projectile"""
		global compteur

		if self.posy_proj <= 450:
			self.vx = self.liste_vecteur[0]/3
			self.liste_vecteur[1] += self.gravite
			self.vy += self.liste_vecteur[1]/10
			self.posx_proj += self.vx
			self.posy_proj += self.vy
			self.posx_shift += self.vx

			self.trajectoire()
			self.shift_world()
			self.update()

			if self.posy_proj >= 449:
				time.sleep(2) #on attend 2 secondes..
				self.return_camera()

		if self.posy_proj != 450:
			fenetre.after(70, self.shoot)


	def trajectoire(self):
		"""Fonction permettant la création d'une trajectoire à chaque module 1 == 0de la position x du projectile"""

		self.point = canvas.create_oval(self.posx_proj - 15, self.posy_proj - 15, self.posx_proj, self.posy_proj, fill = 'white', outline = 'black')
		self.pointx = self.posx_proj
		self.pointy = self.posy_proj

		#puis on ajoute toutes ses valeurs dans 3 listes
		self.list_point_trajectoire_x.append(self.pointx)
		self.list_point_trajectoire_y.append(self.pointy)
		self.list_point_trajectoire.append(self.point)

	def return_camera(self):
		"""Fonction permettant le retour de la caméra lorsque l'un des projectiles est sur le sol"""

		global tour, compteur, shift_return, diff_longueur

		if compteur == 0:
			if tour == 0:
				print("return_camera pour se mettre au j2")
				diff_longueur = (catapulte1.posx - background.posx) - catapulte2.posx
				print("longueur diff", diff_longueur)
				tour = 1

			elif tour == 1:
				print("return_camera pour se mettre au j1")
				diff_longueur = (catapulte1.posx - background.posx) - catapulte1.posx
				print("longueur diff", diff_longueur)
				tour = 0

			#on calcule la valeur de shift (ici : 8px de déplacement par update )
			if diff_longueur < 0:
				shift_return = -8
			else:
				shift_return = 8

		#et on fait le shift
		background.posx += shift_return

		#obj proj1
		catapulte1.posx += shift_return
		catapulte1.x0ela += shift_return
		catapulte1.x1ela += shift_return
		catapulte1.x2ela += shift_return
		catapulte1.x3ela += shift_return
		catapulte1.x_center_ela += shift_return
		catapulte1.posx_proj_initale += shift_return
		catapulte1.posx_proj += shift_return
		for point in range(len(catapulte1.list_point_trajectoire)):
			catapulte1.list_point_trajectoire_x[point] += shift_return


		#obj proj2
		catapulte2.posx += shift_return
		catapulte2.x0ela += shift_return
		catapulte2.x1ela += shift_return
		catapulte2.x2ela += shift_return
		catapulte2.x3ela += shift_return
		catapulte2.x_center_ela += shift_return
		catapulte2.posx_proj_initale += shift_return
		catapulte2.posx_proj += shift_return
		for point in range(len(catapulte2.list_point_trajectoire)):
			catapulte2.list_point_trajectoire_x[point] += shift_return

		#on update
		self.update()

		#on incrémente le compteur
		compteur += 8

		if compteur <= abs(diff_longueur):
			fenetre.after(25, self.return_camera)

		else:
			compteur = 0


	def shift_world(self):
		"""Permet le shift du monde. Celui-ci est dirigé, seulement, par le projectile lancé."""

		#on limite le shift lorsque qu'il y a des limites(droite/gauche)
		if background.limite_droite >  (self.posx_proj + (largeur_canvas - 500)) - background.posx and background.limite_gauche < self.posx_proj - 340 - background.posx:

			#à droite
			if self.posx_shift >= 590:
				print("Shift droit")
				diff = self.posx_proj - 590

				self.posx_proj = 590

				background.posx += -diff

				if self == catapulte1:
					#quand c'est le posproj 1
					#obj proj1 SAUF PROJ1
					self.posx += -diff
					self.x0ela += -diff
					self.x1ela += -diff
					self.x2ela += -diff
					self.x3ela += -diff
					self.x_center_ela += -diff
					self.posx_proj_initale += -diff
					for point in range(len(self.list_point_trajectoire)):
						self.list_point_trajectoire_x[point] += -diff

					#obj proj2
					catapulte2.posx += -diff
					catapulte2.x0ela += -diff
					catapulte2.x1ela += -diff
					catapulte2.x2ela += -diff
					catapulte2.x3ela += -diff
					catapulte2.x_center_ela += -diff
					catapulte2.posx_proj_initale += -diff
					catapulte2.posx_proj += -diff
					for point in range(len(catapulte2.list_point_trajectoire)):
						catapulte2.list_point_trajectoire_x[point] += -diff

				else:
					#quand c'est le posproj 2
					#obj proj2 SAUF POSXPROJ2
					self.posx += -diff
					self.x0ela += -diff
					self.x1ela += -diff
					self.x2ela += -diff
					self.x3ela += -diff
					self.x_center_ela += -diff
					self.posx_proj_initale += -diff
					for point in range(len(self.list_point_trajectoire)):
						self.list_point_trajectoire_x[point] += -diff

					#obj proj1  SAUF PROJ2
					catapulte1.posx += -diff
					catapulte1.x0ela += -diff
					catapulte1.x1ela += -diff
					catapulte1.x2ela += -diff
					catapulte1.x3ela += -diff
					catapulte1.x_center_ela += -diff
					catapulte1.posx_proj_initale += -diff
					catapulte1.posx_proj += -diff
					for point in range(len(catapulte1.list_point_trajectoire)):
						catapulte1.list_point_trajectoire_x[point] += -diff


			#à gauche
			if self.posx_shift <= 250:
				print("Shift gauche")
				diff = self.posx_proj - 250

				self.posx_proj = 250

				background.posx += -diff

				if self == catapulte1:

					#obj proj1 SAUF PROJ1
					self.posx += -diff
					self.x0ela += -diff
					self.x1ela += -diff
					self.x2ela += -diff
					self.x3ela += -diff
					self.x_center_ela += -diff
					self.posx_proj_initale += -diff
					for point in range(len(self.list_point_trajectoire)):
						self.list_point_trajectoire_x[point] += -diff

					#obj proj2
					catapulte2.posx += -diff
					catapulte2.x0ela += -diff
					catapulte2.x1ela += -diff
					catapulte2.x2ela += -diff
					catapulte2.x3ela += -diff
					catapulte2.x_center_ela += -diff
					catapulte2.posx_proj_initale += -diff
					catapulte2.posx_proj += -diff
					for point in range(len(catapulte2.list_point_trajectoire)):
						catapulte2.list_point_trajectoire_x[point] += -diff

				else:
					#obj proj2 sauf POXPROJ2
					self.posx += -diff
					self.x0ela += -diff
					self.x1ela += -diff
					self.x2ela += -diff
					self.x3ela += -diff
					self.x_center_ela += -diff
					self.posx_proj_initale += -diff
					for point in range(len(self.list_point_trajectoire)):
						self.list_point_trajectoire_x[point] += -diff

					#obj proj1
					catapulte1.posx += -diff
					catapulte1.x0ela += -diff
					catapulte1.x1ela += -diff
					catapulte1.x2ela += -diff
					catapulte1.x3ela += -diff
					catapulte1.x_center_ela += -diff
					catapulte1.posx_proj_initale += -diff
					catapulte1.posx_proj += -diff
					for point in range(len(catapulte1.list_point_trajectoire)):
						catapulte1.list_point_trajectoire_x[point] += -diff

	def update(self):
		"""Fonction permettant d'update tous les objets graphiques"""

		if self.posy_proj >= 450:
			self.posy_proj = 450

		#puis on update
		#background
		canvas.coords(background.image, background.posx, background.posy)

		#catapultes
		canvas.coords(catapulte1.image, catapulte1.posx, catapulte1.posy)
		canvas.coords(catapulte2.image, catapulte2.posx, catapulte2.posy)

		#elastiques
		canvas.coords(catapulte1.elastique1, catapulte1.x0ela, catapulte1.y0ela, catapulte1.x1ela, catapulte1.y1ela)
		canvas.coords(catapulte1.elastique2, catapulte1.x2ela, catapulte1.y2ela, catapulte1.x3ela, catapulte1.y3ela)
		canvas.coords(catapulte2.elastique1, catapulte2.x0ela, catapulte2.y0ela, catapulte2.x1ela, catapulte2.y1ela)
		canvas.coords(catapulte2.elastique2, catapulte2.x2ela, catapulte2.y2ela, catapulte2.x3ela, catapulte2.y3ela)

		#positions points trajectoire
		for point in range(len(catapulte1.list_point_trajectoire)):
			canvas.coords(catapulte1.list_point_trajectoire[point], catapulte1.list_point_trajectoire_x[point] + 15, catapulte1.list_point_trajectoire_y[point] + 15, catapulte1.list_point_trajectoire_x[point] + 30, catapulte1.list_point_trajectoire_y[point] + 30)
		for point in range(len(catapulte2.list_point_trajectoire)):
			canvas.coords(catapulte2.list_point_trajectoire[point], catapulte2.list_point_trajectoire_x[point] + 15, catapulte2.list_point_trajectoire_y[point] + 15, catapulte2.list_point_trajectoire_x[point] + 30, catapulte2.list_point_trajectoire_y[point] + 30)

		#projectiles
		canvas.coords(catapulte1.image_proj, catapulte1.posx_proj, catapulte1.posy_proj)
		canvas.coords(catapulte2.image_proj, catapulte2.posx_proj, catapulte2.posy_proj)


class World():
	"""Classe permettant l'affichage du monde"""

	def __init__(self, posx, posy, image):
		"""Constructeur de la classe World"""

		#world
		self.image = canvas.create_image(posx, posy, image = image, anchor = "nw")
		self.posx = posx
		self.posy = posy
		self.limite_gauche = 0
		self.limite_droite = 2560 #largeur monde x


background = World(0, -250, background_img)

catapulte1 = Catapulte(368, 290, catapulte_left_img, 387, 327, 389, 331,   428, 327, 432, 331,     368, 300, red_bird_img)
catapulte2 = Catapulte(696, 290, catapulte_right_img, 698, 327, 702, 331,   739, 327, 743, 331,    700, 300, red_bird_mirror_img)

#lignes limite du shift
limite_shift_gauche = canvas.create_line(590,hauteur_canvas,590,0)
limite_shift_gauche = canvas.create_line(250,hauteur_canvas,250,0)

canvas.bind("<Button-1>", catapulte1.click) #lorsque l'on clique sur la catapulte 1
canvas.bind("<ButtonRelease-1>", catapulte1.unclick) #lorsqu'on relâche le clique sur la catapulte 1
canvas.bind("<B1-Motion>", catapulte1.drag_obj) #lorsque l'on clique sur la catapulte 1

canvas.bind("<Button-3>", catapulte2.click) #lorsque l'on clique sur la catapulte 2
canvas.bind("<ButtonRelease-3>", catapulte2.unclick) #lorsqu'on relâche le clique sur la catapulte 2
canvas.bind("<B3-Motion>",catapulte2.drag_obj) #lorsque l'on clique sur la catapulte 2

#admin
fenetre.mainloop()
