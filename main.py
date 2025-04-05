from utils.master_key import setup_master_key, get_derived_key, derive_key, get_salt
from utils.database import load_data, save_data, encrypt_data, decrypt_data, reset_passwords
from cryptography.fernet import Fernet
import os
import getpass  # Make sure getpass is imported

# Function to display developer info in yellow
def display_developer_info():
    print("\n\033[33m--------------------------------------------")
    print("Developer: techbysakh")
    print("--------------------------------------------\033[0m")

# Function to display options in the same color
def print_options():
    print("\033[32mOptions:")
    print("1. Add new password")
    print("2. View saved passwords")
    print("3. Delete a saved password")
    print("4. Reset options")
    print("5. Exit\033[0m")

# Define the function to input the master password securely
def get_password_input():
    password = getpass.getpass("Enter master password: ")
    return password

def main():
    display_developer_info()  # Display developer info when the program starts

    if not os.path.exists("salt.bin"):  # This check is done to see if it's first-time setup
        key, _ = setup_master_key()  # Getting the key and password during setup
        fernet = Fernet(key)  # Store key in Fernet for encryption
    else:
        # Fetch the stored salt
        salt = get_salt()
        
        # Check if the derived key exists
        stored_key = get_derived_key()
        if stored_key is None:
            print("❌ Master key not found, setup required.")
            return
        
        # Prompt the user to enter the master password
        print("\n🔐 Please enter your master password to continue:")
        entered_password = get_password_input()
        
        # Derive the key from the entered password using the salt
        derived_key = derive_key(entered_password, salt)

        # Compare the derived key with the stored key
        if derived_key != stored_key:
            print("❌ Incorrect password. Exiting...")
            return
        
        fernet = Fernet(stored_key)  # Use the stored key for Fernet encryption

    # Load existing data
    data = load_data()

    try:
        passwords = decrypt_data(data, fernet)
    except Exception as e:
        print(f"❌ Error decrypting data: {e}")
        return

    while True:
        print_options()  # Display the options in uniform color
        choice = input("Choose an option: ")

        if choice == "1":
            site = input("Enter site name: ")
            username = input("Enter username: ")
            pw = input("Enter password: ")
            if site not in passwords:
                passwords[site] = {}
            passwords[site][username] = pw
            encrypted = encrypt_data(passwords, fernet)
            save_data(encrypted)
            print("✅ Password saved.")

        elif choice == "2":
            if not passwords:
                print("📭 No passwords saved.")
            else:
                for site, user_pass in passwords.items():
                    print(f"\nWebsite: {site}")
                    for user, pw in user_pass.items():
                        print(f"  {user}: {pw}")

        elif choice == "3":
            if not passwords:
                print("📭 No passwords saved.")
            else:
                print("\nChoose the website to delete a password from:")
                for idx, site in enumerate(passwords.keys(), 1):
                    print(f"{idx}. {site}")
                site_choice = int(input("Enter site number to delete: "))
                site = list(passwords.keys())[site_choice - 1]

                print("\nChoose the username to delete:")
                for idx, username in enumerate(passwords[site].keys(), 1):
                    print(f"{idx}. {username}")
                user_choice = int(input("Enter username number to delete: "))
                username = list(passwords[site].keys())[user_choice - 1]

                del passwords[site][username]
                if not passwords[site]:
                    del passwords[site]

                encrypted = encrypt_data(passwords, fernet)
                save_data(encrypted)
                print("🗑️ Password deleted.")

        elif choice == "4":
            print("\nReset Options:")
            print("1. Delete all saved passwords and websites")
            print("2. Change master key")
            sub = input("Choose an option: ")
            if sub == "1":
                reset_passwords()
                passwords = {}
                print("🧹 All passwords deleted.")
            elif sub == "2":
                key, _ = setup_master_key()
                fernet = Fernet(key)
                encrypted = encrypt_data(passwords, fernet)
                save_data(encrypted)

        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("❗ Invalid choice.")

if __name__ == "__main__":
    main()
