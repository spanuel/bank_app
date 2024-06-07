import tkinter as tk
from bank_app.account import Account

class AccountManagementWindow(tk.Tk):
    def __init__(self,username):
        super().__init__()
        self.username = username
        self.account = Account.load_account(username)
        self.title("Account Management")
        self.geometry("300x300")
        self.eval('tk::PlaceWindow . center')
        self.create_widgets()

    def create_widgets(self):
        self.greet_label = tk.Label(self,text=f"Hello {self.username}")
        self.greet_label.pack()

        self.balance_label = tk.Label(self,text=f"Current Balance: R{self.account.balance}")
        self.balance_label.pack()

        self.deposit_button = tk.Button(self, text="Deposit")
        self.deposit_button.pack()

        self.withdraw_button = tk.Button(self, text="Withdraw")
        self.withdraw_button.pack()

        self.transfer_button = tk.Button(self, text="Transfer")
        self.transfer_button.pack()


if __name__ == "__main__":
    app = AccountManagementWindow("")
    app.mainloop()

