from modules import prim, second
import os
import sys
import time

# Couleurs ANSI pour terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def clear_screen():
    """Efface l'écran du terminal"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Affiche un en-tête stylisé"""
    clear_screen()
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'MULTICRYPT - CHIFFREMENT SYMÉTRIQUE'.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'=' * 70}{Colors.ENDC}")
    print()

def print_menu(title, options):
    """Affiche un menu avec options numérotées et formatées"""
    print(f"{Colors.BOLD}{title}{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    for idx, option in enumerate(options, 1):
        print(f"{Colors.BOLD}{idx}.{Colors.ENDC} {option}")
    
    print()

def get_user_choice(max_choice):
    """Obtient le choix de l'utilisateur avec validation"""
    while True:
        try:
            choice = input(f"{Colors.YELLOW}➤ Votre choix : {Colors.ENDC}")
            choice = int(choice)
            if 1 <= choice <= max_choice:
                return choice
            print(f"{Colors.RED}❌ Veuillez entrer un nombre entre 1 et {max_choice}.{Colors.ENDC}")
        except ValueError:
            print(f"{Colors.RED}❌ Veuillez entrer un nombre valide.{Colors.ENDC}")

def show_spinner(message, duration=1.5):
    """Affiche une animation de chargement"""
    spinner = ['⣾', '⣽', '⣻', '⢿', '⡿', '⣟', '⣯', '⣷']
    start_time = time.time()
    
    while time.time() - start_time < duration:
        for char in spinner:
            sys.stdout.write(f"\r{Colors.CYAN}{message} {char}{Colors.ENDC}")
            sys.stdout.flush()
            time.sleep(0.1)
    
    sys.stdout.write(f"\r{' ' * (len(message) + 2)}\r")
    sys.stdout.flush()

def print_result(message, success=True):
    """Affiche un message de résultat formaté"""
    prefix = f"{Colors.GREEN}✅" if success else f"{Colors.RED}❌"
    print(f"\n{prefix} {message}{Colors.ENDC}")
    print()

def encrypt_text_file():
    """Interface améliorée pour chiffrer un fichier texte"""
    print_header()
    print(f"{Colors.BOLD}CHIFFREMENT DE FICHIER TEXTE{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    print("Sélectionnez le fichier à chiffrer...")
    show_spinner("Ouverture du sélecteur de fichier", 1)
    
    result = prim.chiffrer_text()
    
    if "✅" in result:
        print_result(result)
    else:
        print_result(result, False)
    
    input(f"{Colors.YELLOW}Appuyez sur Entrée pour continuer...{Colors.ENDC}")

def encrypt_message():
    """Interface améliorée pour chiffrer un message"""
    print_header()
    print(f"{Colors.BOLD}CHIFFREMENT DE MESSAGE{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    message, key = second.demand_msg_key()
    
    print(f"\n{Colors.CYAN}Chiffrement en cours...{Colors.ENDC}")
    show_spinner("Traitement", 1)
    
    result = prim.chiffrer(message, key)
    
    print(f"\n{Colors.GREEN}Message chiffré avec succès !{Colors.ENDC}")
    print(f"\n{Colors.BOLD}Message chiffré :{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    print(result)
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}\n")
    
    input(f"{Colors.YELLOW}Appuyez sur Entrée pour continuer...{Colors.ENDC}")

def encrypt_folder():
    """Interface améliorée pour chiffrer un dossier"""
    print_header()
    print(f"{Colors.BOLD}CHIFFREMENT DE DOSSIER{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    print("Suivez les instructions pour sélectionner le dossier...")
    result = prim.chiffrer_dossier_avec_dialogue()
    
    if "✅" in result:
        print_result(result)
    else:
        print_result(result, False)
    
    input(f"{Colors.YELLOW}Appuyez sur Entrée pour continuer...{Colors.ENDC}")

def decrypt_text_file():
    """Interface améliorée pour déchiffrer un fichier texte"""
    print_header()
    print(f"{Colors.BOLD}DÉCHIFFREMENT DE FICHIER TEXTE{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    print("Sélectionnez le fichier à déchiffrer...")
    show_spinner("Ouverture du sélecteur de fichier", 1)
    
    result = prim.dechiffrer_text()
    
    if "✅" in result:
        print_result(result)
    else:
        print_result(result, False)
    
    input(f"{Colors.YELLOW}Appuyez sur Entrée pour continuer...{Colors.ENDC}")

def decrypt_message():
    """Interface améliorée pour déchiffrer un message"""
    print_header()
    print(f"{Colors.BOLD}DÉCHIFFREMENT DE MESSAGE{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    message_chiffre, key = second.demand_msg_key()
    
    print(f"\n{Colors.CYAN}Déchiffrement en cours...{Colors.ENDC}")
    show_spinner("Traitement", 1)
    
    result = prim.dechiffrer(message_chiffre, key)
    
    print(f"\n{Colors.GREEN}Message déchiffré avec succès !{Colors.ENDC}")
    print(f"\n{Colors.BOLD}Message déchiffré :{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    print(result)
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}\n")
    
    input(f"{Colors.YELLOW}Appuyez sur Entrée pour continuer...{Colors.ENDC}")

def decrypt_folder():
    """Interface améliorée pour déchiffrer un dossier"""
    print_header()
    print(f"{Colors.BOLD}DÉCHIFFREMENT DE DOSSIER{Colors.ENDC}")
    print(f"{Colors.CYAN}{'─' * 50}{Colors.ENDC}")
    
    print("Suivez les instructions pour sélectionner le dossier chiffré...")
    result = prim.dechiffrer_dossier_avec_dialogue()
    
    if "✅" in result:
        print_result(result)
    else:
        print_result(result, False)
    
    input(f"{Colors.YELLOW}Appuyez sur Entrée pour continuer...{Colors.ENDC}")

def main():
    # Clear screen une seule fois au démarrage
    clear_screen()
    
    while True:
        print(f"\n{Colors.BOLD}{Colors.YELLOW}🔐 BIENVENUE DANS MULTICRYPT 🔑{Colors.ENDC}")
        print(f"{Colors.CYAN}Le programme de chiffrement symétrique sécurisé{Colors.ENDC}\n")
        
        print_menu("QUE SOUHAITEZ-VOUS FAIRE ?", [
            f"{Colors.GREEN}Chiffrer un fichier, message ou dossier{Colors.ENDC}",
            f"{Colors.BLUE}Déchiffrer un fichier, message ou dossier{Colors.ENDC}",
            f"{Colors.RED}Quitter le programme{Colors.ENDC}"
        ])
        
        choice = get_user_choice(3)
        
        if choice == 1:
            print(f"\n{Colors.CYAN}{'=' * 50}{Colors.ENDC}")
            print_menu("QUE VOULEZ-VOUS CHIFFRER ?", [
                "Fichier .txt",
                "Message dans la console",
                "Un dossier"
            ])
            
            sub_choice = get_user_choice(3)
            
            if sub_choice == 1:
                encrypt_text_file()
            elif sub_choice == 2:
                encrypt_message()
            elif sub_choice == 3:
                encrypt_folder()
            
        elif choice == 2:
            print(f"\n{Colors.CYAN}{'=' * 50}{Colors.ENDC}")
            print_menu("QUE VOULEZ-VOUS DÉCHIFFRER ?", [
                "Fichier .txt",
                "Message dans la console",
                "Un dossier"
            ])
            
            sub_choice = get_user_choice(3)
            
            if sub_choice == 1:
                decrypt_text_file()
            elif sub_choice == 2:
                decrypt_message()
            elif sub_choice == 3:
                decrypt_folder()
            
        elif choice == 3:
            print(f"\n{Colors.GREEN}Merci d'avoir utilisé MultiCrypt !{Colors.ENDC}")
            print(f"{Colors.YELLOW}À bientôt !{Colors.ENDC}\n")
            break
        
        print(f"\n{Colors.CYAN}{'=' * 50}{Colors.ENDC}")

if __name__ == "__main__":
    main()