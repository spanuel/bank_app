import json
import bcrypt
import os

def initialize_bank_data():
    if not os.path.exists('data/BankData.txt'):
        with open('data/BankData.txt', 'w') as file:
            json.dump({}, file)  

def read_bank_data():
    if not os.path.exists('data/BankData.txt'):
        return {}

    with open('data/BankData.txt', 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = {} 
    return data

def authenticate_user(username, password):
    users = read_bank_data()
    if username in users and bcrypt.checkpw(password.encode('utf-8'), users[username]['password'].encode('utf-8')):
        return True
    return False

def register_user(username, password, account_number):
    users = read_bank_data()
    if username in users:
        return False 

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = {
        "username": username,
        "password": hashed_password,
        "account_number": account_number,
        "balance": 0
    }
    users[username] = new_user  

    with open('data/BankData.txt', 'w') as file:
        json.dump(users, file)
    
    return True

def reset_password(username, new_password):
    users = read_bank_data()
    if username not in users:
        return False 

    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    users[username]['password'] = hashed_password  

    with open('data/BankData.txt', 'w') as file:
        json.dump(users, file)

    return True


initialize_bank_data()
