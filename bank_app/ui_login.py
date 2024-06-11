import tkinter as tk
from tkinter import messagebox
from bank_app.authentication import authenticate_user, reset_password
from bank_app.ui_account_management import AccountManagementWindow
from bank_app.ui_registration import RegistrationWindow
from bank_app.account import Account

class LoginWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("300x150")
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

        self.login_button = tk.Button(self, text="Login", command=self.validate_login)
        self.login_button.pack()

        self.forgot_password_button = tk.Button(self, text="Forgot Password?", command=self.forgot_password, borderwidth=0, cursor="hand2", underline=True)
        self.forgot_password_button.pack()

    def validate_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if authenticate_user(username, password):
            self.destroy()
            account = Account(username)
            AccountManagementWindow(account).mainloop()
        else:
            messagebox.showerror("Error", "Invalid username or password")

    def forgot_password(self):
        ForgotPasswordWindow(self)

class ForgotPasswordWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reset Password")
        self.geometry("300x150")
        self.create_widgets()

    def create_widgets(self):
        self.username_label = tk.Label(self, text="Username")
        self.username_label.pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        self.new_password_label = tk.Label(self, text="New Password")
        self.new_password_label.pack()
        self.new_password_entry = tk.Entry(self, show="*")
        self.new_password_entry.pack()

        self.confirm_password_label = tk.Label(self, text="Confirm Password")
        self.confirm_password_label.pack()
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack()

        self.reset_button = tk.Button(self, text="Reset Password", command=self.reset_password)
        self.reset_button.pack()

    def reset_password(self):
        username = self.username_entry.get()
        new_password = self.new_password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if reset_password(username, new_password):
            if new_password == confirm_password:
                messagebox.showinfo("Success", "Password reset successfully")
                self.destroy()
            else:
                messagebox.showinfo("Error", "Password doesn't match")
        else:
            messagebox.showerror("Error", "Username not found")
        
if __name__ == "__main__":
    app = LoginWindow()
    app.mainloop()
