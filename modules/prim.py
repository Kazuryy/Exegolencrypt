# Appel des fonctions (étapes de chiffrement et déchiffrement)
from . import second
# Chiffrement

def steps_chiff():
    msg, key = second.demand_msg_key()
    return msg

# Déchiffrement

...