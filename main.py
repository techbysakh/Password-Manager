# main.py
from utils.master_key import setup_master_key, get_derived_key
from utils.database import load_data, save_data, encrypt_data, decrypt_data, reset_passwords
from cryptography.fernet import Fernet
from colorama import Fore, Style, init

import os

# Initialize colorama
init(autoreset=True)

def main():
    if not os.path.exists("salt.bin"):
        key, _ = setup_master_key()  # Getting the key and password during setup
    else:
        key, _ = get_derived_key()

    fernet = Fernet(key)
    data = load_data()

    try:
        passwords = decrypt_data(data, fernet)
    except Exception:
        print(Fore.RED + "❌ Incorrect password. Exiting...")
        return

    while True:
        print(Fore.CYAN + "\nOptions:")
        print(Fore.GREEN + "1. Add new password")
        print(Fore.YELLOW + "2. View saved passwords")
        print(Fore.RED + "3. Delete a saved password")
        print(Fore.MAGENTA + "4. Reset options")
        print(Fore.BLUE + "5. Exit")
        choice = input(Fore.WHITE + "Choose an option: ")

        if choice == "1":
            site = input(Fore.WHITE + "Enter site name: ")
            username = input(Fore.WHITE + "Enter username: ")
            pw = input(Fore.WHITE + "Enter password: ")

            if site not in passwords:
                passwords[site] = {}

            passwords[site][username] = pw

            encrypted = encrypt_data(passwords, fernet)
            save_data(encrypted)
            print(Fore.GREEN + "✅ Password saved.")

        elif choice == "2":
            if not passwords:
                print(Fore.YELLOW + "📭 No passwords saved.")
            else:
                for site, accounts in passwords.items():
                    print(Fore.CYAN + f"\nWebsite: {site}")
                    for username, password in accounts.items():
                        print(Fore.YELLOW + f"  {username}: {password}")

        elif choice == "3":
            if not passwords:
                print(Fore.YELLOW + "📭 No passwords saved to delete.")
            else:
                print(Fore.CYAN + "\nList of saved passwords:")
                # Show list of websites and usernames
                sites_and_usernames = []
                for site, accounts in passwords.items():
                    for username in accounts:
                        sites_and_usernames.append(f"{site} - {username}")
                
                for idx, site_user in enumerate(sites_and_usernames, 1):
                    print(Fore.YELLOW + f"{idx}. {site_user}")

                # Prompt the user to choose an item to delete
                try:
                    delete_choice = int(input(Fore.WHITE + "Enter the number of the password you want to delete: "))
                    if delete_choice < 1 or delete_choice > len(sites_and_usernames):
                        print(Fore.RED + "⚠️ Invalid choice.")
                        continue
                except ValueError:
                    print(Fore.RED + "⚠️ Invalid input. Please enter a number.")
                    continue

                # Get the selected site and username
                selected = sites_and_usernames[delete_choice - 1]
                site, username = selected.split(" - ")

                # Delete the selected password
                if site in passwords and username in passwords[site]:
                    del passwords[site][username]
                    encrypted = encrypt_data(passwords, fernet)
                    save_data(encrypted)
                    print(Fore.RED + "🗑️ Password deleted.")
                else:
                    print(Fore.RED + "⚠️ Site or username not found.")

        elif choice == "4":
            print(Fore.MAGENTA + "\nReset Options:")
            print(Fore.GREEN + "1. Delete all saved passwords and websites")
            print(Fore.YELLOW + "2. Change master key")
            sub = input(Fore.WHITE + "Choose an option: ")
            if sub == "1":
                reset_passwords()
                passwords = {}
                print(Fore.MAGENTA + "🧹 All passwords deleted.")
            elif sub == "2":
                key, _ = setup_master_key()
                fernet = Fernet(key)
                encrypted = encrypt_data(passwords, fernet)
                save_data(encrypted)

        elif choice == "5":
            print(Fore.CYAN + "👋 Goodbye!")
            break
        else:
            print(Fore.RED + "❗ Invalid choice.")

if __name__ == "__main__":
    main()
