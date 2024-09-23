'''
================ALTOMEDIA=====================
Telegram members adding script
Coded by a kid - github.com/kdsmedia
Apologies if anything in the code is dumb :)
Copy with credits
************************************************
'''

# Import necessary libraries
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerChannel
from telethon.errors.rpcerrorlist import (
    PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError,
    ChatAdminRequiredError, ChatWriteForbiddenError, UserBannedInChannelError,
    UserAlreadyParticipantError, FloodWaitError
)
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest
import sys, os, pickle, time, random
from colorama import init, Fore

# Initialize colorama for colored terminal output
init()

# Color settings
r = Fore.RED
lg = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
grey = '\033[97m'
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]

# Define some common message formats
info = f'{lg}[{w}i{lg}]{rs}'
error = f'{lg}[{r}!{lg}]{rs}'
success = f'{w}[{lg}*{w}]{rs}'
INPUT = f'{lg}[{cy}~{lg}]{rs}'
plus = f'{w}[{lg}+{w}]{rs}'
minus = f'{w}[{lg}-{w}]{rs}'

# Banner function
def banner():
    # Display a fancy logo
    logo = [
        '░█████╗░██████╗░██████╗░███████╗██████╗░',
        '██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗',
        '███████║██║░░██║██║░░██║█████╗░░██████╔╝',
        '██╔══██║██║░░██║██║░░██║██╔══╝░░██╔══██╗',
        '██║░░██║██████╔╝██████╔╝███████╗██║░░██║',
        '╚═╝░░╚═╝╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝'
    ]
    for line in logo:
        print(f'{random.choice(colors)}{line}{rs}')
    print(f'{lg}Version: {w}2.0{lg} | GitHub: {w}@kdsmedia{rs}')
    print(f'{lg}Telegram: {w}@DearSaif{lg} | Instagram: {w}@sidhanie06{rs}')

# Function to clear screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Load accounts from 'vars.txt'
def load_accounts():
    accounts = []
    with open('vars.txt', 'rb') as f:
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
    return accounts

# Check for banned accounts
def check_banned_accounts(accounts):
    print(f'\n{info}{lg} Checking for banned accounts...')
    banned = []
    for account in accounts:
        phone = account[0]
        print(f'{plus}{grey} Checking {lg}{phone}')
        client = TelegramClient(f'sessions/{phone}', 6842006, '36b82bda4cb0d9eef87eb4071777725a')
        client.connect()
        if not client.is_user_authorized():
            try:
                client.send_code_request(phone)
            except PhoneNumberBannedError:
                print(f'{error} {phone} {r}is banned!{rs}')
                banned.append(account)
        client.disconnect()
    return [acc for acc in accounts if acc not in banned]

# Log the current scraping status
def log_status(scraped_group, index):
    with open('status.dat', 'wb') as f:
        pickle.dump([scraped_group, int(index)], f)
    print(f'{info}{lg} Session stored in {w}status.dat{lg}')

# Exit the script gracefully
def exit_program():
    input(f'\n{cy} Press enter to exit...')
    clear_screen()
    banner()
    sys.exit()

# Main script execution starts here
clear_screen()
banner()

# Load accounts and check for banned ones
accounts = load_accounts()
accounts = check_banned_accounts(accounts)
print(f'{info} Sessions created!')

# Ask for group details
try:
    with open('status.dat', 'rb') as f:
        status = pickle.load(f)
        resume = input(f'{INPUT}{cy} Resume scraping members from {status[0]}? [y/n]: {r}')
        if 'y' in resume:
            scraped_group = status[0]
            start_index = int(status[1])
        else:
            os.remove('status.dat')
            scraped_group = input(f'{INPUT}{cy} Enter public/private group URL to scrape members: {r}')
            start_index = 0
except FileNotFoundError:
    scraped_group = input(f'{INPUT}{cy} Enter public/private group URL to scrape members: {r}')
    start_index = 0

# Continue with the logic for joining groups, scraping, and adding members...
