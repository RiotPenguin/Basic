from cryptography.fernet import Fernet
import json
import os

class PasswordManager:
    def __init__(self, key_file='~/.password_manager/key.key', password_file='~/.password_manager/passwords.json'):
        self.key_file = os.path.expanduser(key_file)
        self.password_file = os.path.expanduser(password_file)
        self.key = self.load_key()
        self.cipher = Fernet(self.key)
        self.passwords = self.load_passwords()

    def load_key(self):
        if not os.path.exists(self.key_file):
            os.makedirs(os.path.dirname(self.key_file), exist_ok=True)
            key = Fernet.generate_key()
            with open(self.key_file, 'wb') as key_file:
                key_file.write(key)
        else:
            with open(self.key_file, 'rb') as key_file:
                key = key_file.read()
        return key

    def load_passwords(self):
        if os.path.exists(self.password_file):
            with open(self.password_file, 'r') as password_file:
                passwords = json.load(password_file)
                for account, enc_password in passwords.items():
                    passwords[account] = self.cipher.decrypt(enc_password.encode()).decode()
        else:
            passwords = {}
        return passwords

    def save_passwords(self):
        encrypted_passwords = {account: self.cipher.encrypt(password.encode()).decode()
                               for account, password in self.passwords.items()}
        os.makedirs(os.path.dirname(self.password_file), exist_ok=True)
        with open(self.password_file, 'w') as password_file:
            json.dump(encrypted_passwords, password_file)

    def add_password(self, account, password):
        self.passwords[account] = password
        self.save_passwords()

    def get_password(self, account):
        return self.passwords.get(account)

    def delete_password(self, account):
        if account in self.passwords:
            del self.passwords[account]
            self.save_passwords()

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Password Manager')
    parser.add_argument('action', choices=['add', 'get', 'delete'], help='Action to perform')
    parser.add_argument('account', help='Account name')
    parser.add
