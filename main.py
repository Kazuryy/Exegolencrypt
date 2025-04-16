from modules import prim, second

def main():
	while True:
		try:
			choice = int(input("Que souhaitez-vous faire ?\n1. Chiffrer mon message.\n2. Déchiffrer mon message.\nMon choix : "))
		except ValueError:
			print("\n❌  Veuillez entrer un chiffre valide.\n")
			continue
		if choice == 1:
			resultat = prim.chiffrer()
			print("Message chiffré : ", resultat) 
			return
		elif choice == 2:
			resultat = prim.dechiffrer()
			print("Message déchiffré : ", resultat)
			return

main()