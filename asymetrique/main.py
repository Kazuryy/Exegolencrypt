import random
import string
import hashlib
import base64
import math
import json
import os
import sys
import datetime

# Ajout du chemin pour pouvoir importer les modules de chiffrement symétrique
# Nous avons besoin de garder cet import pour le chiffrement des clés privées
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from symetrique.modules import prim as sym_prim

# --------------------------
#  Fonctions utilitaires
# --------------------------

def save_to_file(content, default_name, extension='.txt'):
    """Fonction utilitaire pour sauvegarder du contenu dans un fichier."""
    # Proposer un nom de fichier par défaut
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    default_filename = f"{default_name}_{current_time}{extension}"
    
    filename = input(f"\nNom du fichier [{default_filename}]: ").strip()
    if not filename:
        filename = default_filename
    
    # Ajouter l'extension si nécessaire
    if not filename.endswith(extension):
        filename += extension
    
    # Sauvegarder dans le répertoire courant
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"\n✅ Fichier sauvegardé avec succès: {filename}")
        return True
    except Exception as e:
        print(f"\n❌ Erreur lors de la sauvegarde du fichier: {str(e)}")
        return False

def load_from_file(extension='.txt'):
    """Fonction utilitaire pour charger du contenu depuis un fichier."""
    # Lister les fichiers avec l'extension spécifiée
    files = [f for f in os.listdir('.') if os.path.isfile(f) and f.endswith(extension)]
    
    if not files:
        print(f"\n❌ Aucun fichier {extension} trouvé dans le répertoire courant.")
        return None
    
    # Afficher les fichiers disponibles
    print(f"\nFichiers {extension} disponibles:")
    for i, file in enumerate(files, 1):
        print(f"{i}. {file}")
    
    # Demander à l'utilisateur de choisir un fichier
    while True:
        try:
            choice = input("\nChoisissez un fichier (numéro) ou entrez le nom complet: ")
            
            # Si c'est un numéro
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(files):
                    filename = files[idx]
                    break
                else:
                    print("❌ Numéro invalide.")
            except ValueError:
                # Si c'est un nom de fichier
                if choice in files:
                    filename = choice
                    break
                elif choice + extension in files:
                    filename = choice + extension
                    break
                else:
                    print("❌ Fichier non trouvé.")
        except KeyboardInterrupt:
            return None
    
    # Charger le contenu du fichier
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        print(f"\n✅ Fichier chargé avec succès: {filename}")
        return content
    except Exception as e:
        print(f"\n❌ Erreur lors du chargement du fichier: {str(e)}")
        return None

def demand_msg():
    while True:
        msg = input("\nMon message : ")
        if not msg:
            print("❌  Le message ne peut pas être vide.")
            continue
        return msg

def demand_key():
    while True:
        key_str = input("\nMa clé (format : 123,456 ou (123, 456)) : ").strip()
        
        # Nettoie les parenthèses s'il y en a
        if key_str.startswith("(") and key_str.endswith(")"):
            key_str = key_str[1:-1]

        parts = key_str.split(",")

        if len(parts) != 2:
            print("❌ Format invalide. Attendu : deux entiers séparés par une virgule.")
            continue

        try:
            e_or_d = int(parts[0].strip())
            n = int(parts[1].strip())
            return (e_or_d, n)
        except ValueError:
            print("❌ La clé doit contenir deux entiers.")

def demand_symmetric_key():
    while True:
        key = input("\nEntrez votre clé de protection (pour le chiffrement symétrique) : ")
        if not key:
            print("❌ La clé ne peut pas être vide.")
            continue
        return key

def demand_cipher_b64():
    while True:
        msg = input("\nMon message chiffré : ")
        if not msg:
            print("❌  Le message chiffré ne peut pas être vide.")
            continue
        return msg

def gcd(a, b):
    """PGCD avec l'algorithme d'Euclide."""
    while b != 0:
        a, b = b, a % b
    return a

def modinv(e, phi_n):
    """
    Calcule l'inverse modulaire de e modulo phi_n de manière plus efficace.
    Utilise l'algorithme d'Euclide étendu.
    """
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x
    
    gcd, x, y = extended_gcd(e, phi_n)
    
    if gcd != 1:
        return None  # L'inverse modulaire n'existe pas
    else:
        return x % phi_n

def is_prime(num):
    """Test de primalité simple."""
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def generate_salt(length=16):
    """Génère un sel aléatoire."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def simple_hash(message):
    """SHA-256 du message."""
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

# --------------------------
#  Gestion des utilisateurs et clés
# --------------------------

def get_keys_path():
    """Chemin vers le fichier de clés"""
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "users_keys.json")

def load_user_keys():
    """Charge les clés des utilisateurs depuis le fichier JSON"""
    keys_path = get_keys_path()
    if not os.path.exists(keys_path):
        return {}
    
    try:
        with open(keys_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_user_keys(users_keys):
    """Enregistre les clés des utilisateurs dans le fichier JSON"""
    keys_path = get_keys_path()
    os.makedirs(os.path.dirname(keys_path), exist_ok=True)
    
    with open(keys_path, "w") as f:
        json.dump(users_keys, f, indent=4)

def user_exists(username):
    """Vérifie si un utilisateur existe déjà"""
    users_keys = load_user_keys()
    return username in users_keys

def get_user_keys(username):
    """Récupère les clés d'un utilisateur"""
    users_keys = load_user_keys()
    return users_keys.get(username, None)

def list_users():
    """Liste tous les utilisateurs enregistrés"""
    users_keys = load_user_keys()
    
    if not users_keys:
        print("\n📝 Aucun utilisateur enregistré.")
        return []
    
    print("\n📝 Liste des utilisateurs enregistrés:")
    users = list(users_keys.keys())
    for i, username in enumerate(users, 1):
        print(f"{i}. {username}")
    
    return users

def select_user_from_list():
    """Demande à l'utilisateur de sélectionner un utilisateur dans la liste"""
    users = list_users()
    
    if not users:
        return None
    
    while True:
        try:
            choice = input("\nSélectionnez un utilisateur (numéro) ou entrez un nouveau nom: ")
            
            # Vérifier si l'entrée est un numéro
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(users):
                    return users[idx]
                else:
                    print("❌ Numéro invalide.")
                    continue
            except ValueError:
                # L'entrée n'est pas un numéro, on la considère comme un nouveau nom
                if choice.strip():
                    return choice.strip()
                else:
                    print("❌ Veuillez entrer un nom valide.")
        
        except KeyboardInterrupt:
            return None

def get_decrypted_private_key(username, sym_key):
    """Récupère et déchiffre la clé privée d'un utilisateur"""
    user_data = get_user_keys(username)
    if not user_data:
        print(f"❌ Utilisateur {username} introuvable.")
        return None
    
    # Déchiffrement de la clé privée avec la clé symétrique
    encrypted_private_key = user_data["encrypted_private_key"]
    
    try:
        # Déchiffrer la représentation JSON de la clé privée
        decrypted_json = sym_prim.dechiffrer(encrypted_private_key, sym_key)
        if isinstance(decrypted_json, str) and decrypted_json.startswith("Erreur"):
            print(f"❌ {decrypted_json}")
            return None
            
        # Convertir la chaîne JSON en tuple
        try:
            # Essayer de charger en tant que JSON
            key_data = json.loads(decrypted_json)
            return (key_data[0], key_data[1])
        except json.JSONDecodeError:
            print("❌ Erreur de décodage de la clé privée.")
            return None
    except Exception as e:
        print(f"❌ Erreur lors du déchiffrement de la clé privée: {str(e)}")
        return None

def register_new_user():
    """Enregistre un nouvel utilisateur avec ses clés"""
    # Demander le nom d'utilisateur
    while True:
        username = input("\nNom d'utilisateur : ").strip()
        if not username:
            print("❌ Le nom d'utilisateur ne peut pas être vide.")
            continue
        
        if user_exists(username):
            print(f"❌ L'utilisateur {username} existe déjà.")
            continue
        
        break
    
    print(f"\n🔐 Génération des clés pour {username}...")
    public_key, private_key = generate_keys()
    
    # Demander une clé symétrique pour protéger la clé privée
    sym_key = demand_symmetric_key()
    
    # Convertir le tuple de clé privée en JSON pour le chiffrement
    private_key_json = json.dumps(private_key)
    
    # Chiffrer la clé privée avec le chiffrement symétrique
    encrypted_private_key = sym_prim.chiffrer(private_key_json, sym_key)
    
    # Enregistrer les clés
    users_keys = load_user_keys()
    users_keys[username] = {
        "public_key": public_key,
        "encrypted_private_key": encrypted_private_key
    }
    save_user_keys(users_keys)
    
    print(f"✅ Clés générées et enregistrées pour {username}")
    print(f"🔑 Clé publique (e, n) = {public_key}")
    print(f"⚠️ Votre clé privée est protégée par chiffrement symétrique.")
    print(f"⚠️ N'oubliez pas votre clé de protection symétrique!")
    
    return username

# --------------------------
#  Génération de clés RSA
# --------------------------

def generate_keys(key_size=1024):
    """
    Génère une paire de clés RSA de taille spécifiée de manière optimisée.
    
    Args:
        key_size (int): Taille approximative de la clé en bits
    
    Returns:
        tuple: ((e, n), (d, n)) - clé publique et clé privée
    """
    # Taille des nombres premiers (la moitié de la taille de la clé)
    bit_size = key_size // 2
    
    # Générer deux nombres premiers distincts
    p = generate_prime(bit_size)
    q = generate_prime(bit_size)
    
    # S'assurer que p et q sont distincts
    while p == q:
        q = generate_prime(bit_size)
    
    # Calculer n et phi(n)
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    # Exposant public standard: 65537 (0x10001)
    e = 65537
    
    # Vérifier que e est premier avec phi_n
    while gcd(e, phi_n) != 1:
        # Choisir un autre exposant si nécessaire (rare)
        e = 65539  # Prochain nombre premier après 65537
        
        if gcd(e, phi_n) != 1:
            e = 65521  # Plus grand nombre premier inférieur à 65536
            
            # Si toujours pas, utiliser une recherche plus étendue
            if gcd(e, phi_n) != 1:
                e = find_coprime(phi_n)
    
    # Calculer l'exposant privé d
    d = efficient_modinv(e, phi_n)
    
    # Double vérification: e*d ≡ 1 (mod phi_n)
    assert (e * d) % phi_n == 1, "Erreur dans le calcul de l'inverse modulaire"
    
    return (e, n), (d, n)

def generate_prime(bits):
    """
    Génère un nombre premier de la taille spécifiée en bits
    en utilisant une approche optimisée.
    """
    # Liste des petits nombres premiers pour un test de divisibilité rapide
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    
    # Garantir que le nombre est dans la plage correcte: [2^(bits-1), 2^bits - 1]
    min_val = 1 << (bits - 1)
    max_val = (1 << bits) - 1
    
    while True:
        # Générer un nombre impair dans la plage
        candidate = random.randrange(min_val, max_val) | 1
        
        # Test rapide de divisibilité par les petits nombres premiers
        is_divisible = False
        for prime in small_primes:
            if candidate % prime == 0 and candidate > prime:
                is_divisible = True
                break
        
        if is_divisible:
            continue
        
        # Test de Miller-Rabin avec 7 itérations (probabilité d'erreur < 2^-56)
        if is_probable_prime(candidate, 7):
            return candidate

def is_probable_prime(n, k=7):
    """
    Test de primalité de Miller-Rabin optimisé.
    
    Args:
        n: Nombre à tester
        k: Nombre d'itérations (plus k est grand, plus le test est précis)
    
    Returns:
        bool: True si n est probablement premier, False s'il est composé
    """
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    
    # Écrire n-1 comme d*2^r
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Témoins pour le test de Miller-Rabin
    # Pour n < 2⁶⁴, ces témoins garantissent la certitude
    witnesses = [2, 3, 5, 7, 11, 13, 17]
    if k < len(witnesses):
        witnesses = witnesses[:k]
    
    # Test de Miller-Rabin
    for a in witnesses:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def efficient_modinv(a, m):
    """
    Calcule l'inverse modulaire a^(-1) mod m efficacement
    en utilisant l'algorithme d'Euclide étendu itératif.
    """
    if gcd(a, m) != 1:
        raise ValueError("L'inverse modulaire n'existe pas")
    
    # Algorithme d'Euclide étendu itératif
    x0, x1, y0, y1 = 1, 0, 0, 1
    a0, m0 = a, m
    
    while m0 > 0:
        q = a0 // m0
        a0, m0 = m0, a0 - q * m0
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    
    # Normaliser le résultat pour qu'il soit positif
    return x0 % m

def find_coprime(n):
    """
    Trouve un nombre premier avec n en commençant à partir de 3.
    """
    e = 3
    while gcd(e, n) != 1:
        e += 2
    return e

# --------------------------
#  Chiffrement / Déchiffrement
# --------------------------

def encrypt(message, public_key, salt, iv):
    """
    1. Salage caractère à caractère.
    2. Préfixe IV.
    3. Encodage Base64.
    4. Chiffrement RSA.
    5. Encodage Base64 du flux chiffré.
    """
    e, n = public_key

    # 1. Salage
    salted = ''.join(message[i] + salt[i % len(salt)] for i in range(len(message)))
    # 2. Préfixe IV
    iv_msg = iv + salted
    # 3. Base64
    b64_plain = base64.b64encode(iv_msg.encode('utf-8'))

    # 4. RSA : bloc de taille fixe en octets
    block_size = math.ceil(n.bit_length() / 8)
    cipher_bytes = bytearray()
    for byte in b64_plain:
        c = pow(byte, e, n)
        # chaque bloc devient block_size octets big‑endian
        cipher_bytes += c.to_bytes(block_size, byteorder='big')

    # 5. Encode en Base64 pour produire une chaîne ASCII
    return base64.b64encode(bytes(cipher_bytes)).decode('ascii')


def decrypt(cipher_b64, private_key, iv):
    """
    1. Décodage Base64 du flux chiffré.
    2. Découpage en blocs et déchiffrement RSA.
    3. Décodage Base64 pour retrouver IV+salted.
    4. Retrait IV et retrait sel.
    """
    d, n = private_key
    block_size = math.ceil(n.bit_length() / 8)

    # 1. Base64 → bytes chiffrés
    try:
        cipher_bytes = base64.b64decode(cipher_b64)
    except Exception:
        raise ValueError("Erreur de décodage Base64 : message corrompu")

    # 2. Découpe en blocs et déchiffrement RSA
    plain_bytes = bytearray()
    for i in range(0, len(cipher_bytes), block_size):
        block = cipher_bytes[i:i+block_size]
        c = int.from_bytes(block, byteorder='big')
        m = pow(c, d, n)
        # m doit être un octet unique (0–255)
        plain_bytes.append(m)

    # 3. Base64 inverse pour retrouver la chaîne iv+salted
    try:
        full = base64.b64decode(bytes(plain_bytes)).decode('utf-8')
    except Exception:
        raise ValueError("Erreur de décodage Base64 : message corrompu")

    # 4. Retrait IV et sel
    if not full.startswith(iv):
        raise ValueError("IV invalide !")
    salted = full[len(iv):]
    original = ''.join(salted[i] for i in range(0, len(salted), 2))

    # Vérification d'intégrité (optionnelle)
    # if simple_hash(original) != simple_hash(original): ...
    return original

# --------------------------
#  Fonctions d'interface utilisateur
# --------------------------

def asymmetric_encryption_menu():
    """Menu pour le chiffrement asymétrique"""
    while True:
        try:
            print("\nQue souhaitez-vous faire ?")
            print("1. 🔒 Chiffrer un message")
            print("2. 🔓 Déchiffrer un message")
            print("3. 👤 Créer un nouvel utilisateur")
            print("4. 🔙 Retour")
            
            choice = input("\nMon choix : ")
            
            if choice == "1":
                encrypt_message()
            elif choice == "2":
                decrypt_message()
            elif choice == "3":
                register_new_user()
            elif choice == "4":
                return
            else:
                print("❌ Veuillez entrer un choix valide.")
        except KeyboardInterrupt:
            print("\n\n👋 Action interrompue.")
            return
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")

def encrypt_message():
    """Chiffrer un message avec la clé publique d'un utilisateur"""
    print("\n🔒 Chiffrement de message")
    print("Pour chiffrer un message, vous avez besoin de la clé publique du destinataire.")
    
    # Demander avec quelle clé publique chiffrer
    print("\nÀ qui voulez-vous envoyer un message ? ")
    
    # Liste les utilisateurs enregistrés
    username = select_user_from_list()
    
    if not username:
        print("❌ Opération annulée.")
        return
    
    # Si l'utilisateur n'existe pas, proposer de le créer
    if not user_exists(username):
        print(f"\n❔ L'utilisateur {username} n'existe pas.")
        create_new = input("Voulez-vous créer ce nouvel utilisateur? (o/n): ").lower()
        
        if create_new == 'o':
            username = register_new_user()
        else:
            print("❌ Opération annulée.")
            return
    
    # Récupérer la clé publique
    user_data = get_user_keys(username)
    if not user_data:
        print("❌ Impossible de récupérer les informations de l'utilisateur.")
        return
    
    public_key = user_data["public_key"]
    print(f"\n✅ Clé publique de {username} récupérée: {public_key}")
    
    # Demander le message à chiffrer - avec option de charger depuis un fichier
    print("\nComment souhaitez-vous entrer votre message?\n")
    print("1. Saisir le message directement")
    print("2. Charger le message depuis un fichier")
    
    input_choice = input("\nVotre choix: ")
    
    if input_choice == "2":
        message_content = load_from_file()
        if not message_content:
            print("❌ Impossible de charger le message depuis un fichier.")
            return
        message = message_content
    else:
        message = demand_msg()
    
    # Paramètres pour le chiffrement
    iv = "4O6g9trUcd4C3DnQ"
    salt = generate_salt()
    
    # Chiffrer le message
    try:
        cipher_b64 = encrypt(message, public_key, salt, iv)
        
        # Afficher un aperçu du message chiffré
        preview_length = 50  # Longueur de l'aperçu
        preview = cipher_b64[:preview_length] + ("..." if len(cipher_b64) > preview_length else "")
        print(f"\n🔒 Message chiffré pour {username} (aperçu): {preview}")
        
        # Proposer de sauvegarder le message chiffré dans un fichier
        print("\nLe message chiffré va être stocké dans le fichier suivant :")
        save_to_file(cipher_b64, f"message_chiffre_pour_{username}", ".enc")
        print(f"\n✅ Message chiffré et sauvegardé avec succès : message_chiffre_pour_{username}.enc")

    
        
    except Exception as e:
        print(f"❌ Erreur lors du chiffrement: {str(e)}")

def decrypt_message():
    """Déchiffrer un message avec la clé privée d'un utilisateur"""
    print("\n🔓 Déchiffrement de message")
    print("Pour déchiffrer un message, vous avez besoin de la clé privée du destinataire du message.")
    
    # Demander avec quelle clé privée déchiffrer
    print("\nQui est le destinataire du message ? ")
    
    # Liste les utilisateurs enregistrés
    username = select_user_from_list()
    
    if not username:
        print("❌ Opération annulée.")
        return
    
    # Si l'utilisateur n'existe pas, informer
    if not user_exists(username):
        print(f"\n❌ L'utilisateur {username} n'existe pas. Impossible de déchiffrer.")
        return
    
    # Demander la clé symétrique pour déchiffrer la clé privée
    sym_key = demand_symmetric_key()
    
    # Récupérer et déchiffrer la clé privée
    private_key = get_decrypted_private_key(username, sym_key)
    
    if not private_key:
        return
    
    print(f"\n✅ Clé privée de {username} déchiffrée avec succès.")
    
    # Demander le message chiffré - avec option de charger depuis un fichier
    print("\nComment souhaitez-vous entrer le message chiffré?\n")
    print("1. Saisir le message chiffré directement")
    print("2. Charger le message chiffré depuis un fichier")
    
    input_choice = input("\nVotre choix: ")
    
    if input_choice == "2":
        cipher_content = load_from_file(".enc")
        if not cipher_content:
            print("❌ Impossible de charger le message chiffré depuis un fichier.")
            return
        cipher_b64 = cipher_content
    else:
        cipher_b64 = demand_cipher_b64()
    
    # Paramètres pour le déchiffrement
    iv = "4O6g9trUcd4C3DnQ"
    
    # Déchiffrer le message
    try:
        decrypted = decrypt(cipher_b64, private_key, iv)
        
        # Afficher un aperçu du message
        preview_length = 100  # Longueur de l'aperçu
        preview = decrypted[:preview_length] + ("..." if len(decrypted) > preview_length else "")
        print(f"\n🔓 Message déchiffré (aperçu): {preview}")
        
        # Proposer de sauvegarder le message dans un fichier
        save_option = input("\nSouhaitez-vous sauvegarder le message déchiffré dans un fichier? (o/n): ").lower()
        
        if save_option == 'o':
            save_to_file(decrypted, "message_dechiffre")
        else:
            # Si l'utilisateur refuse la sauvegarde, proposer d'afficher le message complet
            view_option = input("\nSouhaitez-vous afficher le message complet dans le terminal? (o/n): ").lower()
            if view_option == 'o':
                print(f"\n📄 Message complet:\n{decrypted}")
            
    except ValueError as err:
        print(f"⚠️ Erreur: {err}")
    except Exception as e:
        print(f"❌ Erreur lors du déchiffrement: {str(e)}")

# --------------------------
#  Programme principal
# --------------------------

def main():
    print("\n🔐 Programme de cryptographie asymétrique 🔑\n")
    
    # Menu principal - On passe directement à l'encryption asymétrique
    asymmetric_encryption_menu()
    
    print("\n👋 Merci d'avoir utilisé notre programme de cryptographie. À bientôt!")

if __name__ == "__main__":
    main()