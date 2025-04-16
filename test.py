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

def chiffrer(message, key):
    """
    Fonction de chiffrement MultiCrypt améliorée sans dépendances externes.
    Compatible avec les clés complexes contenant des caractères spéciaux.
    """
    if not message or not key:
        return "Erreur: Le message et la clé ne peuvent pas être vides."
    
    try:
        # Générer les valeurs dérivées de la clé
        key_values = generate_key_values(key)
        caesar_shift = key_values['caesar_shift']
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
        result = secure_encode(xored)
        return result
        
    except Exception as e:
        return f"Erreur lors du chiffrement: {str(e)}"

def dechiffrer(message_chiffre, key):
    """
    Fonction de déchiffrement MultiCrypt améliorée sans dépendances externes.
    """
    if not message_chiffre or not key:
        return "Erreur: Le message chiffré et la clé ne peuvent pas être vides."
    
    try:
        # Générer les mêmes valeurs dérivées de la clé
        key_values = generate_key_values(key)
        caesar_shift = key_values['caesar_shift']
        block_size = key_values['block_size']
        char_values = key_values['char_values']
        fingerprint = key_values['fingerprint']
        fingerprint_length = len(fingerprint)
        
        # Étape 1: Décodage
        try:
            decoded = secure_decode(message_chiffre)
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


if __name__ == "__main__":
    print("=== Exegolencrypt ===")
    
    while True:
        print("\nQue souhaitez-vous faire?")
        print("1. Chiffrer un message")
        print("2. Déchiffrer un message")
        print("3. Quitter")
        
        choix = input("Votre choix (1/2/3): ")
        
        if choix == "1":
            message = input("Entrez le message à chiffrer: ")
            key = input("Entrez la clé de chiffrement: ")
            
            message_chiffre = chiffrer(message, key)
            print(f"\nMessage chiffré: {message_chiffre}")
            
        elif choix == "2":
            message_chiffre = input("Entrez le message chiffré: ")
            key = input("Entrez la clé de déchiffrement: ")
            
            message_dechiffre = dechiffrer(message_chiffre, key)
            print(f"\nMessage déchiffré: {message_dechiffre}")
            
        elif choix == "3":
            print("Au revoir!")
            break
            
        else:
            print("Choix invalide. Veuillez réessayer.")