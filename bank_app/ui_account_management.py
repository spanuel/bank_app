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
        self.greet_label.pack(pady=5)

        self.balance_label = tk.Label(self,text=f"Current Balance: R{self.account.balance}")
        self.balance_label.pack(pady=5)

        self.deposit_button = tk.Button(self, text="Deposit",bg="gray")
        self.deposit_button.pack(pady=10)

        self.withdraw_button = tk.Button(self, text="Withdraw",bg="gray")
        self.withdraw_button.pack(pady=10)

        self.transfer_button = tk.Button(self, text="Transfer",bg="gray")
        self.transfer_button.pack(pady=10)

        self.transaction_history_button = tk.Button(self, text="Transaction History",bg="gray")
        self.transaction_history_button.pack(pady=10)

        self.bank_statement_button = tk.Button(self, text="Bank Statement",bg="gray")
        self.bank_statement_button.pack(pady=10)


if __name__ == "__main__":
    app = AccountManagementWindow("")
    app.mainloop()

