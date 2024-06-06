import json
import bcrypt
import os

def initialize_bank_data():
    if not os.path.exists('data/BankData.txt'):
        with open('data/BankData.txt', 'w') as file:
            json.dump([], file)

def read_bank_data():
    if not os.path.exists('data/BankData.txt'):
        return []

    with open('data/BankData.txt', 'r') as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError:
            data = []
    return data

def authenticate_user(username, password):
    users = read_bank_data()
    for user_data in users:
        if user_data['username'] == username and bcrypt.checkpw(password.encode('utf-8'), user_data['password'].encode('utf-8')):
            return True
    return False

def register_user(username, password, balance):
    users = read_bank_data()
    for user_data in users:
        if user_data['username'] == username:
            return False  

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    new_user = {
        "username": username,
        "password": hashed_password,
        "balance": balance
    }
    users.append(new_user)

    with open('data/BankData.txt', 'w') as file:
        json.dump(users, file)
    
    return True

def reset_password(username, new_password):
    users = []
    user_found = False

    if not os.path.exists('data/BankData.txt'):
        return False

    with open('data/BankData.txt', 'r') as file:
        for line in file:
            user_data = line.strip().split(',')
            if user_data[0] == username:
                user_data[1] = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user_found = True
            users.append(user_data)

    if not user_found:
        return False

    with open('data/BankData.txt', 'w') as file:
        for user_data in users:
            file.write(','.join(user_data) + '\n')

    return True