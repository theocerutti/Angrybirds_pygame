import time

temps = 0
temps_avant = time.time()

while 2 > temps - temps_avant: 
	temps = time.time()

print("les 2 secondes d'attentes sont passées...")