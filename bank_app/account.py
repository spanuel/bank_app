import json
from datetime import datetime

class Account:
    def __init__(self, username):
        self.username = username
        self.balance = 0.0
        self.load_account()  

    def load_account(self):
        try:
            self.balance = Account.load_account_data(self.username)  
        except ValueError as e:
            print(f"Error loading account: {e}")

    @staticmethod
    def load_account_data(username):
        users = Account.read_bank_data()
        print(f"Checking username: {username}")
        if username in users:
            user_data = users[username]
            balance = user_data.get('balance', 0.0)
            return balance
        else:
            raise ValueError("Account not found")

    @staticmethod
    def read_bank_data():
        try:
            with open('data/BankData.txt', 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}  
        except json.JSONDecodeError:
            data = {} 
        return data

    @staticmethod
    def write_bank_data(data):
        with open('data/BankData.txt', 'w') as file:
            json.dump(data, file)

    def update_account(self):
        users = self.read_bank_data()
        if self.username in users:
            user_data = users[self.username]
            user_data['balance'] = self.balance 
            users[self.username] = user_data
        else:
            raise ValueError("Account not found when updating")
        self.write_bank_data(users)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount
        self.update_account()
        self.log_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self.update_account()
        self.log_transaction("Withdraw", amount)

    def log_transaction(self, transaction_type, amount):
        with open('data/TransactionLog.txt', 'a') as file:
            file.write(f"{datetime.now()} - {self.username} - {transaction_type} - R {amount} - R {self.balance}\n")



