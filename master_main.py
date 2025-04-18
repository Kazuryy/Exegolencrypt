import os
import sys
import importlib.util

def clear_screen():
    """Efface l'écran de la console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Affiche l'en-tête du programme"""
    clear_screen()
    print("=" * 70)
    print("🔐 PROGRAMME DE CRYPTOGRAPHIE AVANCÉE 🔑".center(70))
    print("=" * 70)
    print()

def print_error(message):
    """Affiche un message d'erreur"""
    print(f"\n❌ {message}")

def load_module(module_path, module_name):
    """
    Charge dynamiquement un module Python à partir d'un chemin de fichier
    
    Args:
        module_path (str): Chemin vers le fichier .py à charger
        module_name (str): Nom à donner au module
        
    Returns:
        module: Le module chargé ou None en cas d'erreur
    """
    try:
        # Vérifier que le fichier existe
        if not os.path.exists(module_path):
            print_error(f"Le fichier {module_path} n'existe pas.")
            return None
            
        # Charger le module
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        if spec is None:
            print_error(f"Impossible de charger le module depuis {module_path}")
            return None
            
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        return module
    except Exception as e:
        print_error(f"Erreur lors du chargement du module {module_name}: {str(e)}")
        return None

def get_module_path(module_name):
    """
    Détermine le chemin vers un module spécifique
    
    Args:
        module_name (str): Nom du module ('symetrique' ou 'asymetrique')
        
    Returns:
        str: Chemin vers le fichier main.py du module
    """
    # Chemin du répertoire courant (où se trouve master_main.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construction du chemin vers le module
    module_path = os.path.join(base_dir, module_name, "main.py")
    return module_path

def execute_symmetrique():
    """Exécute le module de chiffrement symétrique"""
    print("\n🔄 Chargement du module de chiffrement symétrique...")
    
    # Base directory où se trouve master_main.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # S'assurer que le répertoire symetrique est dans le chemin Python
    sym_dir = os.path.join(base_dir, "symetrique")
    if sym_dir not in sys.path:
        sys.path.insert(0, sym_dir)
    
    # Chemin complet vers le répertoire modules
    modules_dir = os.path.join(sym_dir, "modules")
    if modules_dir not in sys.path:
        sys.path.insert(0, modules_dir)
    
    # Chemin vers le module symétrique main.py
    sym_path = os.path.join(sym_dir, "main.py")
    
    # Sauvegarder l'état actuel
    old_cwd = os.getcwd()
    old_path = sys.path.copy()
    
    try:
        # Changer le répertoire de travail pour faciliter les imports relatifs
        os.chdir(sym_dir)
        
        # Essayer de charger et exécuter le module
        sym_module = load_module(sym_path, "sym_module")
        if sym_module and hasattr(sym_module, "main"):
            sym_module.main()
        else:
            print_error("Le module symétrique n'a pas pu être chargé correctement.")
    except Exception as e:
        print_error(f"Erreur lors de l'exécution du module symétrique: {str(e)}")
    finally:
        # Restaurer l'état
        os.chdir(old_cwd)
        sys.path = old_path

def execute_asymetrique():
    """Exécute le module de chiffrement asymétrique"""
    print("\n🔄 Chargement du module de chiffrement asymétrique...")
    
    # Base directory où se trouve master_main.py
    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Chemin vers le répertoire asymétrique
    asym_dir = os.path.join(base_dir, "asymetrique")
    
    # Chemin vers le module asymétrique main.py
    asym_path = os.path.join(asym_dir, "main.py")
    
    # Sauvegarder l'état actuel
    old_cwd = os.getcwd()
    old_path = sys.path.copy()
    
    try:
        # S'assurer que les chemins nécessaires sont dans sys.path
        if base_dir not in sys.path:
            sys.path.insert(0, base_dir)
        
        if asym_dir not in sys.path:
            sys.path.insert(0, asym_dir)
        
        # Changer le répertoire de travail pour faciliter les imports
        os.chdir(asym_dir)
        
        # Charger et exécuter le module
        asym_module = load_module(asym_path, "asym_module")
        if asym_module and hasattr(asym_module, "main"):
            asym_module.main()
        else:
            print_error("Le module asymétrique n'a pas pu être chargé correctement.")
    except Exception as e:
        print_error(f"Erreur lors de l'exécution du module asymétrique: {str(e)}")
    finally:
        # Restaurer l'état
        os.chdir(old_cwd)
        sys.path = old_path

def main():
    """Fonction principale"""
    while True:
        print_header()
        print("Bienvenue dans votre programme de cryptographie!")
        print("\nQuel type de cryptographie souhaitez-vous utiliser?")
        print("1. 🔑 Cryptographie symétrique")
        print("2. 🔐 Cryptographie asymétrique")
        print("3. ❌ Quitter le programme")
        print()
        
        try:
            choice = input("Votre choix [1-3]: ")
            
            if choice == "1":
                execute_symmetrique()
            elif choice == "2":
                execute_asymetrique()
            elif choice == "3":
                print("\n👋 Merci d'avoir utilisé notre programme de cryptographie. À bientôt!")
                break
            else:
                print_error("Choix invalide. Veuillez entrer un nombre entre 1 et 3.")
            
            # Demander si l'utilisateur veut continuer
            print("\n")
            continue_choice = input("Voulez-vous revenir au menu principal? (o/n): ").lower()
            if continue_choice != 'o':
                print("\n👋 Merci d'avoir utilisé notre programme de cryptographie. À bientôt!")
                break
                
        except KeyboardInterrupt:
            print("\n\n👋 Programme interrompu. À bientôt!")
            break
        except Exception as e:
            print_error(f"Une erreur inattendue s'est produite: {str(e)}")
            input("\nAppuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main()