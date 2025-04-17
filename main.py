from modules import prim, second
from tkinter import filedialog
import tkinter as tk
import os

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
                    choice2 = int(input("\nQue voulez-vous chiffrer ?\n1. fichier .txt.\n2. Message dans la console.\n3. Un dossier.\nMon choix : "))
                except ValueError:
                    print("\n❌  Veuillez entrer un chiffre valide.\n")
                    continue
                if choice2 == 1:
                    resultat = prim.chiffrer_text()
                    return
                elif choice2 == 2:
                    message, key = second.demand_msg_key()
                    resultat = prim.chiffrer(message, key)
                    print("Message chiffré : ", resultat) 
                    return
                elif choice2 == 3:
                    # Utiliser la fonction avec dialogue pour plus de clarté
                    resultat = prim.chiffrer_dossier_avec_dialogue()
                    return
        elif choice == 2:
            while True:
                try:
                    choice2 = int(input("\nQue voulez-vous déchiffrer ?\n1. Fichier .txt .\n2. Message dans la console.\n3. Un dossier.\n\nMon choix : "))
                except ValueError:
                    print("\n❌  Veuillez entrer un chiffre valide.\n")
                    continue
                if choice2 == 1:
                    resultat = prim.dechiffrer_text()
                    print(resultat)
                    return
                elif choice2 == 2:
                    message_chiffre, key = second.demand_msg_key()
                    resultat = prim.dechiffrer(message_chiffre, key)
                    print("Message déchiffré : ", resultat)
                    return
                elif choice2 == 3:
                    # Utiliser la fonction de déchiffrement de dossier avec dialogue
                    resultat = prim.dechiffrer_dossier_avec_dialogue()
                    print(resultat)
                    return

main()