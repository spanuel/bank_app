import tkinter as tk
from tkinter import messagebox
from bank_app.authentication import register_user
from bank_app.password_generator import generate_password

class RegistrationWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Register")
        self.geometry("300x200")
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
        self.generate_password_checkbox = tk.Checkbutton(self, text="Generate random password", variable=self.generate_password_var, command=self.toggle_password_entry)
        self.generate_password_checkbox.pack()

        self.balance_label = tk.Label(self, text="Opening Balance")
        self.balance_label.pack()
        self.balance_entry = tk.Entry(self)
        self.balance_entry.pack()

        self.register_button = tk.Button(self, text="Register", command=self.register)
        self.register_button.pack()

    def toggle_password_entry(self):
        if self.generate_password_var.get():
            self.password_entry.configure(state='disabled')                      
        else:
            self.password_entry.configure(state='normal')

    def register(self):
        username = self.username_entry.get()
        balance = self.balance_entry.get()

        if self.generate_password_var.get():
            password = generate_password()
            messagebox.showinfo("Generated Password", f"Your generated password is: {password}")           
        else:
            password = self.password_entry.get()

        
        try:
            balance = round(float(balance),2) 
        except ValueError:
            messagebox.showerror("Error", "Invalid balance amount. Please enter a numeric value.")
            return

        if register_user(username, password, balance):
            messagebox.showinfo("Success", "User registered successfully")
            self.destroy()
            from bank_app.ui_login import LoginWindow
            LoginWindow().mainloop()
        else:
            messagebox.showerror("Error", "Username already exists")

if __name__ == "__main__":
    app = RegistrationWindow()
    app.mainloop()
