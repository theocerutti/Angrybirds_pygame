from tkinter import *
import time

fenetre = Tk()

#fenetre.iconbitmap("mon_icone.ico") # on change l'icône de notre fenêtre
fenetre.geometry("1000x800") # on change les dimensions de notre fenêtre
fenetre.title('Jeu des catapultes') #on change le titre du jeu

hauteur_canvas, largeur_canvas = 840, 680
canvas = Canvas(fenetre, width = hauteur_canvas, height = largeur_canvas, bg ='black')
canvas.pack()

background_img = PhotoImage(file = "lib/image/world.gif")
xworld, yworld = 0,0
world = canvas.create_image(xworld, yworld, image = background_img, anchor = "nw")

x0 = 10
x1 = 20
y0 = 90
y1 = 100
rect = canvas.create_rectangle(x0,y0,x1,y1)

def move(event):
	global rect, x0,y0,x1,y1

	x0+=10
	x1+=10

	active_shift()
	canvas.coords(rect, x0,y0,x1,y1)
	canvas.coords(world, xworld, yworld)

def shiftx(difff):
	global world, xworld
	print(difff)
	xworld += -difff

def active_shift():
	global rect, x0,y0,x1,y1
	print(x0)
	if x0 > 100:
		print("a")
		diff = x0 - 100
		x1 = 90
		x0 = 100
		shiftx(diff)

	fenetre.after(10, active_shift)

canvas.bind("<Button-1>", move)

fenetre.mainloop()
