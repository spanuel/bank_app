import json


class Account:
    def __init__(self, username, balance):
        self.username = username
        self.balance = balance


    @staticmethod
    def load_account(username):
        with open('data/BankData.txt', 'r') as f:
            data = json.load(f)
        account_data = data[0] 
        if username == account_data['username']:
            return Account(username, account_data['balance'])
        else:
            raise ValueError("Account not found")
            
