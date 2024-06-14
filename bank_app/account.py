import json
from datetime import datetime

class Account:
    def __init__(self, username,account_number):
        self.username = username
        self.balance = 0.0
        self.account_number = account_number
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
            account_number = users[username]
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
            users[self.account_number] = user_data
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

    def transfer(self, recipient_username, amount):
        recipient = Account(recipient_username)
        self.withdraw(amount)
        recipient.deposit(amount)
        self.log_transaction("Transfer", amount, recipient_username)
        recipient.log_transaction("Receive", amount, self.username)

    def log_transaction(self, transaction_type, amount, recipient_username=None):
        with open('data/TransactionLog.txt', 'a') as file:
            if recipient_username:
                file.write(f"{self.username} - {datetime.now()} - {transaction_type} - R {amount} - R {self.balance} - To/From {recipient_username}\n")
            else:
                file.write(f"{self.username} - {datetime.now()} -  {transaction_type} - R {amount} - R {self.balance}\n")

    def get_transaction_history(self, from_date=None, to_date=None):
        transactions = []
        try:
            with open('data/TransactionLog.txt', 'r') as file:
                for line in file:
                    transaction_details = line.strip().split(' - ')
                    if len(transaction_details) >= 5 and str(self.username) in transaction_details[0]:
                        transaction_date_str = f"{transaction_details[1]}"
                        transaction_date = datetime.strptime(transaction_date_str, "%Y-%m-%d %H:%M:%S.%f")
                        transaction = None
                        if (from_date is None or transaction_date >= from_date) and (to_date is None or transaction_date <= to_date):
                             transaction = {
                            'date': transaction_date,
                            'description': transaction_details[2],
                            'amount': float(transaction_details[3].split(' ')[1]),
                            'balance': float(transaction_details[4].split(' ')[1])                           
                             }
                        transactions.append(transaction)
                        print(transactions)
        except FileNotFoundError:
            pass
        return transactions

    def get_bank_statement(self,from_date=None, to_date=None):
        return self.get_transaction_history(from_date, to_date)



