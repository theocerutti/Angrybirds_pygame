#!/usr/bin/env python
#-*- coding: utf-8 -*-

#IDEE DE DVPT
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

#CE QU'IL FAUT FAIRE
#faire les limites du level et que le shift ne se fasse pas
#déplacer la cata de gauche au milieu de l'écran et l'autre plus loin
#si on tire avec une cata, lorsque le proj tombe et ne bouge plus alors la camera doit se recentrer a l'autre cata
#faire la trajectoire, chaque multiple de 10 de vx -> create_oval
#

#PROBLEME RENCONTRES
#
#
#
#

#PROBLEME ET LEURS SOLUTION

from tkinter import *
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



#----------------------------------------------------------------------------------------------------
# IMAGES
catapulte_left_img = PhotoImage(file = "lib/image/cata_left.gif")
catapulte_right_img = PhotoImage(file = "lib/image/cata_right.gif")
red_bird_img = PhotoImage(file = "lib/image/red_bird.gif")
red_bird_mirror_img = PhotoImage(file = "lib/image/red_bird_mirror.gif")
background_img = PhotoImage(file = "lib/image/world.gif")


#----------------------------------------------------------------------------------------------------
# FONCTIONS


def calcul_vector(v0x, v1x, v0y, v1y):
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
		self.x_center_ela, self.y_center_ela = self.x0ela + 20, self.y0ela #ordonnées du centre "d'inertie" entre les deux élastiques

		#crétion des elastiques
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)

		#position,vecteur, gravité et création du projectile
		self.stop_proj = False
		self.posx_proj = posx_projectile
		self.posy_proj = posy_projectile
		self.posx_proj_initale = posx_projectile #c'est la position initale du projectile, elle restera alors constante
		self.posy_proj_initale = posy_projectile
		self.image_proj = canvas.create_image(self.posx_proj, self.posy_proj, image = image_projectile, anchor = 'nw')
		self.gravite = 10
		self.vy = 0
		self.vx = 0

	def click(self, event):
		"""Fonction permettant de voir si on clique sur l'objet"""

		self.souris_x, self.souris_y = event.x, event.y

		print("Click x ->", self.souris_x,"\nClick y ->", self.souris_y)

		self.x, self.y = canvas.coords(self.image)

		if self.x <= self.souris_x <= self.x + self.hauteur_img and self.y <= self.souris_y <= self.y + self.hauteur_img: #si je clique sur la catapulte alors on met self.drag à True
			self.drag = True

			#on (re)met le projectile dans sa position de base
			self.posx_proj = self.posx_proj_initale
			self.posy_proj = self.posy_proj_initale
			canvas.coords(self.image_proj, self.posx_proj_initale, self.posy_proj_initale)

	def unclick(self, event):
		"""Fonction permettant de détecter lorsque l'on relâche le clique"""

		if self.drag == True:
			self.liste_vecteur = calcul_vector(self.x_center_ela, self.souris_x, self.y_center_ela, self.souris_y)
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

	def shoot(self):
		"""Fonction permettant de faire le shoot du projectile"""

		#si le projectile n'est pas au sol, c'est à dire lorsqu'il est lancé
		if self.posy_proj < 450:

			self.vx = self.liste_vecteur[0]/3
			self.liste_vecteur[1] += self.gravite
			self.vy += self.liste_vecteur[1]/10
			self.posx_proj += self.vx
			self.posy_proj += self.vy

			background.shift_world(self.posx_proj, self.posy_proj)

			canvas.coords(self.image_proj, self.posx_proj, self.posy_proj)

			if self.posy_proj < 450: #si le projectile est au sol, il n'a plus besoin d'être animé donc on l'arrête
				fenetre.after(70, self.shoot)

		#si le projectile est au sol
		else:
			self.pos_proj = 450


class World:
	"""Classe permettant le shift de tous les objets graphiques. Le projectile sera l'objet au centre de la caméra !"""

	def __init__(self, posx, posy, image):
		"""Constructeur"""

		self.image = canvas.create_image(posx, posy, image = image, anchor = "nw")
		self.posx = posx
		self.posy = posy
		self.limite_gauche = 0
		self.limite_droite = 1280 #largeur monde x

	def calcul_normal_obj_shift_x(self, shift_x, obj, obj_posx0, obj_posy0):
		"""Fonction permettant le calcul du shift en x des objets normaux, c'est à dire des images"""

		obj_posx0 += shift_x
		canvas.coords(obj, obj_posx0, obj_posy0)

	def calcul_normal_obj_shift_y(self, shift_y, obj, obj_posx0, obj_posy0):
		"""Fonction permettant le calcul du shift en y"""

		obj_posy0 += shift_y
		canvas.coords(obj, obj_posx0, obj_posy0)

	def calcul_spe_obj_shift_x(self, shift_x, obj, obj_posx0, obj_posy0, obj_posx1, obj_posy1):
		"""Fonction permettant le calcul du shift en x, c'est à dire des objets graphiques : lignes, carrées...."""

		obj_posx0 += shift_x
		obj_posx1 += shift_x
		canvas.coords(obj, obj_posx0, obj_posy0, obj_posx1, obj_posy1)

	def calcul_spe_obj_shift_y(self, shift_y, obj, obj_posx0, obj_posy0, obj_posx1, obj_posy1):
		"""Fonction permettant le calcul du shift en y, c'est à dire des objets graphiques : lignes, carrés...."""

		obj_posy0 += shift_y
		obj_posy1 += shift_y
		canvas.coords(obj, obj_posx0, obj_posy0, obj_posx1, obj_posy1)

	def shift_world(self, obj_posx, obj_posy):
		"""Permet le shift du monde. Celui-ci est dirigé, seulement, par le projectile lancé."""

		#on limite le shift lorsque qu'il y a des limites(droite/gauche)
		if self.limite_droite >  (obj_posx + (largeur_canvas - 500)) - self.posx and self.limite_gauche < obj_posx - 340 - self.posx:

			#à droite
			if obj_posx > 500:
				print("shift droit")
				diff = obj_posx - 500
				obj_posx = 500
				self.calcul_normal_obj_shift_x(-diff, self.image, self.posx, self.posy)
				self.calcul_normal_obj_shift_x(-diff, catapulte1.image, catapulte1.posx, catapulte1.posy)
				self.calcul_normal_obj_shift_x(-diff, catapulte2.image, catapulte2.posx, catapulte2.posy)
				#self.calcul_normal_obj_shift_x(-diff, catapulte1.image_proj, catapulte1.posx_proj, catapulte1.posy_proj)
				#self.calcul_normal_obj_shift_x(-diff, catapulte2.image_proj, catapulte2.posx_proj, catapulte2.posy_proj)
				self.calcul_spe_obj_shift_x(-diff, catapulte1.elastique1, catapulte1.x0ela, catapulte1.y0ela, catapulte1.x1ela, catapulte1.y1ela)
				self.calcul_spe_obj_shift_x(-diff, catapulte1.elastique2, catapulte1.x2ela, catapulte1.y2ela, catapulte1.x3ela, catapulte1.y3ela)
				self.calcul_spe_obj_shift_x(-diff, catapulte2.elastique1, catapulte2.x0ela, catapulte2.y0ela, catapulte2.x1ela, catapulte2.y1ela)
				self.calcul_spe_obj_shift_x(-diff, catapulte2.elastique2, catapulte2.x2ela, catapulte2.y2ela, catapulte2.x3ela, catapulte2.y3ela)

			#à gauche
			if obj_posx < 340:
				print("shift gauche")
				diff =  340 - obj_posx
				obj_posx = 340
				self.calcul_normal_obj_shift_x(diff, self.image, self.posx, self.posy)
				self.calcul_normal_obj_shift_x(diff, catapulte1.image, catapulte1.posx, catapulte1.posy)
				self.calcul_normal_obj_shift_x(diff, catapulte2.image, catapulte2.posx, catapulte2.posy)
				#self.calcul_normal_obj_shift_x(diff, catapulte1.image_proj, catapulte1.posx_proj, catapulte1.posy_proj)
				#self.calcul_normal_obj_shift_x(diff, catapulte2.image_proj, catapulte2.posx_proj, catapulte2.posy_proj)
				self.calcul_spe_obj_shift_x(diff, catapulte1.elastique1, catapulte1.x0ela, catapulte1.y0ela, catapulte1.x1ela, catapulte1.y1ela)
				self.calcul_spe_obj_shift_x(diff, catapulte1.elastique2, catapulte1.x2ela, catapulte1.y2ela, catapulte1.x3ela, catapulte1.y3ela)
				self.calcul_spe_obj_shift_x(diff, catapulte2.elastique1, catapulte2.x0ela, catapulte2.y0ela, catapulte2.x1ela, catapulte2.y1ela)
				self.calcul_spe_obj_shift_x(diff, catapulte2.elastique2, catapulte2.x2ela, catapulte2.y2ela, catapulte2.x3ela, catapulte2.y3ela)

			#en haut
			if obj_posy < 100:
				print("shift haut")
				diff =  100 - obj_posy
				obj_posy = 100
				self.calcul_normal_obj_shift_y(diff, self.image, self.posx, self.posy)
				self.calcul_normal_obj_shift_y(diff, catapulte1.image, catapulte1.posx, catapulte1.posy)
				self.calcul_normal_obj_shift_y(diff, catapulte2.image, catapulte2.posx, catapulte2.posy)
				#self.calcul_normal_obj_shift_y(diff, catapulte1.image_proj, catapulte1.posx_proj, catapulte1.posy_proj)
				#self.calcul_normal_obj_shift_y(diff, catapulte2.image_proj, catapulte2.posx_proj, catapulte2.posy_proj)
				self.calcul_spe_obj_shift_y(diff, catapulte1.elastique1, catapulte1.x0ela, catapulte1.y0ela, catapulte1.x1ela, catapulte1.y1ela)
				self.calcul_spe_obj_shift_y(diff, catapulte1.elastique2, catapulte1.x2ela, catapulte1.y2ela, catapulte1.x3ela, catapulte1.y3ela)
				self.calcul_spe_obj_shift_y(diff, catapulte2.elastique1, catapulte2.x0ela, catapulte2.y0ela, catapulte2.x1ela, catapulte2.y1ela)
				self.calcul_spe_obj_shift_y(diff, catapulte2.elastique2, catapulte2.x2ela, catapulte2.y2ela, catapulte2.x3ela, catapulte2.y3ela)

			#à bas
			if obj_posy > 580:
				print("shift bas")
				diff =  580 - obj_posy
				obj_posy = 580
				self.calcul_normal_obj_shift_y(diff, self.image, self.posx, self.posy)
				self.calcul_normal_obj_shift_y(diff, catapulte1.image, catapulte1.posx, catapulte1.posy)
				self.calcul_normal_obj_shift_y(diff, catapulte2.image, catapulte2.posx, catapulte2.posy)
				#self.calcul_normal_obj_shift_y(diff, catapulte1.image_proj, catapulte1.posx_proj, catapulte1.posy_proj)
				#self.calcul_normal_obj_shift_y(diff, catapulte2.image_proj, catapulte2.posx_proj, catapulte2.posy_proj)
				self.calcul_spe_obj_shift_y(diff, catapulte1.elastique1, catapulte1.x0ela, catapulte1.y0ela, catapulte1.x1ela, catapulte1.y1ela)
				self.calcul_spe_obj_shift_y(diff, catapulte1.elastique2, catapulte1.x2ela, catapulte1.y2ela, catapulte1.x3ela, catapulte1.y3ela)
				self.calcul_spe_obj_shift_y(diff, catapulte2.elastique1, catapulte2.x0ela, catapulte2.y0ela, catapulte2.x1ela, catapulte2.y1ela)
				self.calcul_spe_obj_shift_y(diff, catapulte2.elastique2, catapulte2.x2ela, catapulte2.y2ela, catapulte2.x3ela, catapulte2.y3ela)



background = World(0, -250, background_img)
#cata coord gauche d'avant : catapulte1 = Catapulte(400, 290, catapulte_left_img, 96, 327, 100, 331,   137, 327, 141, 331,      80, 300, red_bird_img)
catapulte1 = Catapulte(400, 290, catapulte_left_img, 417, 327, 421, 331,   460, 327, 464, 331,      400, 300, red_bird_img)
catapulte2 = Catapulte(696, 290, catapulte_right_img, 698, 327, 702, 331,   739, 327, 743, 331,      700, 300, red_bird_mirror_img)

canvas.bind("<Button-1>", catapulte1.click) #lorsque l'on clique sur la catapulte 1
canvas.bind("<ButtonRelease-1>", catapulte1.unclick) #lorsqu'on relâche le clique sur la catapulte 1
canvas.bind("<B1-Motion>", catapulte1.drag_obj) #lorsque l'on clique sur la catapulte 1

canvas.bind("<Button-3>", catapulte2.click) #lorsque l'on clique sur la catapulte 2
canvas.bind("<ButtonRelease-3>", catapulte2.unclick) #lorsqu'on relâche le clique sur la catapulte 2
canvas.bind("<B3-Motion>",catapulte2.drag_obj) #lorsque l'on clique sur la catapulte 2

#admin
fenetre.mainloop()
