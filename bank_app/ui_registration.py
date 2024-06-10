import tkinter as tk
import random
from tkinter import messagebox
from bank_app.account import Account
from bank_app.authentication import register_user
from bank_app.password_generator import generate_password

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

        self.generate_password_var = tk.BooleanVar()
        self.generate_password_checkbox = tk.Checkbutton(self, text="Generate Random Password", variable=self.generate_password_var, command=self.toggle_password_entry)
        self.generate_password_checkbox.pack()

        self.register_button = tk.Button(self, text="Register", command=self.register)
        self.register_button.pack()

    def toggle_password_entry(self):
        if self.generate_password_var.get():
            self.password_entry.configure(state='disabled')
        else:
            self.password_entry.configure(state='normal')

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.generate_password_var.get():
            password = generate_password()

        try:
            account_number = self.generate_account_number()
            register_user(username, password, account_number)
            self.show_registration_success(username, account_number, password)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

        return account_number

    def generate_account_number(self):
        return str(random.randint(100, 999)) + ''.join(random.choices('0123456789', k=7))

    def show_registration_success(self, username, account_number, password):
        details = f"Account Number: {account_number}\nUsername: {username}\n"
        if self.generate_password_var.get():
            details += f"Password: {password}\n"
        details += "Would you like to fund your account now?"
        
        if messagebox.askyesno("Registration Successful", details):
            return True, account_number
        else:
            self.destroy()
            from bank_app.ui_login import LoginWindow
            LoginWindow().mainloop()
            return False, None

class DepositWindow(tk.Tk):
    def __init__(self,account_number):
        super().__init__()
        self.title("Deposit")
        self.geometry("300x150")
        self.eval('tk::PlaceWindow . center')
        self.account_number = account_number
        self.create_widgets()

    def create_widgets(self):
        self.amount_label = tk.Label(self, text="Enter deposit amount: ")
        self.amount_label.pack()
        self.amount_entry  = tk.Entry(self)
        self.amount_entry.pack()

        self.confirm_button = tk.Button(self, text="Confirm")

    def confirm_deposit(self):
        amount = float(self.amount_entry)
        try:
            account = Account(self.account_number)
            account.deposit(amount)
            messagebox.showinfo("Deposit Successful", "Account funded successfully.")
            self.destroy()
            from bank_app.ui_login import LoginWindow
            LoginWindow().mainloop()
        except ValueError as e:
               messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    registration_window = RegistrationWindow()
    registration_window.mainloop()

    if registration_window.show_registration_success:
        success, account_number = registration_window.show_registration_success
        
        if success: 
            DepositWindow(account_number).mainloop()
