#!/usr/bin/env python
#-*- coding: utf-8 -*-

#Programme testant l'animation d'une image

from tkinter import *

fenetre = Tk()

#fenetre.iconbitmap("mon_icone.ico") # on change l'icône de notre fenêtre
fenetre.geometry("1000x800") # on change les dimensions de notre fenêtre
fenetre.title('Jeu des catapultes') #on change le titre du jeu

canvas = Canvas(fenetre, width = 840, height = 680, bg ='black')
canvas.pack()

background = PhotoImage(file = "lib/image/world.gif")
background_img = canvas.create_image(0, -250, image = background, anchor = "nw")

catapulte_right_IDLE = PhotoImage(file = "lib/image/catapulte_right_IDLE.gif")
catapulte_left_IDLE = PhotoImage(file = "lib/image/catapulte_left_IDLE.gif")

cata = canvas.create_image(100, 100, image = catapulte_left_IDLE, anchor = "nw") #l'image de 'base' au début sera la cata gauche
cata2 = canvas.create_image(200, 100, image = catapulte_left_IDLE, anchor = "nw") #l'image de 'base' au début sera la cata gauche

list_catapulte_img = []
list_catapulte_img.append(catapulte_left_IDLE)
list_catapulte_img.append(catapulte_right_IDLE)
cata_indice = 0


def change_image1(event):
	"""Permet de changer l'image pour faire une animation"""
	global cata_indice, cata

	print("je change d'image")
	cata_indice += 1
	if cata_indice == len(list_catapulte_img):
		cata_indice = 0

	canvas.delete(cata) #on supprime l'image d'avant
	cata = canvas.create_image(100, 100, image = list_catapulte_img[cata_indice], anchor = "nw") #l'image de 'base' au début sera la cata gauche

def change_image2(event):
	"""Permet de changer l'image pour faire une animation"""
	global cata_indice, cata2

	print("je change d'image")
	cata_indice += 1
	if cata_indice == len(list_catapulte_img):
		cata_indice = 0

	canvas.delete(cata2) #on supprime l'image d'avant
	cata2 = canvas.create_image(200, 100, image = list_catapulte_img[cata_indice], anchor = "nw") #l'image de 'base' au début sera la cata gauche

canvas.bind("<Motion>", change_image1) #lorsque l'on clique sur la catapulte 1
canvas.bind("<Button-1>", change_image2) #lorsque l'on clique sur la catapulte 2

fenetre.mainloop()
