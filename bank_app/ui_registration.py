import random
import string
import tkinter as tk
from tkinter import messagebox
from bank_app.account import Account
from bank_app.authentication import register_user

class RegistrationWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Register")
        self.geometry("300x250")
        self.eval('tk::PlaceWindow . center')
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.password_label = tk.Label(self, text="Password")
        self.password_label.pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        self.generate_password_var = tk.IntVar()
        self.generate_password_check = tk.Checkbutton(self, text="Generate Random Password", variable=self.generate_password_var, command=self.toggle_password_entry)
        self.generate_password_check.pack()

        self.register_button = tk.Button(self, text="Register", command=self.register)
        self.register_button.pack()

    def toggle_password_entry(self):
        if self.generate_password_var.get():
            self.password_entry.config(state=tk.DISABLED)
            generated_password = self.generate_password()
            self.password_entry.insert(0, generated_password)
        else:
            self.password_entry.config(state=tk.NORMAL)
            self.password_entry.delete(0, tk.END)

    @staticmethod
    def generate_password(length=12):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(random.choice(characters) for _ in range(length))
        return password

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        account_number = self.generate_account_number()

        if register_user(username, password, account_number):
            self.show_registration_success(username, account_number, password if self.generate_password_var.get() else None)
        else:
            messagebox.showerror("Error", "Username already exists")

    def generate_account_number(self):
        prefix = ''.join(random.choice(string.digits) for _ in range(3))
        suffix = ''.join(random.choice(string.digits) for _ in range(7))
        return prefix + suffix

    def show_registration_success(self, username, account_number, password):
        message = f"Registration Successful!\n\nUsername: {username}\nAccount Number: {account_number}"
        if password:
            message += f"\nGenerated Password: {password}"
        message += "\n\nWould you like to fund your account now?"

        if messagebox.askyesno("Success", message):
            self.destroy()
            DepositWindow(username).mainloop()
        else:
            self.destroy()
            from bank_app.ui_login import LoginWindow
            LoginWindow().mainloop()

class DepositWindow(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.title("Deposit Funds")
        self.geometry("300x150")
        self.eval('tk::PlaceWindow . center')
        self.create_widgets()

    def create_widgets(self):
        self.amount_label = tk.Label(self, text="Deposit Amount")
        self.amount_label.pack()
        self.amount_entry = tk.Entry(self)
        self.amount_entry.pack()

        self.deposit_button = tk.Button(self, text="Deposit", command=self.deposit)
        self.deposit_button.pack()

    def deposit(self):
        amount = self.amount_entry.get()
        if amount.isdigit() and int(amount) > 0:
            account = Account(self.username)
            account.deposit(float(amount))
            messagebox.showinfo("Success", f"Deposited R{amount} successfully!")
            self.destroy()
            from bank_app.ui_login import LoginWindow
            LoginWindow().mainloop()
        else:
            messagebox.showerror("Error", "Please enter a valid amount")

if __name__ == "__main__":
    registration_window = RegistrationWindow()
    registration_window.mainloop()
