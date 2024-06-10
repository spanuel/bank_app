import json
from datetime import datetime

class Account:
    def __init__(self, username):
        self.username = username
        self.balance = 0.0
        self.load_account()

    def load_account(self):
        self.balance = Account.load_account_data(self.username)

    @staticmethod
    def load_account_data(username):
        users = Account.read_bank_data()
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
        return data

    @staticmethod
    def write_bank_data(data):
        with open('data/BankData.txt', 'w') as file:
            json.dump(data, file)

    def update_account(self):
        users = self.read_bank_data()
        users[self.username] = {'balance': self.balance}
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
            file.write(f"{datetime.now()} - {transaction_type} - {amount} - {self.balance}\n")

