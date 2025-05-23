# ExegolEncrypt: Système de Cryptographie Galactique

## Transmission Impériale Confidentielle

Ce système de cryptographie a été développé par les ingénieurs de la dernière flotte Sith sur Exegol pour protéger les communications sensibles à travers la galaxie. Il vous est fourni pour évaluation et analyse.

## Prérequis de Déploiement

- Python 3.6 ou supérieur (compatible avec les systèmes de la République et de l'Empire)
- Tkinter (préinstallé dans la plupart des terminaux galactiques)

## Installation sur Terminal Galactique

Aucun droïde de maintenance n'est nécessaire pour l'installation. Le système fonctionne avec les composants standards de Python, sans dépendances externes comme si la Force était avec vous.

## Protocole d'Utilisation

### Activation du système

Pour lancer le système de cryptographie, exécutez le fichier de commande principal :

```bash
python master_main.py
```

### Interface de Contrôle

Le système présente une interface similaire aux terminaux de l'Étoile de la Mort, offrant deux protocoles de cryptographie distincts :

1. **Protocole Symétrique (Voie Jedi)** - Utilise une clé unique pour encoder et décoder, comme un sabre laser à double lame
2. **Protocole Asymétrique (Voie Sith)** - Utilise des paires de clés, comme maître et apprenti travaillant ensemble

#### Protocole Symétrique (KyberCrypt)

Dans ce mode, vous pouvez :
- Chiffrer/déchiffrer un datapad (fichier texte)
- Encoder/décoder un message holographique directement dans le terminal
- Sécuriser/désécuriser un secteur entier de données (crée un fichier .exegolencrypt)

La sécurité repose sur un code secret que vous devez protéger avec autant de soin qu'un cristal Kyber.

**⚠️ Avertissement crucial** : À l'instar des premiers condensateurs de l'Étoile de la Mort, ce système n'est pas optimisé pour traiter des volumes importants de données. Évitez de chiffrer des fichiers ou dossiers trop volumineux, sous peine de surcharge et de défaillance du système. Les ingénieurs impériaux travaillent à résoudre cette limitation. (En gros pas de dissier de centaines de MO)

#### Protocole Asymétrique

Dans ce mode, vous pouvez :
- Créer une nouvelle identité galactique (génère une paire de clés)
- Encoder un message avec la clé publique d'un utilisateur
- Décoder un message avec votre clé privée

Le système stocke les clés publiques dans les archives de l'Ordre Jedi (fichier JSON). Les clés privées sont protégées par un chiffrement supplémentaire, comme les secrets du côté obscur.

## Cartographie des Archives Impériales

```
/
├── master_main.py             # Centre de commande principal
├── .gitignore                 # Liste des données à maintenir secrètes
├── symetrique/                # Module de cryptographie de la Voie Jedi (KyberCrypt)
│   ├── main.py                # Interface pour la cryptographie symétrique
│   └── modules/               # Composants du côté lumineux
│       ├── __init__.py        # Initiateur de la Force
│       ├── prim.py            # Fonctions d'encodage/décodage primaires
│       └── second.py          # Fonctions utilitaires secondaires
├── asymetrique.exegolencrypt  # Module de cryptographie de la Voie Sith (accès restreint)
```

> **Note** : Le fichier asymetrique.exegolencrypt doit être déchiffré avec KyberCrypt avant utilisation. Examinez le format d'extension des fichiers chiffrés pour découvrir la clé.

---

**Avertissement Impérial** : Ce système est fourni pour entraînement uniquement. Toute utilisation non autorisée sera sanctionnée par les Inquisiteurs.
