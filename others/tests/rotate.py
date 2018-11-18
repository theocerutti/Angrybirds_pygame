from tkinter import *
from PIL import Image, ImageTk #installé depuis pip
import time

fenetre = Tk()

#fenetre.iconbitmap("mon_icone.ico") # on change l'icône de notre fenêtre
fenetre.geometry("1000x800") # on change les dimensions de notre fenêtre
fenetre.title('Jeu des catapultes') #on change le titre du jeu

canvas = Canvas(fenetre, width = 840, height = 680, bg ='black')
canvas.pack()


image_cata1 = PhotoImage(file = "lib/image/1_right.gif")
image_cata2_pill = Image.open("lib/image/1_right.gif")
image_cata2_pill = image_cata2_pill.transpose(Image.FLIP_LEFT_RIGHT)
image_cata2 = ImageTk.PhotoImage(image_cata2_pill)

image = canvas.create_image(100, 100, image = image_cata1  , anchor = "nw")
image2 = canvas.create_image(200, 200, image = image_cata2  , anchor = "nw")


fenetre.mainloop()
