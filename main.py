from modules import prim, second

def main():
	while True:
		try:
			choice = int(input("Que souhaitez-vous faire ?\n1. Chiffrer mon message.\n2. Déchiffrer mon message.\nMon choix : "))
		except ValueError:
			print("\n❌  Veuillez entrer un chiffre valide.\n")
			continue
		if choice == 1:
			while True:
				try:
					choice2 = int(input("\nQue voulez-vous chiffrer ?\n1. fichier.txt.\n2. Message dans la console.\nMon choix : "))
				except ValueError:
					print("\n❌  Veuillez entrer un chiffre valide.\n")
					continue
				if choice2 == 1:
					...
					return
				elif choice2 == 2:
					resultat = prim.chiffrer()
					print("Message chiffré : ", resultat) 
					return
		elif choice == 2:
			while True:
				try:
					choice2 = int(input("\nQue voulez-vous déchiffrer ?\n1. fichier.txt.\n2. Message dans la console.\nMon choix : "))
				except ValueError:
					print("\n❌  Veuillez entrer un chiffre valide.\n")
					continue
				if choice2 == 1:
					...
					return
				elif choice2 == 2:
					resultat = prim.dechiffrer()
					print("Message déchiffré : ", resultat)
					return

main()