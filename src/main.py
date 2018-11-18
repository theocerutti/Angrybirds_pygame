#!/usr/bin/env python
#-*- coding: utf-8 -*-

from tkinter import *
from math import *
import time

fenetre = Tk()

try:
	fenetre.iconbitmap("lib/image/icone.ico") # on change l'icône de notre fenêtre
except:
	print("[BUG] Le chargement de l'icône a échoué. Êtes-vous sur Linux ?") #linux ne charge pas les .ico

print("Pour une expérience optimale, veillez à installer la font 'angrybirds' dans le dossier Fonts de Windows.\nLa font est dans le dossier lib/font.")

fenetre.geometry('1000x800') # on change les dimensions de notre fenêtre
fenetre.title('Jeu des catapultes') #on change le titre du jeu
fenetre.configure(bg = 'black') #on change la couleur de la fenetre

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

#liste des images des vies: 3, 2, 1, 0 coeurs
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
		"""Constructeur de la classe catapulte"""

		#coordonnées de la catapulte
		self.posx = posx
		self.posy = posy

		#coordonnées de la partie de la catapulte (la catapulte est sectionnée en 2 partie pour permettre un positionnement plus réaliste des élastiques)
		self.posx_part = posx_part
		self.posy_part = posy_part

		#infos catapultes, booléen click
		self.click = False
		self.largeur_img = 38
		self.hauteur_img = 122 #c'est la hauteur de l'image des catapultes

		#position, vecteur, gravité du projectile
		self.posx_proj = posx_projectile
		self.posy_proj = posy_projectile
		self.posx_proj_initale = posx_projectile #c'est la position initale du projectile
		self.posy_proj_initale = posy_projectile
		self.gravite = 10
		self.vy = 0
		self.vx = 0

		#positions x y des élastiques
		self.x0ela, self.y0ela, self.x1ela, self.y1ela = x0ela, y0ela, x1ela, y1ela
		self.x2ela, self.y2ela, self.x3ela, self.y3ela = x2ela, y2ela, x3ela, y3ela
		self.x_center_ela, self.y_center_ela = self.x0ela + 20, self.y0ela #coordonnées du centre entre les deux élastiques

		#création des élastiques
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

		#vie des catapultes, coordonnées de l'image de la vie
		self.life = 3
		self.life_posx = life_posx
		self.life_posy =  life_posy
		self.list_img_life = list_img_life
		self.list_img_life_indice = 0 #on le met a 0 car cela correspond à l'image avec tous les coeurs (1ere image de la liste)
		self.img_life_default = self.list_img_life[self.list_img_life_indice] #type : PhotoImage
		self.image_life = canvas.create_image(self.life_posx, self.life_posy, image = self.img_life_default, anchor = 'nw')

	def reset_pos_proj(self):
		"""Fonction permettant de réinitialiser la position du projectile"""

		self.posx_proj = self.posx_proj_initale
		self.posy_proj = self.posy_proj_initale
		self.vx = 0
		self.vy = 0

		#on enlève les points de la trajectoire
		for point in range(len(self.list_point_trajectoire)):
			canvas.delete(self.list_point_trajectoire[point])
		#et on supprime toutes les valeurs de ces 3 listes
		self.list_point_trajectoire_x = []
		self.list_point_trajectoire_y = []
		self.list_point_trajectoire = []

	def click_obj(self, event):
		"""Fonction permettant de voir si l'on clique sur un bouton/catapulte"""

		self.souris_x, self.souris_y = event.x, event.y #on prend les coordonnées de la souris

		print("Click x ->", self.souris_x - world.posx,"\nClick y ->", self.souris_y - world.posy - 200)

		#si je clique sur une catapulte
		#et que les joueurs ont encore de la vie (ce qui permet que lorsque les joueurs n'en ont plus alors la catapulte ne peut être cliquable donc la partie ne peut continuer)
		if self.life != 0 and self.posx <= self.souris_x <= self.posx + self.largeur_img and self.posy <= self.souris_y <= self.posy + self.hauteur_img:
			self.click = True #on passe cette valeur à True pour savoir que l'on a cliqué sur la catapulte

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
		"""Fonction permettant de drag l'objet si l'objet a été cliqué"""

		#si on a précedemment cliqué sur la catapulte, alors on peut drag le projectile
		if self.click == True:
			self.souris_x, self.souris_y = event.x, event.y #on prend les coordonnées de la souris

			#on limite les positions des élastiques (rectangle de 120x100)
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
			canvas.coords(self.image_proj, self.souris_x - 15, self.souris_y - 15) #15 c'est la moitié de la taille de l'image du projectile, on fait ceci car le point d'ancrage est en nw

	def unclick(self, event):
		"""Fonction permettant de détecter lorsque l'on relâche le clique"""

		#si on a cliqué auparavant sur la catapulte et qu'on vient de relâcher
		if self.click == True:
			self.liste_vecteur = calcul_vector(self.x_center_ela, self.souris_x, self.y_center_ela, self.souris_y) #on calcule les vecteurs vitesse x et y du projectile
			self.shoot()

		self.click = False

		#on supprime les élastiques lorsque l'on relâche le clique
		canvas.delete(self.elastique1)
		canvas.delete(self.elastique2)

		#puis on les recréer dans leurs positions d'origine
		self.elastique1 = canvas.create_line(self.x0ela, self.y0ela, self.x1ela, self.y1ela, fill = 'black', width = 3)
		self.elastique2 = canvas.create_line(self.x2ela, self.y2ela, self.x3ela, self.y3ela, fill = 'black', width = 3)

	def shoot(self):
		"""Fonction permettant de faire le tir du projectile"""

		if self.posy_proj < 520: #on laisse l'actualisation de cette fonction que lorsque le projectile n'est pas au sol (position y du sol = 520)
			fenetre.after(70, self.shoot)

		else: #si il est au sol
			time.sleep(1.5) #on attend 1.5 secondes..
			world.return_camera() #on fais l'effet de caméra pour retourner à la catapulte qui doit tirer

		if self.posy_proj < 520: #si il est dans les airs alors on calcul sa trajectoire et on applique quelques fonctions
			self.vx = self.liste_vecteur[0]/2
			self.liste_vecteur[1] += self.gravite #on ajoute la gravité au "pre-vecteur" vitesse y
			self.vy += self.liste_vecteur[1]/10
			self.check_collision() #on regarde s'il y a des collisions

			#puis on ajoute les vitesses à la positions x et y du projectile
			self.posx_proj += self.vx
			self.posy_proj += self.vy

			#on modélise la trajectoire du projectile
			self.trajectoire_point()
			#puis on fait l'effet de caméra si le projectile se rapproche de la bordure de l'écran
			world.shift_world()

			if self.posy_proj >= 520: #si sa position est supérieure au niveau du sol
				self.posy_proj = 520  #alors on le met au sol

			#update
			world.update()

	def trajectoire_point(self):
		"""Fonction permettant la création d'une trajectoire en fonction de la position x du projectile"""

		#création d'un point à la position du projectile
		self.point = canvas.create_oval(self.posx_proj - 10, self.posy_proj - 10, self.posx_proj, self.posy_proj, fill = 'white', width = 2, outline = self.color_point)
		#on prend les coordonnées du projectile
		self.pointx = self.posx_proj
		self.pointy = self.posy_proj

		#puis on ajoute toutes ces valeurs dans 3 listes
		self.list_point_trajectoire_x.append(self.pointx)
		self.list_point_trajectoire_y.append(self.pointy)
		self.list_point_trajectoire.append(self.point)

	def move(self, event, direction):
		"""Fonction permettant de bouger vers la droite/gauche si c'est son tour."""

		if world.tour == 0: #si c'est le tour du joueur 1 cette fonction ne s'appliquera qu'à la catapulte 1
			self = catapulte1
		else: #sinon elle s'appliquera à la catapulte 2
			self = catapulte2

		#si la catapulte en x est hors de la limite à droite
		if self.posx < 590 - self.largeur_img and direction == 1:
			move = 10
		#si la catapulte en x est hors de la limite de gauche
		elif self.posx > 250 and direction == -1:
			move = -10
		#sinon je ne bouge plus, je suis à côté des limites alors je ne bouge pas
		else:
			move = 0

		#on ajoute move à toutes les coordonnées en x de tous les objets de la catapulte
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

			if world.execute_one_time == True: #cela permet d'exécuter cette fonction une seule fois par tour (c-a-d une seule collision par tour)
				catapulte2.life -= 1
				catapulte2.list_img_life_indice += 1
				catapulte2.img_life_default = catapulte2.list_img_life[catapulte2.list_img_life_indice] #on charge la PhotoImage de l'image suivante de la liste
				canvas.delete(catapulte2.image_life) #on supprime l'image d'avant
				catapulte2.image_life = canvas.create_image(catapulte2.life_posx, catapulte2.life_posy, image = catapulte2.img_life_default, anchor = 'nw') #puis on recrée l'image qui convient

				world.execute_one_time = False #on remet la variable à False pour ne pas rééxecuter la fonction

		#explication analogue pour la collision du projectile 2 avec la catapulte 1
		if world.tour == 1 and catapulte1.posx - 35 < catapulte2.posx_proj < catapulte1.posx + catapulte1.largeur_img + 35 and catapulte1.posy - 35 < catapulte2.posy_proj < catapulte1.posy + catapulte1.hauteur_img + 35:

			print("collide cata1")

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

		#tour du joueur, quand il est à 0 -> c'est le tour du J0 (à gauche) quand il est à 1 c'est au tour du J1 (à droite)
		self.tour = 0
		self.compteur_shift = 0

		#texte des tours, on commence par le tour 1
		#on met la police angrybirds comme ca si on a installé cette police (qui est dans le dossier src/lib/font) est sera affiché
		self.text_tour = canvas.create_text(420,100, fill="black", font = ('angrybirds', 35), text="TOUR DU JOUEUR 1")

		#on affiche le bouton quitter
		self.quit_button = canvas.create_image(0, 0, image = quit_button_img, anchor = "nw")
		#et le bouton aide
		self.help_button = canvas.create_image(10, 610, image = help_button_img, anchor = "nw")

		#permet d'exécuter une seule fois la collision de la cata
		self.execute_one_time = True

	def return_camera(self):
		"""Fonction permettant le retour de la caméra lorsque l'un des projectiles est sur le sol
			shift = effet de caméra, son mouvement"""

		if self.compteur_shift == 0: #lorsque le shift est fini alors:
			if self.tour == 0:
				canvas.itemconfigure(self.text_tour, text = "TOUR DU JOUEUR 2", font = ('angrybirds', 35))
				self.diff_longueur = -catapulte2.posx + 400 #c'est la distance qui sépare la catapulte 1 de la catapulte 2
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
			if self.diff_longueur < 0: #si la longueur entre les 2 catapultes est négative
				self.shift_return = -6 #alors l'effet de caméra se fera vers la gauche
			else:
				self.shift_return = 6 #sinon vers la droite

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
				diff = -(self.posx_proj - 590) #alors on calcule la 'vitesse de la caméra' par une simple différence de distance, on fait l'opposé du résultat pour bouger les images dans le sens inverse au mouvement du projectile tiré

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
			#explication analogue
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
		"""Fonction permettant la création d'une interface graphique (une autre fenetre) permettant de décrire et expliquer les règles aux joueurs"""

		fen_help = Tk() #on ouvre une seconde fenêtre
		fen_help.geometry('800x800')
		fen_help.title('Aide/Règles')
		can_help = Canvas(fen_help, width = 800, height = 800, bg ='white')
		can_help.pack()

		#on affiche les règles
		title_aide = can_help.create_text(400, 20,fill="black", font = ('segoe UI Black', 20), text="Aide et règles")
		text_aide_regles = can_help.create_text(400, 120,fill="black", font = ('segoe UI Black', 15), text= " Le jeu des catapulte est un jeu opposant deux catapultes pouvant d'une part\n bouger de droite à gauche (il y a des limites) et d'autre part lancer\n le projectile matérialisé par l'angrybirds. \n Le but de ce jeu est de lancer son projectile sur la catapulte adverse. \n Vous avez 3 vies.")
		title_aide_commande = can_help.create_text(400, 230,fill="black", font = ('segoe UI Black', 20), text= "Commandes du jeu")
		text_aide_commande = can_help.create_text(400, 300,fill="black", font = ('segoe UI Black', 15), text= " Mouvement catapulte : flèches directionnelle -> / <-\n Drag&Drop sur la catapulte pour tirer\n Clique gauche pour tirer le projectile 1 et clique droit pour le projectile 2")

	def update(self):
		"""Fonction permettant d'update tous les objets graphiques"""

		#background
		canvas.coords(world.image, world.posx, world.posy)

		#catapultes/projectiles -> entremêlé à cause de la partie de la catapulte (elle doit être devant le projectile)
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
# CREATION OBJETS

world = World(0, -200, background_img)

#on créer les deux objets de type Catapulte
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

#mouvement des catapultes, ces binds sont utilisés aussi pour la cata2 (cf la fonc), on utilise des arguments grâce à la fonction lambda
fenetre.bind("<Left>", lambda event, direction = -1: catapulte1.move(event, direction)) #mouvement gauche, flèche gauche
fenetre.bind("<Right>", lambda event, direction = 1: catapulte1.move(event, direction)) #mouvement droite, flèche droite

fenetre.bind("<Return>", destroy_fen_when_win) #lorsqu'on touche entrée et qu'un joueur a gagné -> arrêt programme

fenetre.mainloop()
