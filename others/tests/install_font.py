#Ce programme permet de copier coller le fichier font angrybirds dans le dossier font de windows.

#-----------------------------------------------
#Ce programme ne peut marcher que lorsque qu'on est en admin. DONC le programme doit être un .exe (pour être lancé en admin)
#

import shutil
import os.path #ceci va permettre de marcher sur n'importe quelle ordinateur, nous ne sommes pas obligés de mettre la lettre de disque dur (ex : C:)

def install_font(source, dest):
	"""Fonction permettant d'installer des fonts dans n'importe quelle dossier. Cette installation ce fait par copier-coller. Attention, il est parfois obligatoire de lancer le programme en tant qu'administrateur pour le bon fonctionnement de la fonction"""

	try:
		shutil.copy(f_source, os.path.abspath(dir_dest)) #on copie-colle
	except:
		print("[ERROR] La font n'a pas été copiée dans le dossier Font de Windows.")
		print("		--> Vous n'avez peut-être pas lancé le programme en tant qu'administrateur.")
		print("		--> Vérifiez bien que votre dossier Font ce trouve dans ' *:\Windows\Fonts '")
