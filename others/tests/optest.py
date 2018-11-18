

class class1:
	def fonc1(self):
		self.a = 10
		test_class2.fonc2(self.a)

class class2:
	def fonc2(self, number):
		number += 1 #là je voudrais passer par l'argument pour changer self.a et en gros je voudrais que ce soit self.a qui incremente au lieu de l'argument..

test_class2 = class2()

test_class1 = class1()
test_class1.fonc1()

print(test_class1.a) #je voudrais au final obtenir 11
