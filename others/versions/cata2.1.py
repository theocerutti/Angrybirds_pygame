#!/usr/bin/env python
#-*- coding: utf-8 -*-

#IDEE DE DVPT
#pouvoirs : vitesse balle ++, barrière, possibilité de détruire la boule adverse, projecticles spéciaux, truc pour recup vie, truc pour augmenter sa vitesse
#système de vie des joueurs
#système de gain d'argent permettant d'acheter des pouvoirs, vies, armure..  -> si on améliore l'armure la catapulte aura un new design
#sytème de barrière

#CE QU'IL FAUT FAIRE
#faire de meilleure collisions
#systeme de vie

#PROBLEME RENCONTRES/BUGS
#sys de collisions complety bugged
#lorsque que je shoot le proj va un peu dans le sol voir dans la fonc shoot
#la corde de la cata droite est plus petite que celle de la cata gauche

#PROBLEME ET LEURS SOLUTION
#* le shift ne peut se faire car la pos_x_obj ne fait que baisser, ce systeme de shift ne va pas avec les projectiles --> j'ai ajouté un intermediaire posx_shift qui elle ne se remet pas a 500
#* si je shift deux fois en mm temps (ex: haut/droite) y'a un bug car il affiche l'image quand y'a un shift mais quand il y eb a deux alors le shift en premier prend le dessus./ faire un fonc affichage qui se fait a la fin --> j'ai enlevé les shifts haut/bas
#* lors du shift les positions ne sont pas changés (même si l'affichage lui est modifié) --> j'ai   juste return la valeur
#* plusieurs bug de shift bizarres : j'avais oublié de reinitialiser self.pox_shift dans le fonc de reset !
#* faire un bon shift -> lorsque je prends proj1 -> shift sur proj2/cata2; si je prends proj2 -> shift sur proj1/cata1 ---> j'ai utilisé
#* pas de shift pour la trajectoire --> j'avais oublié de mettre les pts_trajectoire des deux cata (j'avais juste mis self)

from tkinter import *
from math import *
import install_font #permet d'installer une font pour par la suite l'utiliser
import time

fenetre = Tk()

#fenetre.iconbitmap("mon_icone.ico") # on change l'icône de notre fenêtre
fenetre.geometry('1000x800') # on change les dimensions de notre fenêtre
fenetre.title('Jeu des catapultes') #on change le titre du jeu
#on change la couleur de la fenetre
fenetre.configure(bg = 'black')

hauteur_canvas, largeur_canvas = 840, 680
canvas = Canvas(fenetre, width = hauteur_canvas, height = largeur_canvas, bg ='black')
canvas.pack()


#----------------------------------------------------------------------------------------------------
# VARIABLES

#fichier_source/dest pour l'installation de la font angrybirds
f_source = 'lib/font/angrybirds.ttf'
dir_dest = '/Windows\Fonts'


#----------------------------------------------------------------------------------------------------
# IMAGES
catapulte_left_img = PhotoImage(file = "lib/image/cata_left_mini_parted.gif")
catapulte_right_img = PhotoImage(file = "lib/image/cata_right_mini_parted.gif")
part_cata_left_img = PhotoImage(file = "lib/image/part_cata_left.gif")
part_cata_right_img = PhotoImage(file = "lib/image/part_cata_right.gif")
red_bird_img = PhotoImage(file = "lib/image/red_bird_mini.gif")
blue_bird_img = PhotoImage(file = "lib/image/blue_bird_mini.gif")
background_img = PhotoImage(file = "lib/image/world.gif")
quit_button_img = PhotoImage(file = "lib/image/quit_button.gif")

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

	def __init__(self, posx, posy, image, x0ela, y0ela, x1ela, y1ela, x2ela, y2ela, x3ela, y3ela, posx_projectile, posy_projectile, image_projectile, image_part, posx_part, posy_part, color_point):
		"""Constructeur de la classe catapulte
			Arguments:
				- posx, posy : position x et y de l'objet
				- image : image de l'objet de type PhotoImage
				- liste : liste utilisée et dédiée à l'objet
				- x0ela, y1ela,..., = coordonnées des élastiques"""

		#coordonnées de la catapulte
		self.posx = posx
		self.posy = posy

		#coordonnées de la partie de la catapulte
		self.posx_part = posx_part
		self.posy_part = posy_part

		#infos catapultes, bool drag
		self.drag = False
		self.largeur_img = 38
		self.hauteur_img = 122 #c'est la hauteur de l'image des catapultes

		#position,vecteur, gravité du projectile
		self.posx_proj = posx_projectile
		self.posy_proj = posy_projectile
		self.posx_proj_initale = posx_projectile #c'est la position initale du projectile, elle restera alors constante
		self.posy_proj_initale = posy_projectile
		self.posx_shift = posx_projectile #c'est la position pour le shift elle ne sera pas utilisé pour l'affichage de la position
		self.gravite = 10
		self.vy = 0
		self.vx = 0

		#positions x y des élastiques
		self.x0ela, self.y0ela, self.x1ela, self.y1ela = x0ela, y0ela, x1ela, y1ela
		self.x2ela, self.y2ela, self.x3ela, self.y3ela = x2ela, y2ela, x3ela, y3ela
		self.x_center_ela, self.y_center_ela = self.x0ela + 20, self.y0ela #ordonnées du centre "d'inertie" entre les deux élastiques

		#crétion des elastiques
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)

		#création catapultes/projectiles
		self.image = canvas.create_image(self.posx, self.posy, image = image , anchor = "nw") #on met anchor = NW pour mettre le point d'ancrage en haut à droite
		self.image_proj = canvas.create_image(self.posx_proj, self.posy_proj, image = image_projectile, anchor = 'nw')
		#et sa partie
		self.image_part = canvas.create_image(self.posx_part, self.posy_part, image = image_part , anchor = "nw")

		#trajectoire des points
		self.list_point_trajectoire = []
		self.list_point_trajectoire_x = []
		self.list_point_trajectoire_y = []
		#la couleur du outline des points de la trajectoire
		self.color_point = color_point

		#vie des catapultes
		self.vie = 3

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

		print("Click x ->", self.souris_x - world.posx,"\nClick y ->", self.souris_y - world.posy - 200)

		if self.posx <= self.souris_x <= self.posx + self.largeur_img and self.posy <= self.souris_y <= self.posy + self.hauteur_img: #si je clique sur la catapulte alors on met self.drag à True
			self.drag = True

			#on (re)met le projectile dans sa position de base
			self.reset_pos_proj()
			canvas.coords(self.image_proj, self.posx_proj, self.posy_proj)

		#si je clique sur le bouton quitter
		if 0 <= self.souris_x <= 60 and 0 <= self.souris_y <= 60:
			print("Arrêt du programme")
			fenetre.destroy()

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
			canvas.coords(self.image_proj, self.souris_x - 15, self.souris_y - 15) #30 c'est la moitié de la taille de l'image du projectile

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

		if self.posy_proj >= 520:
			self.posy_proj = 520

		if self.posy_proj == 520:
			time.sleep(1.5) #on attend 1.5 secondes..
			world.return_camera()

		elif self.posy_proj <= 520:
			self.vx = self.liste_vecteur[0]/2
			self.liste_vecteur[1] += self.gravite
			self.vy += self.liste_vecteur[1]/10
			self.check_collision()
			self.posx_proj += self.vx
			self.posy_proj += self.vy
			self.posx_shift += self.vx

			self.trajectoire()
			world.shift_world()
			world.update()

		if self.posy_proj != 520:
			fenetre.after(55, self.shoot)

	def trajectoire(self):
		"""Fonction permettant la création d'une trajectoire à chaque module 1 == 0de la position x du projectile"""

		self.point = canvas.create_oval(self.posx_proj - 10, self.posy_proj - 10, self.posx_proj, self.posy_proj, fill = 'white', width = 2, outline = self.color_point)
		self.pointx = self.posx_proj
		self.pointy = self.posy_proj

		#puis on ajoute toutes ses valeurs dans 3 listes
		self.list_point_trajectoire_x.append(self.pointx)
		self.list_point_trajectoire_y.append(self.pointy)
		self.list_point_trajectoire.append(self.point)

	def move(self, event, direction):
		"""Fonction permettant de bouger vers la droite/gauche si et seulement si c'est son tour."""

		#si c'est le tour du joueur 1 alors on ne bouge que la cata 1
		if world.tour == 0:
			self = catapulte1
		else:
			self = catapulte2

		#si je vais suis hors de la limite à droite et que je clique sur le bouton de droite alors:
		if self.posx < 590 - self.largeur_img and direction == 1:
			move = 10
		#si je vais suis hors de la limite de gauche et que je clique sur le bouton de gauche alors:
		elif self.posx > 250 and direction == -1:
			move = -10
		#sinon je ne bouge plus, je suis en dehors des limites
		else:
			move = 0

		#on ajoute 10 à toutes les coordonnées en x de la catapulte/proj
		self.posx += move
		self.posx_part += move
		self.x0ela += move
		self.x1ela += move
		self.x2ela += move
		self.x3ela += move
		self.x_center_ela += move
		self.posx_proj += move
		self.posx_proj_initale += move

		#et on update
		world.update()

	def check_collision(self):
		"""Fonction permettant de voir si il y a collision entre les catapultes/projectiles"""

		if world.tour == 0:
			if catapulte1.posx_proj > catapulte2.posx and catapulte1.posx_proj < catapulte2.posx + catapulte2.largeur_img and catapulte1.posy_proj + 30 > catapulte2.posy and catapulte1.posy_proj < catapulte2.posy + catapulte2.hauteur_img:
				
				catapulte1.vx = 0
				catapulte1.vy = 0
				catapulte2.vie -= 1
				print("La catapulte2 a été touché, elle ne lui reste plus que", catapulte2.vie, "vies !")

		elif world.tour == 1:
			if catapulte2.posx_proj > catapulte1.posx and catapulte2.posx_proj < catapulte1.posx + catapulte1.largeur_img and catapulte2.posy_proj + 30 > catapulte1.posy and catapulte2.posy_proj < catapulte1.posy + catapulte1.hauteur_img:
				
				catapulte2.vx = 0
				catapulte1.vie -= 1
				print("La catapulte1 a été touché, elle ne lui reste plus que", catapulte1.vie, "vies !")

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
		
		#tour du joueur, quand il est à 0 -> cest le tour du J0 (à gauche) quand il est à 1 c'est au tour du J1 (à droite)
		self.tour = 0
		self.compteur = 0

		#text des tours, pour avoir la font angrybirds il faut installer la font dans le dossier font de windows
		install_font.install_font(f_source, dir_dest)#on installe la font angrybirds
		self.text_tour = canvas.create_text(420,100,fill="black", font = ('angrybirds', 35), text="TOUR DU JOUEUR 1")

		#on affiche le bouton quitter
		self.quit_button = canvas.create_image(0, 0, image = quit_button_img, anchor = "nw")

	def return_camera(self):
		"""Fonction permettant le retour de la caméra lorsque l'un des projectiles est sur le sol"""

		if self.compteur == 0:
			if self.tour == 0:
				canvas.itemconfigure(self.text_tour, text = "TOUR DU JOUEUR 2", font = ('angrybirds', 35))
				self.diff_longueur = (catapulte1.posx - self.posx) - catapulte2.posx
				print("longueur diff", self.diff_longueur)
				self.tour = 1

			elif self.tour == 1:
				canvas.itemconfigure(self.text_tour, text = "TOUR DU JOUEUR 1", font = ('angrybirds', 35))
				self.diff_longueur = -self.posx
				print("longueur diff", self.diff_longueur)
				self.tour = 0

			#on calcule la valeur de shift (ici : 10px de déplacement par update )
			if self.diff_longueur < 0:
				self.shift_return = -6
			else:
				self.shift_return = 6

		#et on fait le shift
		self.posx += self.shift_return

		#obj proj1
		catapulte1.posx += self.shift_return
		catapulte1.posx_part += self.shift_return
		catapulte1.x0ela += self.shift_return
		catapulte1.x1ela += self.shift_return
		catapulte1.x2ela += self.shift_return
		catapulte1.x3ela += self.shift_return
		catapulte1.x_center_ela += self.shift_return
		catapulte1.posx_proj_initale += self.shift_return
		catapulte1.posx_proj += self.shift_return
		for point in range(len(catapulte1.list_point_trajectoire)):
			catapulte1.list_point_trajectoire_x[point] += self.shift_return


		#obj proj2
		catapulte2.posx += self.shift_return
		catapulte2.posx_part += self.shift_return
		catapulte2.x0ela += self.shift_return
		catapulte2.x1ela += self.shift_return
		catapulte2.x2ela += self.shift_return
		catapulte2.x3ela += self.shift_return
		catapulte2.x_center_ela += self.shift_return
		catapulte2.posx_proj_initale += self.shift_return
		catapulte2.posx_proj += self.shift_return
		for point in range(len(catapulte2.list_point_trajectoire)):
			catapulte2.list_point_trajectoire_x[point] += self.shift_return

		#on update
		self.update()

		#on incrémente le compteur
		self.compteur += 6

		if self.compteur <= abs(self.diff_longueur):
			fenetre.after(10, self.return_camera)

		else:
			self.compteur = 0

	def shift_world(self):
		"""Permet le shift du monde. Celui-ci est dirigé, seulement, par le projectile lancé."""

		if self.tour == 0:
			self = catapulte1
		else:
			self = catapulte2

		#on limite le shift lorsque qu'il y a des limites(droite/gauche)
		if world.limite_droite >  (self.posx_proj + (largeur_canvas - 500)) - world.posx and world.limite_gauche < self.posx_proj - 340 - world.posx:

			#à droite
			if self.posx_shift >= 590:
				print("Shift droit")
				diff = self.posx_proj - 590

				self.posx_proj = 590

				world.posx += -diff

				if self == catapulte1:
					#quand c'est le posproj 1
					#obj proj1 SAUF PROJ1
					self.posx += -diff
					self.posx_part += -diff
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
					catapulte2.posx_part += -diff
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
					self.posx_part += -diff
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
					catapulte1.posx_part += -diff
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

				world.posx += -diff

				if self == catapulte1:

					#obj proj1 SAUF PROJ1
					self.posx += -diff
					self.posx_part += -diff
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
					catapulte2.posx_part += -diff
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
					self.posx_part += -diff
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
					catapulte1.posx_part += -diff
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

		#puis on update
		#background
		canvas.coords(world.image, world.posx, world.posy)

		#catapultes/projectiles entremêlé
		canvas.coords(catapulte1.image, catapulte1.posx, catapulte1.posy)
		canvas.coords(catapulte1.image_proj, catapulte1.posx_proj, catapulte1.posy_proj)
		canvas.coords(catapulte1.image_part, catapulte1.posx_part, catapulte1.posy_part)

		canvas.coords(catapulte2.image, catapulte2.posx, catapulte2.posy)
		canvas.coords(catapulte2.image_proj, catapulte2.posx_proj, catapulte2.posy_proj)
		canvas.coords(catapulte2.image_part, catapulte2.posx_part, catapulte2.posy_part)

		#elastiques
		canvas.coords(catapulte1.elastique1, catapulte1.x0ela, catapulte1.y0ela, catapulte1.x1ela, catapulte1.y1ela)
		canvas.coords(catapulte1.elastique2, catapulte1.x2ela, catapulte1.y2ela, catapulte1.x3ela, catapulte1.y3ela)
		canvas.coords(catapulte2.elastique1, catapulte2.x0ela, catapulte2.y0ela, catapulte2.x1ela, catapulte2.y1ela)
		canvas.coords(catapulte2.elastique2, catapulte2.x2ela, catapulte2.y2ela, catapulte2.x3ela, catapulte2.y3ela)

		#positions points trajectoire
		for point in range(len(catapulte1.list_point_trajectoire)):
			canvas.coords(catapulte1.list_point_trajectoire[point], catapulte1.list_point_trajectoire_x[point] + 10, catapulte1.list_point_trajectoire_y[point] + 10, catapulte1.list_point_trajectoire_x[point] + 20, catapulte1.list_point_trajectoire_y[point] + 20)
		for point in range(len(catapulte2.list_point_trajectoire)):
			canvas.coords(catapulte2.list_point_trajectoire[point], catapulte2.list_point_trajectoire_x[point] + 10, catapulte2.list_point_trajectoire_y[point] + 10, catapulte2.list_point_trajectoire_x[point] + 20, catapulte2.list_point_trajectoire_y[point] + 20)


world = World(0, -200, background_img)

catapulte1 = Catapulte(368, 420, catapulte_left_img, 375, 439, 377, 441,   402, 439, 404, 441,     371, 420, red_bird_img, part_cata_left_img, 368, 420, 'red')
catapulte2 = Catapulte(1696, 420, catapulte_right_img, 1698, 439, 1700, 441,   1724, 439, 1726, 441,    1699, 420, blue_bird_img, part_cata_right_img, 1696, 420, 'blue')

#lignes limite du shift
limite_shift_gauche = canvas.create_line(590,hauteur_canvas,590,0)
limite_shift_gauche = canvas.create_line(250,hauteur_canvas,250,0)

canvas.bind("<Button-1>", catapulte1.click) #lorsque l'on clique sur la catapulte 1
canvas.bind("<ButtonRelease-1>", catapulte1.unclick) #lorsqu'on relâche le clique sur la catapulte 1
canvas.bind("<B1-Motion>", catapulte1.drag_obj) #lorsque l'on clique sur la catapulte 1

canvas.bind("<Button-3>", catapulte2.click) #lorsque l'on clique sur la catapulte 2
canvas.bind("<ButtonRelease-3>", catapulte2.unclick) #lorsqu'on relâche le clique sur la catapulte 2
canvas.bind("<B3-Motion>",catapulte2.drag_obj) #lorsque l'on clique sur la catapulte 2

#move des catapultes, ces binds sont utilisés aussi pour la cata2 (cf la fonc), on utilise des arguments
fenetre.bind("<Left>", lambda event, direction = -1: catapulte1.move(event, direction)) #mouvement gauche, flèche gauche
fenetre.bind("<Right>", lambda event, direction = 1: catapulte1.move(event, direction)) #mouvement droite, flèche droite

fenetre.mainloop()
