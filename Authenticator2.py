import random
import string
import time

def read_user_credentials():
    # Read user credentials from the text file and return as a dictionary
    user_credentials = {}
    try:
        with open("accounts.txt", "r") as file:
            for line in file:
                parts = line.strip().split()
                if len(parts) == 2:
                    username, password = parts
                    user_credentials[username] = password
                else:
                    print(f"Skipping invalid line: {line}")
    except FileNotFoundError:
        print("User credentials file not found. Creating a new one...")
        open("accounts.txt", "w").close()
    return user_credentials

def write_user_credentials(user_credentials):
    # Write user credentials from the dictionary to the text file
    with open("accounts.txt", "w") as file:
        for username, password in user_credentials.items():
            file.write(f"{username} {password}\n")

def register():
    # Function for user registration
    print("Register:")
    username = input("Enter your desired username: ")
    if username in user_credentials:
        print("Username already exists. Please choose another one.")
        return
    choice = input("Would you like to enter your own password or generate one? (A/B): ").upper()
    if choice == "A":
        password = input("Enter your desired password: ")
    elif choice == "B":
        password = generate_password()
    else:
        print("Invalid choice. Please try again.")
        return
    user_credentials[username] = password
    write_user_credentials(user_credentials)
    print("Registration successful!")
    time.sleep(2)  # Adding a delay of 2 seconds

def login():
    # Function for user login
    print("Login:")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    if username not in user_credentials or user_credentials[username] != password:
        print("Invalid username or password. Please try again.")
        return False, None  # Returning False and None to indicate unsuccessful login
    print("Login successful!")
    return True, username  # Returning True and the username to indicate successful login

def generate_password():
    # Function to generate a password
    print("Generate Password:")
    default_length = 10
    length = input(f"Enter the length of the password (default is {default_length}): ")
    if length:
        length = int(length)
    else:
        length = default_length

    include_numbers = input("Include numbers? (Yes/No): ").lower() == "yes"
    include_symbols = input("Include symbols? (Yes/No): ").lower() == "yes"
    include_lowercase = input("Include lowercase letters? (Yes/No): ").lower() == "yes"
    include_uppercase = input("Include uppercase letters? (Yes/No): ").lower() == "yes"

    if not (include_numbers or include_symbols or include_lowercase or include_uppercase):
        print("At least one character type must be included.")
        return ""

    password_characters = ""
    if include_numbers:
        password_characters += string.digits
    if include_symbols:
        password_characters += string.punctuation
    if include_lowercase:
        password_characters += string.ascii_lowercase
    if include_uppercase:
        password_characters += string.ascii_uppercase

    password = ''.join(random.choice(password_characters) for _ in range(length))
    return password

def view_accounts():
    # Function to view user accounts (for admin)
    print("User Accounts:")
    for username, password in user_credentials.items():
        print(f"Username: {username}, Password: {password}")

def change_password(username):
    # Function to change the password
    print("Change Password:")
    choice = input("Would you like to enter your own password or generate one? (A/B): ").upper()
    if choice == "A":
        new_password = input("Enter your new password: ")
    elif choice == "B":
        new_password = generate_password()
    else:
        print("Invalid choice. Password remains unchanged.")
        return

    user_credentials[username] = new_password
    write_user_credentials(user_credentials)
    print("Password changed successfully!")
    time.sleep(2)  # Adding a delay of 2 seconds

# Read existing user credentials
user_credentials = read_user_credentials()

# Main menu
while True:
    print("\nWelcome to User Authentication System")
    print("A. Register")
    print("B. Login")
    print("C. Exit")
    
    choice = input("Select an option: ").upper()

    if choice == "A":
        register()
    elif choice == "B":
        logged_in, username = login()
        if logged_in:
            if username.lower() == "admin":
                print("Welcome Admin!")
                while True:
                    print("\nAdmin Menu:")
                    print("1. View Accounts")
                    print("2. Logout")
                    sub_choice = input("Select an option: ").lower()
                    if sub_choice == "1":
                        view_accounts()
                    elif sub_choice == "2":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please select again.")
            else:
                print("Welcome to GELOS!")
                while True:
                    print("\nLogged In Menu:")
                    print("1. Change Password")
                    print("2. Logout")
                    sub_choice = input("Select an option: ").lower()
                    if sub_choice == "1":
                        change_password(username)
                    elif sub_choice == "2":
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Please select again.")
    elif choice == "C":
        print("Exiting...")
        time.sleep(2)  # Adding a delay of 2 seconds before exiting
        break
    else:
        print("Invalid choice. Please select again.")

