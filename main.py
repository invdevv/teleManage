#!/bin/python3

import json
import subprocess
import getpass
import argparse

parser = argparse.ArgumentParser(
    prog="tg",
    description="Telegram Account managment tool"
)

parser.add_argument("ids", nargs='*', help="Account IDs or Names")

parser.add_argument("-l", "--list", action="store_true", help="Show list of all accounts") #action="store_true" for create flag

parser.add_argument("-a", "--add", type=str, help="Add new account (Enter acc Name)")


args = parser.parse_args()

# CONSTANTS
JSON_PATH = f"/home/{getpass.getuser()}/Documents/TelegramAccs/script/accs.json"
TELEGRAM_FOLDER_PATH = f"/home/{getpass.getuser()}/Documents/TelegramAccs/accounts"
RUN_TELEGRAM_COMMAND = f"cd {TELEGRAM_FOLDER_PATH}/Telegram{"{id}"} && ./Telegram &>/dev/null &"


def get_accs_data():
    with open(JSON_PATH) as f:
        data = json.load(f)

    return data

def add_account(name: str):
    accounts = get_accs_data()
    accounts[str(len(accounts) + 1)] = name

    new_acc_path = f"{TELEGRAM_FOLDER_PATH}/Telegram{len(accounts)}"

    subprocess.run(f"mkdir {new_acc_path}", shell=True)
    subprocess.run(f"mkdir {new_acc_path}/TelegramForcePortable", shell=True)

    subprocess.run(f"cp {TELEGRAM_FOLDER_PATH}/Telegram1/Telegram {new_acc_path}", shell=True)
    subprocess.run(f"cp {TELEGRAM_FOLDER_PATH}/Telegram1/Updater {new_acc_path}", shell=True)

    with open(JSON_PATH, "w") as f:
        json.dump(accounts, f)

    return len(accounts)

    



def get_id_by_pattern(pattern: str):
    accounts: dict = get_accs_data()

    ids = []
    names = []

    for id, name in accounts.items():
        if pattern.lower() in name.lower():
            ids.append(int(id))
            names.append(name)

    return ids, names

def edit_account_name(id: int, name: str):
    accounts = get_accs_data()
    accounts[str(id)] = name

    with open(JSON_PATH, "w") as f:
        json.dump(accounts, f)

def run_clients(ids: list[int]):
    for id in ids:
        subprocess.run(RUN_TELEGRAM_COMMAND.format(id = id), shell=True)


def main(args):
    if args.ids:
        to_run = []
        for id in args.ids:
            if (id.isdigit()):
                to_run.append(int(id))

            else:
                ids, _ = get_id_by_pattern(id)
                to_run.extend(ids)
        
        run_clients(to_run)

        accounts_data = get_accs_data()
        print(f"Started Clients: {" ".join([accounts_data[str(id)] for id in to_run])}")

    elif args.list:
        accounts: dict = get_accs_data()

        for id, name in accounts.items():
            print(f"{id} - {name}")
    
    elif args.add:
        id = add_account(args.add)

        run_clients([id])
        
        

if __name__ == "__main__":
    main(args)
