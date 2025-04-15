from modules import prim, second

def main():
	while True:
		try:
			choice = int(input("Que souhaitez-vous faire ?\n1. Chiffrer mon message.\n2.Déchiffrer mon message.\nMon choix :"))
		except ValueError:
			print("Veuillez entrer un chiffre valide.")
			continue
		if choice == 1:
			message = input("Quel est votre message ?\nMon message :")
			if not message:
				print("Le message ne peut pas être vide.")
				continue
			key = input("Quelle est votre clé de chiffrement ?\nMa clé :")
			if not key:
				print("La clé ne peut pas être vide.")
				continue
			resultat = # Faire les étapes de chiffrement avec prim.etapes_chif
			print("Message chiffré : ", resultat) 
			return
		elif choice == 2:
			message = input("Quel est votre message ?\nMon message :")
			if not message:
				print("Le message ne peut pas être vide.")
				continue
			key = input("Quelle est votre clé de déchiffreemnt ?\nMa clé :")
			if not key:
				print("La clé ne peut pas être vide.")
				continue
			resultat = # Faire les étapes de déchiffrement avec second.etapes_dechif
			print("Message déchiffré : ", resultat)
			return