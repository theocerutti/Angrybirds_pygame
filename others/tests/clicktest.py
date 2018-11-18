#!/usr/bin/env python
#-*- coding: utf-8 -*-

from tkinter import *

fenetre = Tk()

#fenetre.iconbitmap("mon_icone.ico") # on change l'icône de notre fenêtre
fenetre.geometry("1000x800") # on change les dimensions de notre fenêtre
fenetre.title('Jeu des catapultes') #on change le titre du jeu

canvas = Canvas(fenetre, width = 840, height = 680, bg ='black')
canvas.pack()

def click1(event):
	print("click1")

def click2(event):
	print("click2")

canvas.bind("<Button-1>", click1)
canvas.bind("<Button-1>", click2)

fenetre.mainloop()
