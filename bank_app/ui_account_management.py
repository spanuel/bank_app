import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

class AccountManagementWindow(tk.Tk):
    def __init__(self,account):
        super().__init__()
        self.account = account
        self.title("Account Management")
        self.geometry("300x300")
        self.eval('tk::PlaceWindow . center')
        self.create_widgets()

    def create_widgets(self):
        username = self.account.username.capitalize()
        balance = self.account.balance

        self.greet_label = tk.Label(self,text=f"Hello, {username}")
        self.greet_label.pack(pady=5)

        self.balance_label = tk.Label(self,text=f"Current Balance: R{balance:.2f}")
        self.balance_label.pack(pady=5)

        self.deposit_button = tk.Button(self, text="Deposit", bg="gray", command=self.deposit)
        self.deposit_button.pack(pady=10)

        self.withdraw_button = tk.Button(self, text="Withdraw", bg="gray", command=self.withdraw)
        self.withdraw_button.pack(pady=10)

        self.transfer_button = tk.Button(self, text="Transfer", bg="gray", command=self.transfer)
        self.transfer_button.pack(pady=10)

        self.transaction_history_button = tk.Button(self, text="Transaction History", bg="gray", command=self.show_transaction_history)
        self.transaction_history_button.pack(pady=10)

        self.bank_statement_button = tk.Button(self, text="Bank Statement", bg="gray", command=self.show_bank_statement)
        self.bank_statement_button.pack(pady=10)

    def update_balance_label(self):
        self.balance_label.config(text=f"Current Balance: R{self.account.balance:.2f}")

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None:
            try:
                self.account.deposit(amount)
                self.update_balance_label()
                messagebox.showinfo("Success", "Deposit successful")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None:
            try:
                self.account.withdraw(amount)
                self.update_balance_label()
                messagebox.showinfo("Success", "Withdrawal successful")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def transfer(self):
        recipient_username = simpledialog.askstring("Transfer", "Enter recipient's username:")
        if recipient_username:
            amount = simpledialog.askfloat("Transfer", "Enter amount to transfer:")
            if amount is not None:
                try:
                    self.account.transfer(recipient_username, amount)
                    self.update_balance_label()
                    messagebox.showinfo("Success", "Transfer successful")
                except ValueError as e:
                    messagebox.showerror("Error", str(e))

    def show_transaction_history(self):
        transactions = self.account.get_transaction_history(self.account.username)
        messagebox.showinfo("Transaction History", "\n".join(transactions))

    def show_bank_statement(self):
        statement = self.account.get_bank_statement()
        messagebox.showinfo("Bank Statement", "\n".join(statement))
  

if __name__ == "__main__":
    app = AccountManagementWindow("")
    app.mainloop()

