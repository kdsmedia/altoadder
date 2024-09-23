from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle, os
from colorama import init, Fore
from time import sleep
import requests  # Moved import here to avoid runtime issues

init()

n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

def banner():
    import random
    b = [
        '░██████╗███████╗████████╗██╗░░░██╗██████╗░',
        '██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗',
        '╚█████╗░█████╗░░░░░██║░░░██║░░░██║██████╔╝',
        '░╚═══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔═══╝░',
        '██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░',
        '╚═════╝░╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░░░'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    print('Contact below address for get premium script')
    print(f'{lg}Version: {w}2.0{lg} | GitHub: {w}@kdsmedia{n}')
    print(f'{lg}Telegram: {w}@sidhanie06{lg} | Instagram: {w}@sidhanie06{n}')

def clr():
    os.system('cls' if os.name == 'nt' else 'clear')

def load_accounts():
    accounts = []
    if not os.path.exists('vars.txt'):
        return accounts
    with open('vars.txt', 'rb') as h:
        while True:
            try:
                accounts.append(pickle.load(h))
            except EOFError:
                break
    return accounts

def save_accounts(accounts):
    with open('vars.txt', 'wb') as k:
        for account in accounts:
            pickle.dump(account, k)

def get_choice():
    while True:
        try:
            choice = int(input('\nEnter your choice: '))
            return choice
        except ValueError:
            print(f'{r}[!] Please enter a valid number.{n}')
            sleep(2)

while True:
    clr()
    banner()
    print(f'{lg}[1] Add new accounts{n}')
    print(f'{lg}[2] Filter all banned accounts{n}')
    print(f'{lg}[3] Delete specific accounts{n}')
    print(f'{lg}[4] Update your Script{n}')
    print(f'{lg}[5] Display All Accounts{n}')
    print(f'{lg}[6] Quit{n}')

    a = get_choice()

    if a == 1:
        new_accs = []
        number_to_add = int(input(f'\n{lg} [~] Enter How Many Accounts You Want To Add: {r}'))
        with open('vars.txt', 'ab') as g:
            for _ in range(number_to_add):
                phone_number = input(f'\n{lg} [~] Enter Phone Number With Country Code: {r}')
                parsed_number = ''.join(phone_number.split())
                pickle.dump([parsed_number], g)
                new_accs.append(parsed_number)
            print(f'\n{lg} [i] Saved all accounts in vars.txt')
            clr()
            print(f'\n{lg} [*] Logging in from new accounts\n')
            for number in new_accs:
                c = TelegramClient(f'sessions/{number}', 6842006, '36b82bda4cb0d9eef87eb4071777725a')
                c.start(number)
                print(f'{lg}[+] Login successful')
                c.disconnect()
            input(f'\n Press enter to goto main menu...')

    elif a == 2:
        accounts = load_accounts()
        if not accounts:
            print(f'{r}[!] There are no accounts! Please add some and retry')
            sleep(3)
        else:
            banned_accs = []
            for account in accounts:
                phone = str(account[0])
                client = TelegramClient(f'sessions/{phone}', 6842006, '36b82bda4cb0d9eef87eb4071777725a')
                client.connect()
                if not client.is_user_authorized():
                    try:
                        client.send_code_request(phone)
                        print(f'{lg}[+] {phone} is not banned{n}')
                    except PhoneNumberBannedError:
                        print(r + phone + ' is banned!' + n)
                        banned_accs.append(account)
            for m in banned_accs:
                accounts.remove(m)
            save_accounts(accounts)
            print(f'{lg}[i] All banned accounts removed{n}' if banned_accs else f'{lg}Congrats! No banned accounts')
            input('\nPress enter to goto main menu...')

    elif a == 3:
        accs = load_accounts()
        print(f'{lg}[i] Choose an account to delete\n')
        for i, acc in enumerate(accs):
            print(f'{lg}[{i}] {acc[0]}{n}')
        index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
        if 0 <= index < len(accs):
            phone = str(accs[index][0])
            session_file = f'sessions/{phone}.session'
            os.remove(session_file) if os.name == 'nt' else os.system(f'rm sessions/{session_file}')
            del accs[index]
            save_accounts(accs)
            print(f'\n{lg}[+] Account Deleted{n}')
            input(f'\nPress enter to goto main menu...')
        else:
            print(f'{r}[!] Invalid choice.{n}')
            sleep(2)

    elif a == 4:
        print(f'\n{lg}[i] Checking for updates...')
        try:
            version = requests.get('https://raw.githubusercontent.com/kdsmedia/altoadder/main/version.txt')
            if float(version.text) > 2.0:
                prompt = input(f'{lg}[~] Update available [Version {version.text}]. Download?[y/n]: {r}')
                if prompt.lower() in {'y', 'yes'}:
                    print(f'{lg}[i] Downloading updates...')
                    os.remove('add.py') if os.name == 'nt' else os.system('rm add.py')
                    os.remove('manager.py') if os.name == 'nt' else os.system('rm manager.py')
                    os.system('curl -l -O https://raw.githubusercontent.com/kdsmedia/altoadder/main/add.py')
                    os.system('curl -l -O https://raw.githubusercontent.com/kdsmedia/altoadder/main/manager.py')
                    print(f'{lg}[*] Updated to version: {version.text}')
                    input('Press enter to exit...')
                    exit()
                else:
                    print(f'{lg}[!] Update aborted.')
                    input('Press enter to goto main menu...')
            else:
                print(f'{lg}[i] Your Telegram-Members-Adder is already up to date')
                input('Press enter to goto main menu...')
        except requests.RequestException:
            print(f'{r} You are not connected to the internet')
            print(f'{r} Please connect to the internet and retry')
            input('Press enter to goto main menu...')

    elif a == 5:
        accs = load_accounts()
        print(f'\n{cy}')
        print(f'\tList Of Phone Numbers Are')
        print('==========================================================')
        for z in accs:
            print(f'\t{z[0]}')
        print('==========================================================')
        input('\nPress enter to goto main menu')

    elif a == 6:
        clr()
        banner()
        exit()
