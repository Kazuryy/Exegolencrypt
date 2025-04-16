# Appel des fonctions (étapes de chiffrement et déchiffrement)
from . import second
import tkinter as tk
from tkinter import filedialog

# Chiffrement

def chiffrer(message, key):
    """
    Fonction de chiffrement MultiCrypt améliorée sans dépendances externes.
    Compatible avec les clés complexes contenant des caractères spéciaux.
    """
    
    try:
        # Générer les valeurs dérivées de la clé
        key_values = second.generate_key_values(key)
        block_size = key_values['block_size']
        char_values = key_values['char_values']
        fingerprint = key_values['fingerprint']
        
        # Étape 1: Ajout de l'empreinte de la clé au début
        processed = fingerprint
        
        # Étape 2: Ajout du message original en préservant tous les caractères
        # Cette fois, on ne fait pas de substitution César pour préserver les caractères accentués
        processed += message
        
        # Étape 3: Expansion (ajouter des caractères leurres)
        expanded = ""
        for i, char in enumerate(processed):
            expanded += char
            # Ajouter un caractère leurre basé sur la position et la clé
            key_char_index = i % len(key)
            leurre_value = (ord(key[key_char_index]) + i) % 95 + 32  # Caractères imprimables ASCII
            expanded += chr(leurre_value)
        
        # Étape 4: Transposition par blocs
        blocks = [expanded[i:i+block_size] for i in range(0, len(expanded), block_size)]
        transposed = ""
        for block in blocks:
            # Inverser chaque bloc
            transposed += block[::-1]
        
        # Étape 5: XOR avec les valeurs des caractères de la clé
        xored = ""
        for i, char in enumerate(transposed):
            key_value = char_values[i % len(char_values)]
            xored_value = ord(char) ^ key_value
            xored += chr(xored_value % 65536)  # S'assurer que nous restons dans la plage Unicode valide

        # Étape 6: Encodage final
        result = second.secure_encode(xored)
        return result
        
    except Exception as e:
        return f"Erreur lors du chiffrement: {str(e)}"

def chiffrer_text():
    try:
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        if not file_path:
            return "Aucun fichier sélectionné."

        try:
            with open(file_path, 'r') as file:
                contenu = file.read()
        except Exception as e:
            return f"Erreur lors de la lecture du fichier : {e}"

        try:
            key = second.demand_key()
            contenu_chiffre = chiffrer(contenu, key)
        except Exception as e:
            return f"Erreur lors du chiffrement : {e}"

        try:
            with open(file_path, 'w') as file2:
                file2.write(contenu_chiffre)
        except Exception as e:
            return f"Erreur lors de l'écriture du fichier : {e}"

        return f"✅  Fichier chiffré avec succès : {file_path}"

    except Exception as e:
        return f"Une erreur inattendue s'est produite : {e}"

# Déchiffrement

def dechiffrer(message_chiffre, key):
    """
    Fonction de déchiffrement MultiCrypt améliorée sans dépendances externes.
    """
    
    try:
        # Générer les mêmes valeurs dérivées de la clé
        key_values = second.generate_key_values(key)
        block_size = key_values['block_size']
        char_values = key_values['char_values']
        fingerprint = key_values['fingerprint']
        fingerprint_length = len(fingerprint)
        
        # Étape 1: Décodage
        try:
            decoded = second.secure_decode(message_chiffre)
        except:
            return "Erreur: Le message chiffré est corrompu ou mal formaté."
        
        # Étape 2: Inverser le XOR
        unxored = ""
        for i, char in enumerate(decoded):
            key_value = char_values[i % len(char_values)]
            original_value = ord(char) ^ key_value
            unxored += chr(original_value % 65536)  # Rester dans la plage Unicode valide
        
        # Étape 3: Inverser la transposition par blocs
        # D'abord, découper en blocs
        transposed_blocks = [unxored[i:i+block_size] for i in range(0, len(unxored), block_size)]
        untransposed = ""
        for block in transposed_blocks:
            # Inverser chaque bloc à nouveau
            untransposed += block[::-1]
        
        # Étape 4: Supprimer les caractères leurres (un sur deux, en commençant par le deuxième)
        contracted = ""
        for i in range(0, len(untransposed), 2):
            if i < len(untransposed):
                contracted += untransposed[i]

        # Étape 5: Vérifier l'empreinte de la clé
        if len(contracted) <= fingerprint_length:
            return "Erreur: Message trop court ou clé incorrecte."

        received_fingerprint = contracted[:fingerprint_length]
        message_sans_fingerprint = contracted[fingerprint_length:]

        if received_fingerprint != fingerprint:
            return "Erreur: Clé de déchiffrement incorrecte."
        
        # Étape 6: Retourner le message original sans transformation
        # Nous avons supprimé la phase de substitution César pour préserver les caractères spéciaux
        return message_sans_fingerprint

    except Exception as e:
        return f"Erreur de déchiffrement: {str(e)}"

def dechiffrer_text():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename()

    with open(file_path, 'r') as file:
        contenu = file.read()
    key = second.demand_key()
    contenu_dechiffre = dechiffrer(contenu, key)

    with open(file_path, 'w') as file2:
        file2.write(contenu_dechiffre)

    return f"Retrouvez votre fichier .txt ici : {file_path}"

def dechiffrer_text():
    try:
        root = tk.Tk()
        root.withdraw()

        file_path = filedialog.askopenfilename()

        if not file_path:
            return "Aucun fichier sélectionné."

        try:
            with open(file_path, 'r') as file:
                contenu = file.read()
        except Exception as e:
            return f"Erreur lors de la lecture du fichier : {e}"

        try:
            key = second.demand_key()
            contenu_dechiffre = dechiffrer(contenu, key)
        except Exception as e:
            return f"Erreur lors du déchiffrement : {e}"

        try:
            with open(file_path, 'w') as file2:
                file2.write(contenu_dechiffre)
        except Exception as e:
            return f"Erreur lors de l'écriture du fichier : {e}"

        return f"✅  Fichier déchiffré avec succès : {file_path}"

    except Exception as e:
        return f"Une erreur inattendue s'est produite : {e}"