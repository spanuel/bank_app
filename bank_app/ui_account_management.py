import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox
from datetime import datetime
from bank_app.account import Account 

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
        transactions = Account.get_transaction_history(self.account.username)
        messagebox.showinfo("Transaction History", "\n".join(transactions))

    def show_bank_statement(self):
        from_date = self.get_date("From Date")
        if from_date:
            to_date = self.get_date("To Date")
            if to_date:
                statement = self.account.get_bank_statement(from_date, to_date)
                self.display_bank_statement(from_date, to_date)

    def get_date(self, prompt):
        date_str = simpledialog.askstring("Date Entry", f"Enter {prompt} (YYYY-MM-DD):")
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please enter a valid date in YYYY-MM-DD format.")
            return None

    def display_bank_statement(self, from_date, to_date):
        statement = self.account.get_bank_statement(from_date, to_date)

        statement_window = tk.Toplevel(self)
        statement_window.title("Bank Statement")
        statement_window.geometry("600x400")
        statement_text = tk.Text(statement_window, wrap=tk.WORD)
        statement_text.pack(expand=True, fill=tk.BOTH)

        statement_header = (
            f"Tech Junkies Bank\n\n"
            f"Bank Statement\n"
            f"From Date: {from_date.strftime('%Y-%m-%d')}\n"
            f"To Date: {to_date.strftime('%Y-%m-%d')}\n"
            f"Print Date: {datetime.now().strftime('%Y-%m-%d')}\n\n"
            f"Personal Details\n"
            f"{self.account.username.capitalize()}\n"
            f"Account Number: {self.account.account_number}\n\n"
            f"Transaction Date\tDescription\tMoney In (R)\tMoney Out (R)\tBalance (R)\n"
        )
        statement_text.insert(tk.END, statement_header)

        for transaction in statement:
            parts = transaction.split(' - ')
            date = parts[0]
            desc = parts[2]
            amount = float(parts[3].split(' ')[1])
            balance = float(parts[4].split(' ')[1])
            if desc in ["Deposit", "Receive"]:
                money_in = f"{amount:.2f}"
                money_out = ""
            else:
                money_in = ""
                money_out = f"{amount:.2f}"

            statement_text.insert(tk.END, f"{date}\t{desc}\t{money_in}\t{money_out}\t{balance:.2f}\n")

        statement_text.config(state=tk.DISABLED)

  
if __name__ == "__main__":
    app = AccountManagementWindow("")
    app.mainloop()

