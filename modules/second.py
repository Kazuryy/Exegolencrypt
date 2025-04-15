# Fonctions de chiffrement et déchiffrement

# Principal

def demand_msg_key():
    while True:
        message = input("\nQuel est votre message ?\nMon message : ")
        if not message:
            print("❌  Le message ne peut pas être vide.")
            continue
        key = input("\nQuelle est votre clé de chiffrement ?\nMa clé : ")
        if not key:
            print("❌  La clé ne peut pas être vide.")
            continue
        return message, key

# Chiffrement

...

# Déchiffrement

...