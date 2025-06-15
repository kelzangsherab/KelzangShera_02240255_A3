import tkinter as tk
from tkinter import messagebox, simpledialog

class InvalidAmountError(Exception):
    """Raised when amount is invalid (negative or zero)"""
    pass

class InsufficientFundsError(Exception):
    """Raised when account has insufficient funds"""
    pass

class BankAccount:
    def __init__(self, name, balance=0):
        self.name = name
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        self.balance += amount
        self.transactions.append(f"Deposited Nu.{amount}")

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Withdrew Nu.{amount}")

    def transfer(self, amount, target):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        if target == self:
            raise InvalidAmountError("Cannot transfer to same account")
        self.balance -= amount
        target.balance += amount
        self.transactions.append(f"Sent Nu.{amount} to {target.name}")
        target.transactions.append(f"Received Nu.{amount} from {self.name}")

    def mobile_topup(self, amount, number):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")
        if amount > self.balance:
            raise InsufficientFundsError("Not enough balance")
        self.balance -= amount
        self.transactions.append(f"Mobile top-up Nu.{amount} to {number}")

    def get_transactions(self):
        return self.transactions

class BankingApp:
    def __init__(self, master):
        self.master = master
        master.title("Bhutanese Banking App")
        self.accounts = {}
        self.current = None

        tk.Label(master, text="Welcome to Bhutanese Banking App").pack()
        tk.Button(master, text="Open Account", command=self.open_account).pack()
        tk.Button(master, text="Select Account", command=self.select_account).pack()
        
        self.deposit_btn = tk.Button(master, text="Deposit", command=self.deposit, state=tk.DISABLED)
        self.deposit_btn.pack()
        self.withdraw_btn = tk.Button(master, text="Withdraw", command=self.withdraw, state=tk.DISABLED)
        self.withdraw_btn.pack()
        self.transfer_btn = tk.Button(master, text="Send Money", command=self.transfer, state=tk.DISABLED)
        self.transfer_btn.pack()
        self.topup_btn = tk.Button(master, text="Mobile Top-Up", command=self.mobile_topup, state=tk.DISABLED)
        self.topup_btn.pack()
        self.delete_btn = tk.Button(master, text="Close Account", command=self.close_account, state=tk.DISABLED)
        self.delete_btn.pack()
        
        self.balance_label = tk.Label(master, text="No account selected")
        self.balance_label.pack()
        self.txn_text = tk.Text(master, height=8, width=40, state=tk.DISABLED)
        self.txn_text.pack()
        tk.Button(master, text="Quit", command=master.quit).pack()

    def open_account(self):
        name = simpledialog.askstring("Open Account", "Enter account holder name:")
        if name and name not in self.accounts:
            bal = simpledialog.askfloat("Open Account", "Enter opening balance (Nu.):", minvalue=0)
            if bal is not None:
                self.accounts[name] = BankAccount(name, bal)
                messagebox.showinfo("Success", f"Account opened for {name}")
        elif name:
            messagebox.showerror("Error", "Account already exists")

    def select_account(self):
        if not self.accounts:
            messagebox.showerror("Error", "No accounts yet")
            return
        name = simpledialog.askstring("Select Account", "Enter account holder name:")
        if name in self.accounts:
            self.current = self.accounts[name]
            self.update_display()
            for btn in [self.deposit_btn, self.withdraw_btn, self.transfer_btn, self.topup_btn, self.delete_btn]:
                btn.config(state=tk.NORMAL)
        else:
            messagebox.showerror("Error", "Account not found")

    def update_display(self):
        if self.current:
            self.balance_label.config(text=f"{self.current.name} Balance: Nu.{self.current.balance:.2f}")
            self.txn_text.config(state=tk.NORMAL)
            self.txn_text.delete(1.0, tk.END)
            for t in self.current.transactions:
                self.txn_text.insert(tk.END, f"{t}\n")
            self.txn_text.config(state=tk.DISABLED)

    def deposit(self):
        amt = simpledialog.askfloat("Deposit", "Enter amount (Nu.):", minvalue=0.01)
        if amt:
            try:
                self.current.deposit(amt)
                self.update_display()
                messagebox.showinfo("Success", f"Deposited Nu.{amt}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def withdraw(self):
        amt = simpledialog.askfloat("Withdraw", "Enter amount (Nu.):", minvalue=0.01)
        if amt:
            try:
                self.current.withdraw(amt)
                self.update_display()
                messagebox.showinfo("Success", f"Withdrew Nu.{amt}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def transfer(self):
        if len(self.accounts) < 2:
            messagebox.showerror("Error", "Need at least 2 accounts")
            return
        target = simpledialog.askstring("Send Money", "Enter recipient's name:")
        if target and target in self.accounts and target != self.current.name:
            amt = simpledialog.askfloat("Send Money", "Enter amount (Nu.):", minvalue=0.01)
            if amt:
                try:
                    self.current.transfer(amt, self.accounts[target])
                    self.update_display()
                    messagebox.showinfo("Success", f"Sent Nu.{amt} to {target}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Error", "Invalid recipient")

    def mobile_topup(self):
        number = simpledialog.askstring("Mobile Top-Up", "Enter mobile number:")
        if number:
            amt = simpledialog.askfloat("Mobile Top-Up", "Enter amount (Nu.):", minvalue=0.01)
            if amt:
                try:
                    self.current.mobile_topup(amt, number)
                    self.update_display()
                    messagebox.showinfo("Success", f"Topped up Nu.{amt} to {number}")
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def close_account(self):
        if self.current:
            confirm = messagebox.askyesno("Close Account", f"Close account for {self.current.name}?")
            if confirm:
                del self.accounts[self.current.name]
                self.current = None
                self.balance_label.config(text="No account selected")
                self.txn_text.config(state=tk.NORMAL)
                self.txn_text.delete(1.0, tk.END)
                self.txn_text.config(state=tk.DISABLED)
                for btn in [self.deposit_btn, self.withdraw_btn, self.transfer_btn, self.topup_btn, self.delete_btn]:
                    btn.config(state=tk.DISABLED)
                messagebox.showinfo("Success", "Account closed")

if __name__ == "__main__":
    root = tk.Tk()
    app = BankingApp(root)
    root.mainloop()