# Fonctions de chiffrement et déchiffrement

# Principal

def demand_msg_key():
    while True:
        message = input("\nQuel est votre message ?\nMon message : ")
        if not message:
            print("❌  Le message ne peut pas être vide.")
            continue
        while True:
            key = input("\nQuelle est votre clé de chiffrement ?\nMa clé : ")
            if not key:
                print("❌  La clé ne peut pas être vide.")
                continue
            return message, key

def generate_key_values(key):
    """
    Génère différentes valeurs dérivées de la clé pour être utilisées dans les différentes étapes
    du chiffrement, sans utiliser de bibliothèques cryptographiques.
    """
    # Somme des valeurs Unicode de chaque caractère de la clé
    key_sum = sum(ord(c) for c in key)
    
    # Générer différentes valeurs pour chaque étape
    caesar_shift = key_sum % 26
    block_size = (len(key) % 5) + 3  # Entre 3 et 7
    
    # Tableau des valeurs ordinales de chaque caractère
    char_values = [ord(c) for c in key]
    
    # Génération d'une empreinte simple basée sur la clé
    fingerprint = ""
    for i in range(10):  # Créer une empreinte de 10 caractères
        index = (key_sum + i) % len(key)
        char_value = ord(key[index])
        fingerprint += chr(33 + (char_value % 94))  # Caractères imprimables ASCII
    
    return {
        'caesar_shift': caesar_shift,
        'block_size': block_size,
        'char_values': char_values,
        'fingerprint': fingerprint,
        'key_sum': key_sum
    }

# Chiffrement

def secure_encode(text):
    """
    Encodage sécurisé sans dépendances externes.
    Encodage similaire à base64 mais avec une meilleure prise en charge des caractères Unicode.
    """
    # Alphabet standard pour l'encodage (similaire à base64 mais sûr pour les URLs)
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    
    # Convertir la chaîne en octets UTF-8
    bytes_data = text.encode('utf-8')
    
    # Convertir les octets en une chaîne binaire
    binary = ""
    for byte in bytes_data:
        binary += format(byte, '08b')  # Convertir en binaire sur 8 bits
    
    # Compléter avec des zéros pour avoir un multiple de 6 bits
    padding_needed = (6 - len(binary) % 6) % 6
    binary += "0" * padding_needed
    
    # Encoder par groupes de 6 bits
    result = ""
    for i in range(0, len(binary), 6):
        chunk = binary[i:i+6]
        index = int(chunk, 2)
        result += alphabet[index]
    
    return result

# Déchiffrement

def secure_decode(encoded):
    """
    Décodage sécurisé sans dépendances externes.
    """
    # Alphabet identique à celui utilisé pour l'encodage
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
    
    # Convertir l'encodage en bits
    binary = ""
    for char in encoded:
        if char in alphabet:
            index = alphabet.index(char)
            binary += format(index, '06b')  # 6 bits par caractère
    
    # Supprimer les bits de padding (si nécessaire)
    # Note: nous supprimons les bits qui ne complètent pas un octet entier
    remainder = len(binary) % 8
    if remainder != 0:
        binary = binary[:-remainder]
    
    # Convertir les bits en octets puis en chaîne UTF-8
    result_bytes = bytearray()
    for i in range(0, len(binary), 8):
        if i + 8 <= len(binary):  # S'assurer qu'on a un octet complet
            byte = int(binary[i:i+8], 2)
            result_bytes.append(byte)
    
    # Décoder les octets en chaîne UTF-8
    try:
        return result_bytes.decode('utf-8')
    except UnicodeDecodeError:
        # En cas d'erreur, essayer de récupérer ce qu'on peut
        return result_bytes.decode('utf-8', errors='replace')