#!/usr/bin/env python
#-*- coding: utf-8 -*-

#CE QU'IL FAUT FAIRE
#faire l'help


#PROBLEME RENCONTRES/BUGS
#comme le return camera remet toujours la cata au milieu alors quand on bouge la cata vers la gauche et qu'il y a un return camera et bien on sort de l'écran -> je doit alors faire que si y'a une limite y'a plus de return camera -> non en faite je dois surtout trouver la bonne formule pour que diff_longuer prenne en compte une certaine limite
#lorsque proj1 reste sur cata2 --> au changement de tour --> perd une vie

#PROBLEME ET LEURS SOLUTION
#* le shift ne peut se faire car la pos_x_obj ne fait que baisser, ce systeme de shift ne va pas avec les projectiles --> j'ai ajouté un intermediaire posx_shift qui elle ne se remet pas a 500
#* si je shift deux fois en mm temps (ex: haut/droite) y'a un bug car il affiche l'image quand y'a un shift mais quand il y eb a deux alors le shift en premier prend le dessus./ faire un fonc affichage qui se fait a la fin --> j'ai enlevé les shifts haut/bas
#* lors du shift les positions ne sont pas changés (même si l'affichage lui est modifié) --> j'ai   juste return la valeur
#* plusieurs bug de shift bizarres : j'avais oublié de reinitialiser self.pox_shift dans le fonc de reset !
#* faire un bon shift -> lorsque je prends proj1 -> shift sur proj2/cata2; si je prends proj2 -> shift sur proj1/cata1 ---> j'ai utilisé
#* pas de shift pour la trajectoire --> j'avais oublié de mettre les pts_trajectoire des deux cata (j'avais juste mis self)
#*faire que le camera return mette toujours la cata au milieu -Wvoir code
#*#lorsque que je shoot le proj va un peu dans le sol voir dans la fonc shoot --> voir code

from tkinter import *
from math import *
import install_font #permet d'installer une font pour par la suite l'utiliser
import time

fenetre = Tk()

try:
	fenetre.iconbitmap("lib/image/icone.ico") # on change l'icône de notre fenêtre
except:
	print("[BUG] Le chargement de l'icône a échoué. Êtes-vous sur Linux ?")

fenetre.geometry('1000x800') # on change les dimensions de notre fenêtre
fenetre.title('Jeu des catapultes') #on change le titre du jeu
#on change la couleur de la fenetre
fenetre.configure(bg = 'black')

hauteur_canvas, largeur_canvas = 840, 680
canvas = Canvas(fenetre, width = hauteur_canvas, height = largeur_canvas, bg ='black')
canvas.pack()

#----------------------------------------------------------------------------------------------------
# IMAGES
catapulte_left_img = PhotoImage(file = "lib/image/cata_left_parted.gif")
catapulte_right_img = PhotoImage(file = "lib/image/cata_right_parted.gif")
part_cata_left_img = PhotoImage(file = "lib/image/part_cata_left.gif")
part_cata_right_img = PhotoImage(file = "lib/image/part_cata_right.gif")
red_bird_img = PhotoImage(file = "lib/image/red_bird.gif")
blue_bird_img = PhotoImage(file = "lib/image/blue_bird.gif")
background_img = PhotoImage(file = "lib/image/world.gif")
quit_button_img = PhotoImage(file = "lib/image/quit_button.gif")
help_button_img = PhotoImage(file = "lib/image/button_help.gif")
life_full_img = PhotoImage(file = "lib/image/life_full.gif")
life_2_img = PhotoImage(file = "lib/image/life_2.gif")
life_1_img = PhotoImage(file = "lib/image/life_1.gif")
no_life_img = PhotoImage(file = "lib/image/no_life.gif")

#----------------------------------------------------------------------------------------------------
# VARIABLES

#fichier source et de destination pour l'installation de la font 'angrybirds'
f_source = 'lib/font/angrybirds.ttf'
dir_dest = '/Windows/Fonts'

#liste des images des images des vies: 3, 2, 1, 0 coeurs
list_img_life = [life_full_img, life_2_img, life_1_img, no_life_img]


#----------------------------------------------------------------------------------------------------
# FONCTIONS


def calcul_vector(v0x, v1x, v0y, v1y):
	"""Fonction permettant de calculer un vecteur"""

	vecteur_x = v0x - v1x
	vecteur_y = v0y - v1y
	print("Impulsion x ->",vecteur_y,"\nImpulsion y ->", vecteur_x)
	list_v = [vecteur_x, vecteur_y]

	return list_v

def destroy_fen_when_win(event):
	"""Fonction permettant l'arrêt du programme lorsque qu'un joueur n'a plus de vie et que l'on tape sur la touche entrée"""

	if catapulte1.life <= 0 or catapulte2.life <= 0:
		print("Arrêt du programme ! --> entrée")
		fenetre.destroy()


#----------------------------------------------------------------------------------------------------
# CLASSES

class Catapulte:
	"""Classe permettant la gestion de la catapulte"""

	def __init__(self, posx, posy, image, x0ela, y0ela, x1ela, y1ela, x2ela, y2ela, x3ela, y3ela, posx_projectile, posy_projectile, image_projectile, image_part, posx_part, posy_part, color_point, list_img_life, life_posx, life_posy):
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

		#infos catapultes, booléen click
		self.click = False
		self.largeur_img = 38
		self.hauteur_img = 122 #c'est la hauteur de l'image des catapultes

		#position,vecteur, gravité du projectile
		self.posx_proj = posx_projectile
		self.posy_proj = posy_projectile
		self.posx_proj_initale = posx_projectile #c'est la position initale du projectile, elle restera alors constante
		self.posy_proj_initale = posy_projectile
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
		self.image = canvas.create_image(self.posx, self.posy, image = image , anchor = 'nw') #on met anchor = NW pour mettre le point d'ancrage en haut à droite
		self.image_proj = canvas.create_image(self.posx_proj, self.posy_proj, image = image_projectile, anchor = 'nw')
		#et sa partie
		self.image_part = canvas.create_image(self.posx_part, self.posy_part, image = image_part , anchor = 'nw')

		#trajectoire des points
		self.list_point_trajectoire = []
		self.list_point_trajectoire_x = []
		self.list_point_trajectoire_y = []
		#la couleur du outline des points de la trajectoire
		self.color_point = color_point

		#vie des catapultes
		self.life = 3
		self.life_posx = life_posx
		self.life_posy =  life_posy
		self.list_img_life = list_img_life
		self.list_img_life_indice = 0 #on le met a 0 car cela correspond à l'image avec tous les coeurs
		self.img_life_default = self.list_img_life[self.list_img_life_indice] #type : PhotoImage
		self.image_life = canvas.create_image(self.life_posx, self.life_posy, image = self.img_life_default, anchor = 'nw')

	def reset_pos_proj(self):
		"""Fonction permettant de réinitialiser la position du projectile"""

		self.posx_proj = self.posx_proj_initale
		self.posy_proj = self.posy_proj_initale
		self.vx = 0
		self.vy = 0

		#on enleve les points de la trajectoire
		for point in range(len(self.list_point_trajectoire)):
			canvas.delete(self.list_point_trajectoire[point])
		self.list_point_trajectoire_x = []
		self.list_point_trajectoire_y = []
		self.list_point_trajectoire = []

	def click_obj(self, event):
		"""Fonction permettant de voir si on clique sur l'objet"""

		self.souris_x, self.souris_y = event.x, event.y

		print("Click x ->", self.souris_x - world.posx,"\nClick y ->", self.souris_y - world.posy - 200)

		if self.life != 0 and self.posx <= self.souris_x <= self.posx + self.largeur_img and self.posy <= self.souris_y <= self.posy + self.hauteur_img: #si je clique sur la catapulte alors on met self.click à True
			self.click = True

			#on (re)met le projectile dans sa position de base
			self.reset_pos_proj()
			canvas.coords(self.image_proj, self.posx_proj, self.posy_proj)

		#si je clique sur le bouton quitter
		if 0 <= self.souris_x <= 60 and 0 <= self.souris_y <= 60:
			print("Arrêt du programme")
			fenetre.destroy()

		#si je clique sur le bouton aide
		if 0 <= self.souris_x <= 74 and 610 <= self.souris_y <= 680:
			world.create_help()

	def drag_obj(self, event):
		"""Fonction permettant de drag l'objet et l'animer, si et seulement si, l'objet a été cliqué"""

		#si on a précedemment cliqué sur la catapulte, alors on peut drag le projectile
		if self.click == True:
			self.souris_x, self.souris_y = event.x, event.y #on prend les coordonnées de la souris

			#on limite les positions des élastiques
			if self.souris_x > self.x_center_ela + 120:
				self.souris_x = self.x_center_ela + 120
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

		#si on a cliqué
		if self.click == True:
			self.liste_vecteur = calcul_vector(self.x_center_ela, self.souris_x, self.y_center_ela, self.souris_y) #on calcule les vecteurs vitesse x et y du projectile
			self.shoot()

		self.click = False

		#on supprime les élastiques lorsque l'on un-clique
		canvas.delete(self.elastique1)
		canvas.delete(self.elastique2)

		#recréation des élastiques de la catapulte
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)

	def shoot(self):
		"""Fonction permettant de faire le shoot du projectile"""

		if self.posy_proj != 520: #on laisse l'actualisation de cette fonction que lorsque le projectile n'est pas au sol
			fenetre.after(70, self.shoot)

		else: #si il est au sol
			time.sleep(1.5) #on attend 1.5 secondes..
			world.return_camera()

		if self.posy_proj < 520: #si il est dans les airs alors on calcul sa trajectoire et on applique certaine fonctions
			self.vx = self.liste_vecteur[0]/2
			self.liste_vecteur[1] += self.gravite #on ajoute la gravité au "pre-vecteur" vitesse y
			self.vy += self.liste_vecteur[1]/10
			self.check_collision() #on regarde s'il y a des collisions

			#puis on ajoute les vitesses à la positions x et y du projectile
			self.posx_proj += self.vx
			self.posy_proj += self.vy

			#on trace la ligne de point-trajectoire
			self.trajectoire_point()
			#effet de caméra si le projectile se rapproche de la bordure de l'écran
			world.shift_world()

			if self.posy_proj >= 520: #si sa position est supérieure au niveau du sol
				self.posy_proj = 520  #alors on le met au sol

			#update
			world.update()

	def trajectoire_point(self):
		"""Fonction permettant la création d'une trajectoire à chaque module 1 == 0de la position x du projectile"""

		#création d'un point à la position du projectile
		self.point = canvas.create_oval(self.posx_proj - 10, self.posy_proj - 10, self.posx_proj, self.posy_proj, fill = 'white', width = 2, outline = self.color_point)
		#on prend les coordonnées du projectile
		self.pointx = self.posx_proj
		self.pointy = self.posy_proj

		#puis on ajoute toutes ses valeurs dans 3 listes
		self.list_point_trajectoire_x.append(self.pointx)
		self.list_point_trajectoire_y.append(self.pointy)
		self.list_point_trajectoire.append(self.point)

	def move(self, event, direction):
		"""Fonction permettant de bouger vers la droite/gauche si et seulement si c'est son tour."""

		if world.tour == 0: #si c'est le tour du joueur 1 cette fonction ne s'appliquera qu'à la catapulte 1
			self = catapulte1
		else: #sinon elle s'appliquera qu'a la catapulte 2
			self = catapulte2

		#si la catapulte en x est hors de la limite à droite et que l'on clique sur le bouton de droite
		if self.posx < 590 - self.largeur_img and direction == 1:
			move = 10
		#si la catapulte en x est hors de la limite de gauche et que je clique sur le bouton de gauche alors:
		elif self.posx > 250 and direction == -1:
			move = -10
		#sinon je ne bouge plus, je suis en dehors des limites alors je ne bouge pas
		else:
			move = 0

		#on ajoute 10 à toutes les coordonnées en x de tous les attributs de la catapulte
		self.posx += move
		self.posx_part += move
		self.x0ela += move
		self.x1ela += move
		self.x2ela += move
		self.x3ela += move
		self.x_center_ela += move
		self.posx_proj += move
		self.posx_proj_initale += move
		self.life_posx += move

		#on update
		world.update()

	def check_collision(self):
		"""Fonction permettant de voir si il y a collision entre les catapultes/projectiles"""

		#si c'est le tour de la catapulte 1 -> c'est obligatoirement son projectile qui fera la collision avec la catapulte 2
		#si le projectile 1 touche la catapulte 2
		if world.tour == 0 and catapulte2.posx - 50 < catapulte1.posx_proj < catapulte2.posx + catapulte2.largeur_img + 35 and catapulte2.posy - 35 < catapulte1.posy_proj < catapulte2.posy + catapulte2.hauteur_img + 35:

			print("collide cata2")
			#ceci ne s'éxécute qu'une seule fois même si il y a une ou plusieurs collisions.

			catapulte1.vx = 0 #on stop instantanément la vitesse x du projectile pour créer un effet de collision

			if world.execute_one_time == True: #cela permet d'éxecuté cette fonction une seule fois par tour (c-a-d une seule collision par tour)
				catapulte2.life -= 1
				catapulte2.list_img_life_indice += 1
				catapulte2.img_life_default = catapulte2.list_img_life[catapulte2.list_img_life_indice] #on charge la PhotoImage de l'image suivante de la liste
				canvas.delete(catapulte2.image_life) #on supprime l'image d'avant
				catapulte2.image_life = canvas.create_image(catapulte2.life_posx, catapulte2.life_posy, image = catapulte2.img_life_default, anchor = 'nw') #puis on recrée l'image qui convient

				world.execute_one_time = False #on remet la variable à False pour ne pas rééxecuter la fonction

		#explication analogue pour la collision du projectile 2 avec la catapulte 1
		if world.tour == 1 and catapulte1.posx - 35 < catapulte2.posx_proj < catapulte1.posx + catapulte1.largeur_img + 35 and catapulte1.posy - 35 < catapulte2.posy_proj < catapulte1.posy + catapulte1.hauteur_img + 35:

			print("collide cata1")
			#ceci ne s'éxécute qu'une seule fois même si il y a une ou plusieurs collisions.

			catapulte2.vx = 0

			if world.execute_one_time == True:
				catapulte1.life -= 1
				catapulte1.list_img_life_indice += 1
				catapulte1.img_life_default = catapulte2.list_img_life[catapulte2.list_img_life_indice]
				canvas.delete(catapulte1.image_life)
				catapulte1.image_life = canvas.create_image(catapulte1.life_posx, catapulte1.life_posy, image = catapulte1.img_life_default, anchor = 'nw')

				world.execute_one_time = False

		#on regarde si l'un des joueurs n'a plus de vie, si oui alors un message de fin de partie est affiché
		if catapulte1.life == 0:
			win_label = canvas.create_text(420, 220, fill = 'black',font = ('angrybirds', 15), text = "La catapulte 1 n'a plus de vie.. La catapulte 2 a alors gagné bravo !")
			win_label_2 = canvas.create_text(420, 260, fill = 'black', font = ('angrybirds', 10), text = "Cliquez sur entrée pour quitter le jeu")
		elif catapulte2.life == 0:
			win_label = canvas.create_text(420, 220, fill = 'black',font = ('angrybirds', 15), text = "La catapulte 2 n'a plus de vie.. La catapulte 1 a alors gagné bravo !")
			win_label_2 = canvas.create_text(420, 260, fill = 'black', font = ('angrybirds', 10), text = "Cliquez sur entrée pour quitter le jeu")

		#tant que les joueurs on de la vie on fait une boucle de cette fonction
		if catapulte1.life != 0 and catapulte2.life != 0:
			fenetre.after(20, self.check_collision)


class World():
	"""Classe permettant la gestion du monde"""

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
		self.compteur_shift = 0

		#text des tours, pour avoir la font angrybirds il faut installer la font dans le dossier font de windows
		install_font.install_font(f_source, dir_dest)#on installe la font angrybirds
		#si la font Angrybirds n'a pas été chargée alors Tkinter créera le texte avec la font par défaut
		self.text_tour = canvas.create_text(420,100,fill="black", font = ('angrybirds', 35), text="TOUR DU JOUEUR 1")

		#on affiche le bouton quitter
		self.quit_button = canvas.create_image(0, 0, image = quit_button_img, anchor = "nw")
		#et le bouton aide
		self.help_button = canvas.create_image(10, 610, image = help_button_img, anchor = "nw")

		#permet d'executer une seul fois la collision de la cata
		self.execute_one_time = True

	def return_camera(self):
		"""Fonction permettant le retour de la caméra lorsque l'un des projectiles est sur le sol"""

		if self.compteur_shift == 0:
			if self.tour == 0:
				canvas.itemconfigure(self.text_tour, text = "TOUR DU JOUEUR 2", font = ('angrybirds', 35))
				self.diff_longueur = -catapulte2.posx + 400 #c'est la distance du vecteur qui sépare la catapulte 1 de la catapulte 2
				print("longueur diff", self.diff_longueur)
				#on change de tour
				self.tour = 1
				#quand on change de tour on change la valeur de cette variable pour que l'on ne fasse qu'une seule collision
				self.execute_one_time = True

			elif self.tour == 1:
				canvas.itemconfigure(self.text_tour, text = "TOUR DU JOUEUR 1", font = ('angrybirds', 35))
				self.diff_longueur = -catapulte1.posx + 400
				print("longueur diff", self.diff_longueur)
				#on change de tour
				self.tour = 0
				#quand on change de tour on change la valeur de cette variable pour que l'on ne fasse qu'une seule collision
				self.execute_one_time = True

			#on calcule la valeur de shift
			if self.diff_longueur < 0:
				self.shift_return = -6
			else:
				self.shift_return = 6

		#et on fait le shift pour tous les objets graphiques
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
		catapulte1.life_posx += self.shift_return


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
		catapulte2.life_posx += self.shift_return

		#on update
		self.update()

		#on incrémente le compteur pour voir à combien à parcourus le shift_return
		self.compteur_shift += abs(self.shift_return)

		#si le compteur n'a pas encore atteint diff_longueur on continue d'actualiser la fonction
		if self.compteur_shift <= abs(self.diff_longueur):
			fenetre.after(10, self.return_camera)

		else: #sinon on arrête d'actualiser et on réinitialise le compteur
			self.compteur_shift = 0

	def shift_world(self):
		"""Permet le shift du monde. Celui-ci est dirigé, seulement, par le projectile lancé."""

		if self.tour == 0:
			self = catapulte1
		else:
			self = catapulte2

		print((self.posx_proj + (largeur_canvas - 500)) - world.posx)

		#on limite le shift aux limites du monde
		if world.limite_droite >  (self.posx_proj + (largeur_canvas - 590)) - world.posx and world.limite_gauche < self.posx_proj - 250 - world.posx:

			#à droite
			if self.posx_proj >= 590: #si la catapulte va trop vers le côté de l'écran
				print("Shift droit")
				diff = -(self.posx_proj - 590) #on calcule la 'vitesse de la caméra' par une simple différence de distance, on fait l'opposé du résultat pour bouger les images dans le sens inverses au mouvement du projectile tiré

				self.posx_proj = 590 #on remet le projectile à la limite de l'écran

				#si c'est le tour du joueur 1 alors on fait le shift du projectile du joueur 2 et PAS du joueur 1 car le joueur 1 bouge déjà
				if world.tour == 0:
					catapulte2.posx_proj += diff
				else: #sinon on fait l'inverse
					catapulte1.posx_proj += diff

				world.posx += diff
				#obj cata1
				catapulte1.posx += diff
				catapulte1.posx_part += diff
				catapulte1.x0ela += diff
				catapulte1.x1ela += diff
				catapulte1.x2ela += diff
				catapulte1.x3ela += diff
				catapulte1.x_center_ela += diff
				catapulte1.posx_proj_initale += diff
				for point in range(len(catapulte1.list_point_trajectoire)):
					catapulte1.list_point_trajectoire_x[point] += diff
				catapulte1.life_posx += diff

				#obj cata2
				catapulte2.posx += diff
				catapulte2.posx_part += diff
				catapulte2.x0ela += diff
				catapulte2.x1ela += diff
				catapulte2.x2ela += diff
				catapulte2.x3ela += diff
				catapulte2.x_center_ela += diff
				catapulte2.posx_proj_initale += diff
				for point in range(len(catapulte2.list_point_trajectoire)):
					catapulte2.list_point_trajectoire_x[point] += diff
				catapulte2.life_posx += diff


			#à gauche
			if self.posx_proj <= 250:
				print("Shift gauche")
				diff = -(self.posx_proj - 250)

				self.posx_proj = 250

				#quand je tire avec une cata je ne veut pas faire le shift de son projectile
				if self == catapulte1:
					catapulte2.posx_proj += diff
				else:
					catapulte1.posx_proj += diff

				world.posx += diff
				#obj cata1
				catapulte1.posx += diff
				catapulte1.posx_part += diff
				catapulte1.x0ela += diff
				catapulte1.x1ela += diff
				catapulte1.x2ela += diff
				catapulte1.x3ela += diff
				catapulte1.x_center_ela += diff
				catapulte1.posx_proj_initale += diff
				for point in range(len(catapulte1.list_point_trajectoire)):
					catapulte1.list_point_trajectoire_x[point] += diff
				catapulte1.life_posx += diff

				#obj proj2
				catapulte2.posx += diff
				catapulte2.posx_part += diff
				catapulte2.x0ela += diff
				catapulte2.x1ela += diff
				catapulte2.x2ela += diff
				catapulte2.x3ela += diff
				catapulte2.x_center_ela += diff
				catapulte2.posx_proj_initale += diff
				for point in range(len(catapulte2.list_point_trajectoire)):
					catapulte2.list_point_trajectoire_x[point] += diff
				catapulte2.life_posx += diff

	def create_help(self):
		"""Fonction permettant la création d'une interface graphique (une autre fenetre) permettant de décrire et expliquer les règles au joueur"""

		fen_help = Tk() #on ouvre une seconde fenêtre
		fen_help.geometry('800x800')
		fen_help.title('Aide/Règles')
		can_help = Canvas(fen_help, width = 800, height = 800, bg ='white')
		can_help.pack()

		#on affiche les règles
		title_aide = can_help.create_text(400, 20,fill="black", font = ('angrybirds', 20), text="Aide et règles")
		text_aide_regles = can_help.create_text(400, 120,fill="black", font = ('angrybirds', 15), text= " Le jeu des catapulte est un jeu opposant deux catapultes pouvant d'une part\n bouger de droite à gauche (il y a des limites) et d'autre part lancer\n le projectile matérialisé par l'angrybirds. \n Le but de ce jeu est de lancer son projectile sur la catapulte adverse. \n Vous avez 3 vies.")
		title_aide_commande = can_help.create_text(400, 230,fill="black", font = ('angrybirds', 20), text= "Commandes du jeu")
		text_aide_commande = can_help.create_text(400, 300,fill="black", font = ('angrybirds', 15), text= " Mouvement catapulte : flèches directionnelle -> / <-\n Drag&Drop sur la catapulte pour tirer")

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

		#vies
		canvas.coords(catapulte1.image_life, catapulte1.life_posx, catapulte1.life_posy)
		canvas.coords(catapulte2.image_life, catapulte2.life_posx, catapulte2.life_posy)

		#positions points trajectoire
		for point in range(len(catapulte1.list_point_trajectoire)):
			canvas.coords(catapulte1.list_point_trajectoire[point], catapulte1.list_point_trajectoire_x[point] + 10, catapulte1.list_point_trajectoire_y[point] + 10, catapulte1.list_point_trajectoire_x[point] + 20, catapulte1.list_point_trajectoire_y[point] + 20)
		for point in range(len(catapulte2.list_point_trajectoire)):
			canvas.coords(catapulte2.list_point_trajectoire[point], catapulte2.list_point_trajectoire_x[point] + 10, catapulte2.list_point_trajectoire_y[point] + 10, catapulte2.list_point_trajectoire_x[point] + 20, catapulte2.list_point_trajectoire_y[point] + 20)

#----------------------------------------------------------------------------------------------------
# OBJETS

world = World(0, -200, background_img)

#on créer les 2 objets de type Catapulte
catapulte1 = Catapulte(400, 420, catapulte_left_img, 405, 439, 407, 441,   432, 439, 434, 441,     401, 420, red_bird_img, part_cata_left_img, 400, 420, 'red', list_img_life, 388, 390)

catapulte2 = Catapulte(1696, 420, catapulte_right_img, 1698, 439, 1700, 441,   1724, 439, 1726, 441,    1699, 420, blue_bird_img, part_cata_right_img, 1696, 420, 'blue', list_img_life, 1685, 390)

#----------------------------------------------------------------------------------------------------
# BINDS

canvas.bind("<Button-1>", catapulte1.click_obj) #lorsque l'on clique sur la catapulte 1
canvas.bind("<ButtonRelease-1>", catapulte1.unclick) #lorsqu'on relâche le clique sur la catapulte 1
canvas.bind("<B1-Motion>", catapulte1.drag_obj) #lorsque l'on clique sur la catapulte 1

canvas.bind("<Button-3>", catapulte2.click_obj) #lorsque l'on clique sur la catapulte 2
canvas.bind("<ButtonRelease-3>", catapulte2.unclick) #lorsqu'on relâche le clique sur la catapulte 2
canvas.bind("<B3-Motion>",catapulte2.drag_obj) #lorsque l'on clique sur la catapulte 2

#move des catapultes, ces binds sont utilisés aussi pour la cata2 (cf la fonc), on utilise des arguments grâce à la fonction lambda
fenetre.bind("<Left>", lambda event, direction = -1: catapulte1.move(event, direction)) #mouvement gauche, flèche gauche
fenetre.bind("<Right>", lambda event, direction = 1: catapulte1.move(event, direction)) #mouvement droite, flèche droite

fenetre.bind("<Return>", destroy_fen_when_win) #lorsqu'on touche entrée et qu'un joueur a gagné -> arrêt programme



fenetre.mainloop()
