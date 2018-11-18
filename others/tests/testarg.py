#!/usr/bin/env python
#-*- coding: utf-8 -*-

from tkinter import *

fenetre = Tk()

class test:

	def fonc1(self, event, a, b):

		self.fonc2(a)

	def fonc2(self, b):

		print("Tout c'est bien passé!", b)

		fenetre.after(70, self.fonc2)

TEST = test()

fenetre.bind('<Button-1>', lambda event, a = 1, b = 2: TEST.fonc1(event, a, b))
fenetre.mainloop()
