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
			resultat = prim.step_chiff(message, key)
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
			resultat = prm.step_dechiff(message, key)
			print("Message déchiffré : ", resultat)
			return