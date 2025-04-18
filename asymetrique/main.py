import random
import string
import hashlib
import base64
import math
import json
import os
import sys

# Ajout du chemin pour pouvoir importer les modules de chiffrement symétrique
# Nous avons besoin de garder cet import pour le chiffrement des clés privées
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from symetrique.modules import prim as sym_prim

# --------------------------
#  Fonctions utilitaires
# --------------------------

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

def demand_username():
    username = input("\nQui êtes-vous ? (nom d'utilisateur) : ")
    return username.strip()

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
    """Inverse modulaire de e modulo phi_n."""
    for d in range(1, phi_n):
        if (e * d) % phi_n == 1:
            return d
    return None

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
        if decrypted_json.startswith("Erreur"):
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

def register_new_user(username):
    """Enregistre un nouvel utilisateur avec ses clés"""
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
    
    return public_key

# --------------------------
#  Génération de clés RSA
# --------------------------

def generate_keys(key_size=1024):
    """
    Génère une paire de clés RSA de taille spécifiée.
    
    Args:
        key_size (int): Taille approximative de la clé en bits (par défaut 1024)
    
    Returns:
        tuple: ((e, n), (d, n)) - clé publique et clé privée
    """
    # Déterminer la taille approximative de p et q
    # Pour une clé de n bits, p et q doivent être d'environ n/2 bits
    bit_size = key_size // 2
    
    # Calculer les limites approximatives pour p et q
    # 2^(bit_size-1) à 2^bit_size - 1
    low = 2 ** (bit_size - 1)
    high = 2 ** bit_size - 1
    
    print(f"⏳ Génération de nombres premiers ({bit_size} bits)... Cela peut prendre un moment.")
    
    # Générer p
    p = random.randint(low, high)
    # Pour un test de primalité plus efficace sur de grands nombres, 
    # nous utilisons un test probabiliste (Miller-Rabin)
    while not isProbablePrime(p):
        p = random.randint(low, high)
    
    # Générer q (différent de p)
    q = random.randint(low, high)
    while not isProbablePrime(q) or q == p:
        q = random.randint(low, high)
        
    print("✅ Nombres premiers générés!")
    
    n = p * q
    phi_n = (p - 1) * (q - 1)
    
    # Une valeur e commune est 65537 (0x10001), qui est un nombre premier
    # avec des caractéristiques pratiques pour le chiffrement RSA
    e = 65537
    
    # Vérifier que e est premier avec phi_n
    if gcd(e, phi_n) != 1:
        # Si ce n'est pas le cas (rare), on en cherche un autre
        e = random.randint(3, phi_n - 1)
        while gcd(e, phi_n) != 1:
            e = random.randint(3, phi_n - 1)
    
    # Calculer d, l'inverse modulaire de e mod phi_n
    d = modinv(e, phi_n)
    
    return (e, n), (d, n)

def isProbablePrime(n, k=5):
    """
    Test de primalité Miller-Rabin.
    
    Args:
        n (int): Nombre à tester
        k (int): Nombre d'itérations (plus k est grand, plus le test est précis)
    
    Returns:
        bool: True si n est probablement premier, False sinon
    """
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # Écrire n-1 sous la forme 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Témoin de primalité
    for _ in range(k):
        a = random.randint(2, n - 2)
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

def asymmetric_encryption_menu(username):
    """Menu pour le chiffrement asymétrique"""
    while True:
        try:
            choice = int(input("\nQue souhaitez-vous faire ?\n1. 🔐 Chiffrer un message\n2. 🔓 Déchiffrer un message\n3. 🔙 Retour\nMon choix : "))
            
            if choice == 1:
                encrypt_message_for_user(username)
            elif choice == 2:
                decrypt_message_for_user(username)
            elif choice == 3:
                return
            else:
                print("❌ Veuillez entrer un choix valide.")
        except ValueError:
            print("❌ Veuillez entrer un chiffre valide.")

def encrypt_message_for_user(recipient_username):
    """Chiffrer un message avec la clé publique d'un utilisateur"""
    # Demander le nom du destinataire
    dest_username = input("\nPour qui est ce message? (nom d'utilisateur) : ")
    
    # Vérifier si l'utilisateur existe
    if not user_exists(dest_username):
        print(f"❌ Utilisateur {dest_username} introuvable.")
        return
    
    # Récupérer la clé publique du destinataire
    user_data = get_user_keys(dest_username)
    public_key = user_data["public_key"]
    
    # Demander le message à chiffrer
    message = demand_msg()
    
    # Paramètres pour le chiffrement
    iv = "4O6g9trUcd4C3DnQ"
    salt = generate_salt()
    
    # Chiffrer le message
    try:
        cipher_b64 = encrypt(message, public_key, salt, iv)
        print(f"🔒 Message chiffré pour {dest_username} : {cipher_b64}\n")
    except Exception as e:
        print(f"❌ Erreur lors du chiffrement : {str(e)}")

def decrypt_message_for_user(username):
    """Déchiffrer un message avec la clé privée de l'utilisateur"""
    # Demander le message chiffré
    cipher_b64 = demand_cipher_b64()
    
    # Demander la clé symétrique pour déchiffrer la clé privée
    sym_key = demand_symmetric_key()
    
    # Récupérer et déchiffrer la clé privée
    private_key = get_decrypted_private_key(username, sym_key)
    
    if not private_key:
        return
    
    # Paramètres pour le déchiffrement
    iv = "4O6g9trUcd4C3DnQ"
    
    # Déchiffrer le message
    try:
        decrypted = decrypt(cipher_b64, private_key, iv)
        print(f"🔓 Message déchiffré : {decrypted}\n")
    except ValueError as err:
        print(f"⚠️ Erreur : {err}")
    except Exception as e:
        print(f"❌ Erreur lors du déchiffrement : {str(e)}")

# Cette fonction a été retirée car le chiffrement symétrique est géré par master_main.py

# --------------------------
#  Programme principal
# --------------------------

def main():
    print("\n🔐 Programme de cryptographie asymétrique 🔑\n")
    
    # Demander l'identité de l'utilisateur
    username = demand_username()
    
    # Vérifier si l'utilisateur existe déjà
    if not user_exists(username):
        print(f"\n👤 Bienvenue {username}, vous êtes un nouvel utilisateur.")
        register_new_user(username)
    else:
        print(f"\n👋 Bon retour parmi nous, {username}!")
    
    # Menu principal
    while True:
        # Cryptographie asymétrique directement sans choix
        asymmetric_encryption_menu(username)
            
        # Demander si l'utilisateur veut continuer
        continue_choice = input("\nVoulez-vous continuer? (o/n): ").lower()
        if continue_choice != 'o':
            print("\n👋 Merci d'avoir utilisé notre programme de cryptographie. À bientôt!")
            break

if __name__ == "__main__":
    main()