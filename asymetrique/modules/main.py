import random
import string
import hashlib
import base64
import math

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

def demand_cipher_b64():
    while True:
        msg = input("\nMon message chiffré : ")
        if not msg:
            print("❌  Le message chiffré ne peut pas être vide.")
            continue
        return msg

def gcd(a, b):
    """PGCD avec l’algorithme d’Euclide."""
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
#  Génération de clés RSA
# --------------------------

def generate_keys(low=1000, high=5000):
    """
    - Choisit deux nombres premiers p, q dans [low, high].
    - Calcule n = p*q et phi(n) = (p-1)*(q-1).
    - Choisit e premier avec phi(n) et calcule d.
    """
    p = random.randint(low, high)
    while not is_prime(p):
        p = random.randint(low, high)
    q = random.randint(low, high)
    while not is_prime(q):
        q = random.randint(low, high)

    n = p * q
    phi_n = (p - 1) * (q - 1)
    e = random.randint(2, phi_n - 1)
    while gcd(e, phi_n) != 1:
        e = random.randint(2, phi_n - 1)
    d = modinv(e, phi_n)
    return (e, n), (d, n)

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
    cipher_bytes = base64.b64decode(cipher_b64)

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
        raise ValueError("Erreur de décodage Base64 : message corrompu")

    # 4. Retrait IV et sel
    if not full.startswith(iv):
        raise ValueError("IV invalide !")
    salted = full[len(iv):]
    original = ''.join(salted[i] for i in range(0, len(salted), 2))

    # Vérification d’intégrité (optionnelle)
    # if simple_hash(original) != simple_hash(original): ...
    return original

# --------------------------
#  Programme principal
# --------------------------

if __name__ == "__main__":

    iv = "4O6g9trUcd4C3DnQ"

    while True:
        try:
            choice = int(input("Que souhaitez-vous faire ?\n1. 🔑 Générer les clés.\n2. 🔐 Chiffrer mon message.\n3. 🔓 Déchiffrer mon message.\nMon choix : "))
        except ValueError:
            print("\n❌ Veuillez entrer un chiffre valide.\n")
            continue
        if choice == 1:
            public_key, private_key = generate_keys()
            print(f"✅ Clé publique (e, n) = {public_key}")
            print(f"🔐 Clé privée (d, n) = {private_key}")
        elif choice == 2:
            message = demand_msg()
            public_key = demand_key()
            salt = generate_salt()
            # iv = generate_iv()
            # print(f"IV : {iv}\n")
            cipher_b64 = encrypt(message, public_key, salt, iv)
            print(f"🔒 Message chiffré : {cipher_b64}\n")
        elif choice == 3:
            cipher_b64 = demand_cipher_b64()
            private_key = demand_key()
            # iv = demand_iv()
            try:
                decrypted = decrypt(cipher_b64, private_key, iv)
                print(f"🔓 Déchiffré : {decrypted}\n")
            except ValueError as err:
                print(f"⚠️ Erreur : {err}")
        else:
            print("❌ Veuillez choisir un chiffre valide.")
