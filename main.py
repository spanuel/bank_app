import tkinter as tk
from bank_app.ui_login import LoginWindow
from bank_app.ui_registration import RegistrationWindow

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Banking App")
        self.geometry("300x150")
        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Welcome to the Banking App")
        self.label.pack(pady=10)

        self.login_button = tk.Button(self, text="Login", command=self.open_login_window)
        self.login_button.pack(pady=5)

        self.register_button = tk.Button(self, text="Register", command=self.open_registration_window)
        self.register_button.pack(pady=5)

    def open_login_window(self):
        self.destroy() 
        LoginWindow().mainloop()

    def open_registration_window(self):
        self.destroy() 
        RegistrationWindow().mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
